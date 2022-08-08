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
from .settings import PLACE_COST


app = Flask(__name__)
app.secret_key = 'something_special'

data = Data()


@app.route('/')
def index():
    """displays the login form"""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST', 'GET'])
def showSummary():
    """displays the summary if logged in"""
    if request.method == 'POST':
        club = [club for club in data.clubs
                if club.email == request.form['email']]
        if club:
            data.current_club = club[0]
            return render_template(
                'welcome.html', club=club[0],
                competitions=data.competitions)
        else:
            flash(f"Unknown email: '{request.form['email']}'")
            return redirect(url_for('index'))

    if request.method == 'GET':
        if data.current_club is not None:
            return render_template(
                'welcome.html', club=data.current_club,
                competitions=data.competitions)
        else:
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
            places_booked = competition.places_booked[club.name]
        except KeyError:
            competition.places_booked[club.name] = 0
            places_booked = 0

        return render_template(
            'booking.html', club=club, competition=competition,
            places_booked=places_booked)

    else:
        abort(404)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Purchasing some places logic"""
    competition = [comp for comp in data.competitions
                   if comp.name == request.form['competition']][0]
    club = [c for c in data.clubs if c.name == request.form['club']][0]
    try:
        # no booking if the competition is past:
        if date_is_past(competition.date):
            flash("Aborted: Impossible to book places in a past competition.")
            return render_template(
                'welcome.html', club=club, competitions=data.competitions)

        placesRequired = int(request.form['places'])
        if placesRequired < 1:  # no negative value allowed
            raise ValueError
        if not isinstance(placesRequired, int):
            raise ValueError
    except ValueError:
        placesRequired = 0
        flash('Aborted: invalid value given')
    places_booked = competition.places_booked[club.name]
    if int(club.points) >= placesRequired*PLACE_COST and\
            placesRequired <= int(competition.numberOfPlaces) and\
            placesRequired + places_booked <= 12:
        competition.numberOfPlaces = int(
            competition.numberOfPlaces)-placesRequired
        competition.places_booked[club.name] += placesRequired
        club.points = int(club.points) - placesRequired*PLACE_COST
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
            places_booked=places_booked
            )


@app.route('/clubs_display')
def clubs_display():
    clubs = data.clubs
    return render_template("clubs_display.html", clubs=clubs)


@app.route('/logout')
def logout():
    data.current_club = None
    return redirect(url_for('index'))
