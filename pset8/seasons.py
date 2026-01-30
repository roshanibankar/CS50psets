from datetime import date
import sys
import inflect


def main():
    birth_date_str = input("Date of Birth: ")
    try:
        birth_date = validate_date(birth_date_str)
    except ValueError:
        sys.exit("Invalid date")

    minutes = minutes_since_birth(birth_date)
    print(number_to_words(minutes) + " minutes")


def validate_date(birth_date_str):
    try:
        year, month, day = map(int, birth_date_str.split("-"))
        return date(year, month, day)
    except Exception:
        raise ValueError("Invalid date format")


def minutes_since_birth(birth_date):
    today = date.today()
    days_difference = (today - birth_date).days
    if days_difference < 0:
        raise ValueError("Birth date cannot be in the future")
    return days_difference * 24 * 60

def number_to_words(number):
    p = inflect.engine()
    words = p.number_to_words(number, andword="")
    return words.capitalize()


if __name__ == "__main__":
    main()
