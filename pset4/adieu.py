
def bid_adieu(names):
    if len(names) == 1:
        print(f"Adieu, adieu, to {names[0]}")
    elif len(names) == 2:
        print(f"Adieu, adieu, to {names[0]} and {names[1]}")
    else:
        farewell = ", ".join(names[:-1])  
        farewell += f", and {names[-1]}"  
        print(f"Adieu, adieu, to {farewell}")

def main():
    names = []
    try:
        while True:
            name = input("Name: ").strip()
            if name:
                names.append(name)
    except EOFError:
        pass
    
    if names:
        bid_adieu(names)

if __name__ == "__main__":
    main()

