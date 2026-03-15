import shutil
import os
os.chdir("first")
shutil.copytree("second","folder")
os.chdir("..")