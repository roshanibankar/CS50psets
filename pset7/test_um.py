from um import count

def test_basic():
    assert count("um") == 1
    assert count("Um") == 1
    assert count("UM") == 1

def test_punctuation():
    assert count("um, thanks") == 1
    assert count("well, um... okay") == 1
    assert count("Um?") == 1

def test_multiple():
    assert count("um, um, um") == 3
    assert count("Um, thanks, um... okay, um!") == 3

def test_no_um():
    assert count("yummy") == 0
    assert count("umbrella") == 0
    assert count("album") == 0
