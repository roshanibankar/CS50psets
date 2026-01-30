import emoji

def main():
    a=input("Input: ")
    if not a.startswith(":"):
        a = ":" + a
    if not a.endswith(":"):
        a = a + ":"
    try:
        result = emoji.emojize(a, language='alias')
        print(result)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
