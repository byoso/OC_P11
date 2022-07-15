

"""Data abstraction, should be replaced by an ORM for production"""


import os
import json


# sets this directory as the base for all relative paths to datas
DATA_DIR = os.path.abspath(os.path.dirname(__file__))


class Data:
    def __init__(
        self,
        clubs_file='clubs.json',
        competitions_file='competitions.json'
    ):
        self.current_club = None  # replace with authentication for production
        self.clubs_file = clubs_file
        self.competitions_file = competitions_file
        if clubs_file is not None and competitions_file is not None:
            self.clubs = self._loadClubs()
            self.competitions = self._loadCompetitions()

    def _loadClubs(self):
        with open(os.path.join(DATA_DIR, self.clubs_file)) as c:
            listOfClubs = json.load(c)['clubs']
            clubs = [Club(**club) for club in listOfClubs]
            return clubs

    def _loadCompetitions(self):
        with open(os.path.join(DATA_DIR, self.competitions_file)) as comps:
            listOfCompetitions = json.load(comps)['competitions']
            competitions = [Competition(**comp) for comp in listOfCompetitions]
            return competitions

    def __repr__(self):
        message = "\nClubs: \n"
        for club in self.clubs:
            message += f"- {club}\n"
        message += "\nCompetitions: \n"
        for comp in self.competitions:
            message += f"- {comp}\n"
        return message

    def __str__(self):
        return self.__repr__()


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
