#! /usr/bin/env python3
# coding: utf-8

import os
import json
from datetime import datetime


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

# sets this directory as the base for all relative paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def loadClubs():
    with open(os.path.join(BASE_DIR, 'clubs.json')) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open(os.path.join(BASE_DIR, 'competitions.json')) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """displays the login form"""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """displays the summary if logged in"""
    club = [club for club in clubs
            if club['email'] == request.form['email']]
    if club:
        return render_template(
            'welcome.html', club=club[0],
            competitions=competitions)
    else:
        flash(f"Unknown email: '{request.form['email']}'")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """displays the booking form"""
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        club = foundClub[0]
        competition = foundCompetition[0]
        try:
            tickets_spent = competition['tickets_spent'][club['name']]
        except KeyError:
            competition['tickets_spent'] = {}
            competition['tickets_spent'][club['name']] = 0
            tickets_spent = 0
        return render_template(
            'booking.html', club=club, competition=competition,
            tickets_spent=tickets_spent)
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Purchasing some places slogic"""
    competition = [c for c in competitions
                   if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        placesRequired = 0
        flash('Aborted: invalid value given')
    tickets_spent = competition['tickets_spent'][club['name']]
    if int(club['points']) >= placesRequired and\
            placesRequired + tickets_spent <= 12:
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces'])-placesRequired
        competition['tickets_spent'][club['name']] += placesRequired
        club['points'] = int(club['points']) - placesRequired
        if placesRequired != 0:
            flash('Great-booking complete!')
        return render_template(
            'welcome.html', club=club, competitions=competitions)
    else:
        flash(
            f"Aborted: asked {placesRequired} places (12 max)."
            f" Your club owns {club['points']} points."
            f" You spent {tickets_spent}/12 in this competition. ")
        return render_template(
            'booking.html', club=club, competition=competition
            )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
