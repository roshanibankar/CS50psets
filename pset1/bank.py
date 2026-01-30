
import re


def main():
    greeting = input("Enter the greeting: ")
    amount = value(greeting)
    print(f"${amount}")

def value(greeting):
    greeting = greeting.lower()
    greeting = re.sub("!", "", greeting)
    greeting = greeting.strip()

    if greeting.startswith("hello"):
        return 0
    elif greeting[0] == "h":
        return 20
    else:
        return 100

if __name__ == "__main__":
    main()