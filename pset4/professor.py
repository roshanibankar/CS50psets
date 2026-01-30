import random

def main():
    level = get_level()
    score = 0
    for _ in range(10):
        x, y = generate_integer(level), generate_integer(level)
        for _ in range(3):
            try:
                if int(input(f"{x} + {y} = ")) == x + y:
                    score += 1
                    break
            except ValueError:
                pass
            print("EEE")
        else:
            print(f"{x} + {y} = {x + y}")

    print(f"Score: {score}")


def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level in [1, 2, 3]:
                return level
        except ValueError:
            pass


def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)
    else:
        raise ValueError



if __name__ == "__main__":
    main()
