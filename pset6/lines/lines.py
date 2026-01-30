import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python lines.py <filename.py>")

    filename = sys.argv[1]

    if not filename.endswith(".py"):
        sys.exit("Not a Python file.")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            count = 0
            for line in file:
                stripped = line.lstrip()

                if stripped == "": #blank lines
                    continue

                if stripped.startswith("#"): #comment lines
                    continue

                count += 1

            print(count)

    except FileNotFoundError:
        sys.exit("File does not exist.")

if __name__ == "__main__":
    main()
