
#control- d for EOF error
menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

def get_total_cost(order):
    total = 0
    for item in order:
        total += menu.get(item, 0)
    return total

def main():
    order = []
    try:
        while True:
            try:
                item = input("Item: ").strip().title()
                order.append(item)
                total_cost = get_total_cost(order)
                print(f"Total: ${total_cost:.2f}")
            except EOFError:
                break
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
