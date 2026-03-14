with open("file.txt","x") as f:
    f.write("Hello \nPython is fun")

with open("file.txt","r") as f:
    print(f.read())