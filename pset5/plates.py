def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    #plate length between 2 and 6 characters
    if len(s) < 2 or len(s) > 6:
        return False

    #all characters must be alphanumeric
    if not s.isalnum():
        return False

    #numbers cannot be in the middle; if numbers exist, they must be at the end
    for i, char in enumerate(s):
        if char.isdigit() and i == 0:
            return False  # first character cannot be a number
        if char.isdigit() and s[i-1].isalpha() and not s[i:].isdigit():
            return False  # digits must come at the end

    #first number used cannot be '0'
    for char in s:
        if char.isdigit():
            if char == '0':
                return False
            break

    return True


if __name__ == "__main__":
    main()
