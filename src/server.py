#! /usr/bin/env python3
# coding: utf-8


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
)

from .datas import (
    Data,
)
from .helpers import (
    date_is_past,
)


app = Flask(__name__)
app.secret_key = 'something_special'

data = Data()


@app.route('/')
def index():
    """displays the login form"""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """displays the summary if logged in"""
    club = [club for club in data.clubs
            if club.email == request.form['email']]
    if club:
        return render_template(
            'welcome.html', club=club[0],
            competitions=data.competitions)
    else:
        flash(f"Unknown email: '{request.form['email']}'")
        return redirect(url_for('index'))


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name, club_name):
    """displays the booking form"""
    foundClub = [club for club in data.clubs if club.name == club_name]
    foundCompetition = [comp for comp in data.competitions
                        if comp.name == competition_name]
    if foundClub and foundCompetition:
        club = foundClub[0]
        competition = foundCompetition[0]
        try:
            tickets_spent = competition.tickets_spent[club.name]
        except KeyError:
            competition.tickets_spent = {}
            competition.tickets_spent[club.name] = 0
            tickets_spent = 0

        return render_template(
            'booking.html', club=club, competition=competition,
            tickets_spent=tickets_spent)
    else:
        abort(404)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Purchasing some places slogic"""
    competition = [comp for comp in data.competitions
                   if comp.name == request.form['competition']][0]
    club = [c for c in data.clubs if c.name == request.form['club']][0]
    try:
        # no booking if the competition is past:
        if date_is_past(competition.date):
            print("DATE IS PAST")
            flash("Aborted: Impossible to book places in a past competition.")
            return render_template(
                'welcome.html', club=club, competitions=data.competitions)

        placesRequired = int(request.form['places'])
        if placesRequired < 1:  # no negative value allowed
            raise ValueError
    except ValueError:
        placesRequired = 0
        flash('Aborted: invalid value given')
    tickets_spent = competition.tickets_spent[club.name]
    if int(club.points) >= placesRequired and\
            placesRequired + tickets_spent <= 12:
        competition.numberOfPlaces = int(
            competition.numberOfPlaces)-placesRequired
        competition.tickets_spent[club.name] += placesRequired
        club.points = int(club.points) - placesRequired
        if placesRequired != 0:
            flash('Great-booking complete!')
        return render_template(
            'welcome.html', club=club, competitions=data.competitions)
    else:
        flash(
            f"Aborted: asked {placesRequired} places (12 max)."
            )
        return render_template(
            'booking.html', club=club, competition=competition,
            tickets_spent=tickets_spent
            )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
