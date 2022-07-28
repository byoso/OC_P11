#! /usr/bin/env python3
# coding: utf-8


"""Execute the tests with 'pytest -v --cov=src'"""


from src import server
from tests.conftest import mocker_data
from src.settings import PLACE_COST


class TestServer:
    # def setup_method(self, method, mocker):
    #     mocker.patch.object(server, 'data', mocker_data)

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_showSummary(self, client, mocker):
        mocker.patch.object(server, 'data', mocker_data)
        response = client.post("/showSummary", data={"email": "user@test.com"})
        assert response.status_code == 200

        # redirect if wrong email
        response = client.post(
            "/showSummary", data={"email": "not_user@test.com"})
        assert response.status_code == 302

    def test_book(self, client, mocker):
        mocker.patch.object(server, 'data', mocker_data)
        response = client.get("/book/Comp_1/Club_1")
        assert response.status_code == 200
        response = client.get("/book/no_Comp/no_Club")
        assert response.status_code == 404

    def test_purchase_places(self, client, mocker):
        mocker.patch.object(server, 'data', mocker_data)
        # remaining_points = mocker_data.clubs[0].points
        response = client.post(
            '/purchasePlaces',
            data={'club': "Club_1", 'competition': 'Comp_1', 'places': '5'})

        assert response.status_code == 200
        # points are consumed:
        club = mocker_data.clubs[0]
        assert club.points == 100 - 5*PLACE_COST

        # 10 more is refused (more than 12)
        response = client.post(
            '/purchasePlaces',
            data={'club': "Club_1", 'competition': 'Comp_1', 'places': '10'})
        assert response.status_code == 200
        assert club.points == 100 - 5*PLACE_COST  # the points remain the same

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == 302  # redirection

    def test_clubs_display(self, client):
        response = client.get('/clubs_display')
        assert response.status_code == 200
