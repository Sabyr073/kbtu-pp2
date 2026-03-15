import os
from pathlib import Path

os.makedirs("first/second/third/fourth")
os.chdir("first")
folders = ["data", "images", "text"]
for i in folders:
    os.mkdir(i)

print(os.listdir())
os.chdir("..")

for file in Path().iterdir():
    if file.suffix == ".py":
        print(file)