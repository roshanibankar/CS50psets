def main():
    grocery_list = {}
    try:
        while True:
            try:
                item = input("").strip().title()
                grocery_list[item] = grocery_list.get(item, 0) + 1
            except EOFError:
                break
    except KeyboardInterrupt:
        pass

    sorted_items = sorted(grocery_list.items(), key=lambda x: x[0])
    for item, count in sorted_items:
        print(f"{count} {item.upper()}")

if __name__ == "__main__":
    main()