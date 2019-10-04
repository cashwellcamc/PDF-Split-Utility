import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import config
import xlrd
import numpy as np
import pandas as pd
import math
import os

data1 = pd.read_excel(config.Excel1)
data2 = pd.read_excel(config.Excel2)

df = pd.DataFrame(data1)
header = df.iloc[0]
df = df[1:]
df.rename(columns = header)

df2 = pd.DataFrame(data2)
header2 = df2.iloc[0]
df2 = df2[1:]
df2.rename(columns = header2)

for filename in os.listdir(config.ManualCheck):
    if filename.endswith(".pdf"):
        First_Name, Last_Name, Zip = filename.replace(".pdf",'').split()
        Name = First_Name + " " + Last_Name

        print(Name)
        print(Zip)

        matches1 = df[df['Member Name'].str.contains(Name) & df['Member Address Line 3'].str.contains(Zip)]

        if len(matches1) == 1:
            row_index = matches1.iloc[0]['MRN']
            print("Match Found in DF1")
            print(row_index)

            memberI = str(row_index)

            os.rename(config.ManualCheck+filename, config.MRN+memberI+'.pdf')
            # os.rename(config.Total+filename, config.MRN+memberI)
        else:
            print("Match not Found in DF1")
            # print("No Match Found in DF1, Search Df2")
            # os.rename(config.Total+filename, config.ManualCheck+filename+'.pdf')
            # os.rename(config.Total+filename, config.ManualCheck+filename)
            matches2 = df2[df2['Member Name'].str.contains(Name) & df2['Member Address Line 3'].str.contains(Zip)]

            if len(matches2) == 1:
                row_index = matches2.iloc[0]['MRN']
                print("Match Found in DF2")
                print(row_index)

                memberI = str(row_index)

                # os.rename(config.ManualCheck+filename, config.MRN+memberI+'.pdf')
                os.rename(config.ManualCheck+filename, config.MRN+memberI+'.pdf')
            else: 
                print("Match not Found in DF2")
                # os.rename(config.Total+filename, config.ManualCheck+filename+'.pdf')
                os.rename(config.ManualCheck+filename, config.ManualCheck+filename)