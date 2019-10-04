import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import config
import xlrd
import numpy as np
import pandas as pd
import math
import os

for filename in os.listdir(config.ManualCheck):
    if filename.endswith(".pdf"):
        First_Name, Last_Name, Zip = filename.replace(".pdf",'').split()
        Name = First_Name + " " + Last_Name
        
        print(Name)
        print(Zip)

        data1 = pd.read_excel(config.Excel1)

        df = pd.DataFrame(data1)
        header = df.iloc[0]

        df = df[1:]
        df.rename(columns = header)
      
        row_numberd1 = df[df['Member Name'].str.contains(Name)].index.min()
        row_numberd12 = df[df['Member Address Line 3'].str.contains(Zip)].index.min()

        if row_numberd1 == row_numberd12: # When rows match of NameUp and Zip var in DF1
            rowMatched = row_numberd1
            print("Match Found in DF1")
            print(rowMatched)

            MemberID = df['MRN'][rowMatched]
            MemberI = str(MemberID)

            os.rename(config.ManualCheck+filename, config.Total+MemberI+'.pdf')

        else:
            print("No matching rows found in DF1 for Name and Zip")

            data2 = pd.read_excel(config.Excel2)
            df2 = pd.DataFrame(data2)
            header2 = df2.iloc[0]

            df2 = df2[1:]
            df2.rename(columns = header2)

            row_numberd2 = df2[df2['Member Name'].str.contains(Name)].index.min()
            row_numberd22 = df2[df2['Member Address Line 3'].str.contains(Zip)].index.min()

            if row_numberd2 == row_numberd22: # When rows match of NameUp and Zip var in DF2
                rowMatched2 = row_numberd1

                row_numberd1 = df2[df['Member Name'].str.contains(Name)].index.min()
                row_numberd12 = df2[df['Member Address Line 3'].str.contains(Zip)].index.min()


                os.rename(config.ManualCheck+filename, config.Total+MemberI+'.pdf')

