import os
os.system('cls')
import pandas as pd
import math

def octact_identification(mod=5000):
    try:
        df = pd.read_csv('octant_input.csv')
        print(df.head())
    except:
        print("Error: File does not appear to exist.")
        exit()

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000
octact_identification(mod)