import random

def main():
    while True:
        try:
            n = int(input("Number: "))
            if n <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
    
    guess_game(n)


def guess_game(n):
    number = random.randint(0, n)
    print(f"Guess the number between 0 and {n}")
    
    while True:
        try:
            user_guess = int(input("Your guess: "))
            if user_guess < number:
                print("Too low!")
            elif user_guess > number:
                print("Too high!")
            else:
                print("You guessed it!")
                break
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()


