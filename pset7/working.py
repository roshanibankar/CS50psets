import re
def main():
    print(convert(input("Hours: ")))

import re

def convert(s):
    pattern = r"^(\d{1,2})(?::(\d{2}))? (AM|PM) to (\d{1,2})(?::(\d{2}))? (AM|PM)$"
    match = re.search(pattern, s)
    if not match:
        raise ValueError("Invalid time format")

    h1, m1, mer1, h2, m2, mer2 = match.groups()
    m1 = m1 if m1 else "00"
    m2 = m2 if m2 else "00"

    h1, m1, h2, m2 = int(h1), int(m1), int(h2), int(m2)

    if not (1 <= h1 <= 12 and 0 <= m1 < 60 and 1 <= h2 <= 12 and 0 <= m2 < 60):
        raise ValueError("Invalid time values")

    def to_24(hour, meridiem):
        if meridiem == "AM":
            return 0 if hour == 12 else hour
        else:
            return 12 if hour == 12 else hour + 12

    h1_24 = to_24(h1, mer1)
    h2_24 = to_24(h2, mer2)

    return f"{h1_24:02}:{m1:02} to {h2_24:02}:{m2:02}"

if __name__ == "__main__":
    main()
