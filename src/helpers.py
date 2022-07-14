
from datetime import datetime


def str_to_date(string):
    date = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    return date


def date_is_past(date_str):
    date = str_to_date(date_str)
    today = datetime.now()
    if today > date:
        return True
    else:
        return False
