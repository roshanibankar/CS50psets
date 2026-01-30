from fuel import convert , gauge 

import pytest
from fuel import convert, gauge


def test_convert_normal():
    assert convert("1/2") == 50
    assert convert("3/4") == 75
    assert convert("0/5") == 0
    assert convert("5/5") == 100

def test_convert_rounding():
    assert convert("1/3") == 33
    assert convert("2/3") == 67

def test_convert_invalid_input():
    with pytest.raises(ValueError):
        convert("a/b")
    with pytest.raises(ValueError):
        convert("5/2")  # X > Y
    with pytest.raises(ValueError):
        convert("-1/2")
    with pytest.raises(ValueError):
        convert("1/-2")
    with pytest.raises(ValueError):
        convert("1.5/2")

def test_convert_zero_division():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")

def test_gauge_extremes():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(100) == "F"

def test_gauge_middle():
    assert gauge(50) == "50%"
    assert gauge(33) == "33%"
    assert gauge(67) == "67%"
