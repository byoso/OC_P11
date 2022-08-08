#! /usr/bin/env python3
# coding: utf-8


"""Execute the tests with 'pytest -v --cov=src'"""


from src import server
from tests.tests_unit.conftest import mocker_data
from src.settings import PLACE_COST


class TestServer:

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_showSummary(self, client, mocker):
        # POST
        # if email is known
        mocker.patch.object(server, 'data', mocker_data)
        response = client.post("/showSummary", data={"email": "user@test.com"})
        assert response.status_code == 200

        # redirect if wrong email
        response = client.post(
            "/showSummary", data={"email": "not_user@test.com"})
        assert response.status_code == 302

        # GET
        # current club logged in
        response = client.get("/showSummary")
        assert response.status_code == 200

        # no current club logged
        mocker_data.current_club = None
        response = client.get("/showSummary")
        assert response.status_code == 302

    def test_book(self, client, mocker):
        # club and competition exist
        mocker.patch.object(server, 'data', mocker_data)
        response = client.get("/book/Comp_1/Club_1")
        assert response.status_code == 200
        # club or competition does't exist
        response = client.get("/book/no_Comp/no_Club")
        assert response.status_code == 404

    def test_purchase_places(self, client, mocker):
        mocker.patch.object(server, 'data', mocker_data)
        # invalid input, no points substracted
        club = mocker_data.clubs[0]
        response = client.post(
            '/purchasePlaces',
            data={
                'club': "Club_1",
                'competition': 'Comp_1', 'places': 'wrong input'})
        assert response.status_code == 200
        assert club.points == 100

        # input < 1
        club = mocker_data.clubs[0]
        response = client.post(
            '/purchasePlaces',
            data={
                'club': "Club_1",
                'competition': 'Comp_1', 'places': '-12'})
        assert response.status_code == 200
        assert club.points == 100

        # correct request
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

    def test_clubs_display(self, client):
        response = client.get('/clubs_display')
        assert response.status_code == 200

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == 302  # redirection
