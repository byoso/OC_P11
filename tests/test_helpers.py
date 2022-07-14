import datetime

from src.helpers import (
    str_to_date,
    date_is_past,
)


class TestHelpers:
    def test_str_to_date(self):
        str_date = "2021-01-01 13:00:00"
        date = str_to_date(str_date)
        assert type(date) == datetime.datetime
        assert str(date) == str_date

    def test_date_is_past(self):
        date_passed = "2021-01-01 13:00:00"
        date_not_passed = "2121-01-01 13:00:00"

        assert date_is_past(date_passed) is True
        assert date_is_past(date_not_passed) is False
