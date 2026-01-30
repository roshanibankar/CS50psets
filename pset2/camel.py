camelCase = input("camelCase: ")
snake_case = ""

for c in camelCase:
    if c.isupper():
        snake_case += "_" + c.lower()
    else:
        snake_case += c

print("snake_case: ", snake_case)