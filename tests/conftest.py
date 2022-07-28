import pytest

from src.server import app
from src.datas import Club, Competition, Data


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


mock_clubs = [
    {
        "name": "Club_1",
        "email": "user@test.com",
        "points": 100
    },
]
mocker_clubs = [Club(**club) for club in mock_clubs]

mock_comps = [
        {
            "name": "Comp_1",
            "date": "2030-01-01 10:00:00",
            "numberOfPlaces": "25"
        },
]
mocker_comps = [Competition(**comp) for comp in mock_comps]

mocker_data = Data(None, None)
mocker_data.clubs = [Club(**club) for club in mock_clubs]
mocker_data.competitions = [Competition(**comp) for comp in mock_comps]
