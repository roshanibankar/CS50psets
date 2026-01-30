from bank import value

def test_hello_exact():
    assert value("hello") == 0
    assert value("Hello") == 0
    assert value("HELLO there") == 0

def test_h_but_not_hello():
    assert value("hi") == 20
    assert value("Hey") == 20
    assert value("howdy") == 20

def test_other_greetings():
    assert value("good morning") == 100
    assert value("what's up") == 100
    assert value("yo") == 100

def test_case_insensitivity():
    assert value("HeLLo") == 0
    assert value("hI") == 20
    assert value("GREETINGS") == 100

