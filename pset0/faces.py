def convert(text:str)->str:
    text = text.replace(":)", "🙂")
    text = text.replace(":(", "🙁")
    return text

input=input()
converted=convert(input)
print(converted)


