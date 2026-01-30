x, y, z=input("Expression: ").split(" ")

def calculate(x,y,z):
    if y=="+":
        print(float(x)+float(z))
    elif y=="-":
        print(float(x)-float(z))
    elif y=="*":
        print(float(x)*float(z))
    elif y=="/":
        print(float(x)/float(z))

calculate(x,y,z)

