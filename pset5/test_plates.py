from plates import is_valid

#valid plates
def test_valid_plate_letters_only():
    assert is_valid("CS50") == True

def test_valid_plate_with_numbers_end():
    assert is_valid("ABC123") == True

#invalid plates
def test_too_short():
    assert is_valid("A") == False

def test_too_long():
    assert is_valid("ABCDEFG") == False

def test_invalid_characters():
    assert is_valid("CS50!") == False

def test_number_in_middle():
    assert is_valid("AB1C") == False

def test_first_number_zero():
    assert is_valid("AB0") == False

