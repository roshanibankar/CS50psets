def main():
    a = input("What time is it? ").strip().lower()
    time = convert(a)

    if 7 <= time <= 8:
        print("breakfast time")
    elif 12 <= time <= 13:
        print("lunch time")
    elif 18 <= time <= 19:
        print("dinner time")


def convert(time):
    #a 12hr format with AM/PM
    if "a.m." in time or "p.m." in time:
        is_pm = "p.m." in time
        time = time.replace("a.m.", "").replace("p.m.", "").strip()
        hours, minutes = map(int, time.split(":"))

        if is_pm and hours != 12:
            hours += 12
        if not is_pm and hours == 12:
            hours = 0
    else:
        # 24hr format
        hours, minutes = map(int, time.split(":"))

    return hours + minutes / 60



if __name__ == "__main__":
    main()
