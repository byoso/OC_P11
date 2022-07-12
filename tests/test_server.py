#! /usr/bin/env python3
# coding: utf-8

from src import server
from tests.conftest import mocker_clubs, mocker_comps


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_showSummary(client, mocker):
    mocker.patch.object(server, 'clubs', mocker_clubs)
    response = client.post("/showSummary", data={"email": "user@test.com"})
    assert response.status_code == 200

    # redirect if wrong email
    response = client.post("/showSummary", data={"email": "not_user@test.com"})
    assert response.status_code == 302


def test_book(client, mocker):
    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_comps)
    response = client.get("/book/Comp_1/Club_1")
    assert response.status_code == 200
    response = client.get("/book/no_Comp/no_Club")
    assert response.status_code == 404


def test_purchase_places(client, mocker):
    mocker.patch.object(server, 'clubs', mocker_clubs)
    mocker.patch.object(server, 'competitions', mocker_comps)
    response = client.post(
        '/purchasePlaces',
        data={'club': "Club_1", 'competition': 'Comp_1', 'places': '5'})

    assert response.status_code == 200
    # points are consumed:
    club = mocker_clubs[0]
    assert club.points == 15

    # 10 more is refused (more than 12)
    response = client.post(
        '/purchasePlaces',
        data={'club': "Club_1", 'competition': 'Comp_1', 'places': '10'})
    assert response.status_code == 200
    assert club.points == 15  # points remain the same


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # redirection
