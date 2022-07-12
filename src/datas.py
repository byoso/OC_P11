
import os
import json


# sets this directory as the base for all relative paths to datas
DATA_DIR = os.path.abspath(os.path.dirname(__file__))


def loadClubs():
    with open(os.path.join(DATA_DIR, 'clubs.json')) as c:
        listOfClubs = json.load(c)['clubs']
        clubs = [Club(**club) for club in listOfClubs]
        return clubs


def loadCompetitions():
    with open(os.path.join(DATA_DIR, 'competitions.json')) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        competitions = [Competition(**comp) for comp in listOfCompetitions]
        return competitions


class Club:
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __str__(self) -> str:
        return f"<Club - {self.name}>"

    def __repr__(self) -> str:
        return str(self)


class Competition:
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
        if "tickets_spent" not in kwargs:
            self.tickets_spent = {}

    def __str__(self) -> str:
        return f"<Competition - {self.name}>"

    def __repr__(self) -> str:
        return str(self)
