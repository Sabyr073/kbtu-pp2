import shutil
import os
shutil.copy("file.txt","copy.txt")
os.remove("copy.txt")
os.remove("file.txt")