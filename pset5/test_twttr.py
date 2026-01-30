from twttr import shorten

def test_lowercase():
    assert shorten("twitter") == "twttr"

def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"

def test_mixed_case():
    assert shorten("TwItTeR") == "TwtTR"

def test_with_numbers():
    assert shorten("CS50") == "CS50"

def test_with_punctuation():
    assert shorten("What's up?") == "Wht's p?"

def test_only_vowels():
    assert shorten("aeiouAEIOU") == ""

def test_empty_string():
    assert shorten("") == ""
