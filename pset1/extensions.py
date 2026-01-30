import re 
a=input("File Name: ")
a=a.lower() and re.sub("!&-.*","",a) and a.lstrip(" ") and a.rstrip(" ")
if a.endswith(".jpeg"):
    print("image/jpeg")
elif a.endswith(".jpg"):
    print("image/jpg")
elif a.endswith(".gif"):
    print("image/gif")
elif a.endswith(".pdf"):
    print("document/pdf")
elif a.endswith(".zip"):
    print("document/zip")
elif a.endswith(".png"):
    print("image/png")
elif a.endswith(".txt"):
    print("document/txt")
else:
    print("application/octet-stream")