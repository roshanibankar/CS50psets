def main():
    fraction = input("Fraction: ")
    try:
        percentage = convert(fraction)
        print(gauge(percentage))
    except (ValueError, ZeroDivisionError):
        print("Invalid input")


def convert(fraction):
    try:
        x_str, y_str = fraction.split("/")
        x = int(x_str)
        y = int(y_str)
    except (ValueError, AttributeError):
        raise ValueError

    if y == 0:
        raise ZeroDivisionError

    if x > y or x < 0 or y < 0:
        raise ValueError

    percentage = round((x / y) * 100)
    return max(0, min(100, percentage))


def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()
