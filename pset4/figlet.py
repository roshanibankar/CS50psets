
import sys
import random
import pyfiglet
#python3 pset4/figlet.py -f slant

def print_usage_and_exit():
    print("Invalid usage")
    sys.exit(1)

def main():
    if len(sys.argv) == 1:
        font_name = random.choice(pyfiglet.FigletFont.getFonts())
    elif len(sys.argv) == 3 and (sys.argv[1] == '-f' or sys.argv[1] == '--font'):
        font_name = sys.argv[2]
        if font_name not in pyfiglet.FigletFont.getFonts():
            print_usage_and_exit()
    else:
        print_usage_and_exit()

    text = input("Input: ")
    figlet = pyfiglet.Figlet(font=font_name)
    ascii_art = figlet.renderText(text)
    print(ascii_art)

if __name__ == "__main__":
    main()
 