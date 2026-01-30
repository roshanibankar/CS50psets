import re

def main():
    print(parse(input("HTML: ")))

def parse(s):
    if matches := re.search(
        r'src="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)"', s):
        return f"https://youtu.be/{matches.group(1)}"
    return None

if __name__ == "__main__":
    main()

#<iframe src="http://www.youtube.com/embed/xvFZjo5PgG0"></iframe> for testing
