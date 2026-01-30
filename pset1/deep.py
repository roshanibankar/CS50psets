import re
n=input("What's the answer to the life the universe and everything: ")
n=n.lower().strip()
n = re.sub(r"\s+", " ", n) 

if n=="42" or n=="forty-two" or n=="forty two":
   print("Yes")
else:
    print("No")
