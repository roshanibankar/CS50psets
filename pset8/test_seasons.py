from datetime import date, timedelta
from seasons import validate_date, minutes_since_birth, number_to_words
import pytest


def test_validate_date_valid():
    assert validate_date("2000-01-01") == date(2000, 1, 1)


def test_validate_date_invalid_format():
    with pytest.raises(ValueError):
        validate_date("01-01-2000")
    with pytest.raises(ValueError):
        validate_date("2000/01/01")
    with pytest.raises(ValueError):
        validate_date("invalid-date")


def test_minutes_since_birth_one_year():
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    assert minutes_since_birth(one_year_ago) in [525600, 527040]  #leap year possible


def test_minutes_since_birth_two_years():
    today = date.today()
    two_years_ago = today - timedelta(days=730)
    minutes = minutes_since_birth(two_years_ago)
    assert minutes in [1051200, 1052640]


def test_minutes_since_birth_future_date():
    future = date.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        minutes_since_birth(future)


def test_number_to_words_basic():
    assert number_to_words(525600) == "Five hundred twenty-five thousand, six hundred"
    assert number_to_words(1051200).startswith("One million")


def test_number_to_words_capitalized():
    assert number_to_words(1000).startswith("One thousand")

