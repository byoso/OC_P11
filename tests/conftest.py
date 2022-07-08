import pytest

from src.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


mocker_clubs = [
    {
        "name": "Club_1",
        "email": "user@test.com",
        "points": 20
    },
]

mocker_comps = [
        {
            "name": "Comp_1",
            "date": "2030-01-01 10:00:00",
            "numberOfPlaces": "25"
        },
]
