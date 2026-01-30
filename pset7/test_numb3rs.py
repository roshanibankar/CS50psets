from numb3rs import validate

def test_valid():
    assert validate("127.0.0.1")
    assert validate("255.255.255.255")
    assert validate("0.0.0.0")
    assert validate("192.168.1.1")

def test_invalid_numbers():
    assert not validate("275.3.6.28")
    assert not validate("256.100.50.25")
    assert not validate("1.2.3.1000")

def test_invalid_format():
    assert not validate("cat")
    assert not validate("192.168.001.1")  
    assert not validate("192.168.1")
    assert not validate("192.168.1.1.1")
    assert not validate("192.168.1.-1")

