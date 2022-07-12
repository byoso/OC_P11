import pytest

from src.server import app
from src.datas import Club, Competition


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


clubs = [
    {
        "name": "Club_1",
        "email": "user@test.com",
        "points": 20
    },
]
mocker_clubs = [Club(**club) for club in clubs]

comps = [
        {
            "name": "Comp_1",
            "date": "2030-01-01 10:00:00",
            "numberOfPlaces": "25"
        },
]
mocker_comps = [Competition(**comp) for comp in comps]
