months_map = {
    "January": 1, "Jan": 1,
    "February": 2, "Feb": 2,
    "March": 3, "Mar": 3,
    "April": 4, "Apr": 4,
    "May": 5,
    "June": 6, "Jun": 6,
    "July": 7, "Jul": 7,
    "August": 8, "Aug": 8,
    "September": 9, "Sep": 9, "Sept": 9,
    "October": 10, "Oct": 10,
    "November": 11, "Nov": 11,
    "December": 12, "Dec": 12
}
# 12/11/2003, December 11, 2003, Dec 11, 2003

def is_valid_date(date_str):
    try:
        if "/" in date_str:
            month, day, year = map(int, date_str.split("/"))
        else:
            date_parts = date_str.split()
            if len(date_parts) != 3:
                return False
            month_str, day_str, year = date_parts
            if month_str not in months_map:
                return False
            month = months_map[month_str]
            day = int(day_str.strip(","))
        return 1 <= month <= 12 and 1 <= day <= 31 and int(year) > 0
    except (ValueError, IndexError):
        return False

def convert_to_iso(date_str):
    if "/" in date_str:
        month, day, year = map(int, date_str.split("/"))
    else:
        date_parts = date_str.split()
        month_str, day_str, year = date_parts
        month = months_map[month_str]
        day = int(day_str.strip(","))
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"  

def main():
    while True:
        date_input = input("Date: ")
        if is_valid_date(date_input):
            iso_date = convert_to_iso(date_input)
            print(iso_date)
            break
        else:
            print("Invalid date format. Try again.")

if __name__ == "__main__":
    main()
