#! /usr/bin/env python3
# coding: utf-8

import os
import json

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
            if club['email'] == request.form['email']][0]
    return render_template(
        'welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """displays the booking form"""
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Purchasing place slogic, should redirect to show summary"""
    competition = [c for c in competitions
                   if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template(
        'welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))