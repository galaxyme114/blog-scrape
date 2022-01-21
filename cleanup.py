import pandas as pd
import sys
import numpy as np
import os

def cleanup_csv(folder_name):

    for file in os.listdir(folder_name):
        if file.endswith(".csv"):
            loc_file = os.path.join(folder_name, file)
            
            df = pd.read_csv(loc_file)
            df_result = df[df["Open"] != 0]
            
            df_result.to_csv(loc_file, index=False)
    
            print(file + "   cleaned")
def read_file():
    array = []
    for file in os.listdir("."):
        if file.endswith(".csv"):
            array.append(file)
    print(array)
    return array
if __name__ == "__main__":
    '''
    with open("settings.txt") as f:
        folder = f.readlines()
    #print(folder[0])
    '''
    file_name = read_file()
    for file in file_name:
        print(file)
        #cleanup_csv(file)
        
    