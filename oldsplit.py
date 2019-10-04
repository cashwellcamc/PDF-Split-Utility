import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import config
import xlrd
import numpy as np
import pandas as pd
import math

with open(config.ENCRYPTED_FILE_PATH, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        if reader.isEncrypted:
            reader.decrypt('VPHP061419')
            print(f"Number of page: {reader.getNumPages()}")

            data1 = pd.read_excel(config.Excel1)
            data2 = pd.read_excel(config.Excel2)

            df = pd.DataFrame(data1)
            header = df.iloc[0]
            df2 = pd.DataFrame(data2)
            header2 = df2.iloc[0]

            df = df[1:]
            df.rename(columns = header)
            df2 = df2[1:]
            df2.rename(columns = header2)
            
            try:
                for i in range(reader.numPages):

                    output = PdfFileWriter()
                    output.addPage(reader.getPage(i))  

                    pageObj = reader.getPage(i)
                    page_content = pageObj.extractText()
                    # .encode('ascii', 'ignore')
                    clean_content = re.sub(r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])|(?<=[a-z])(?=[A-Z])', ' ', page_content)
                    last_rinse = clean_content.encode('ascii', 'ignore')

                    find_name = ' '.join(clean_content.split(' ')[0:2])
                    NameUp = find_name.upper()

                    zip_code = re.search(r'(?:[^\d]|^)(\d{5}\-\d{4})(?:[^\d]|$)', clean_content)
                    Zip = zip_code.group(0)[:6]

                    try:
                        # Check DF 1 for matching NameUp and Zip vars
                        # if row_numberd1:
                        row_numberd1 = df[df['Member Name'].str.contains(NameUp)].index.min()
                        print ("Member Name found in df 1 Excel")
                        row_numberd12 = df[df['Member Address Line 3'].str.contains(Zip)].index.min()
                        print ("Member Zip found in df 1 Excels")
                        print (row_numberd1 + row_numberd12)
                        if row_numberd1 == row_numberd12: # When rows match of NameUp and Zip var in DF1
                            rowMatched = row_numberd1
                            print("Match Found")
                            print(rowMatched)

                            MemberID = df['MRN'][rowMatched]
                            MemberI = str(MemberID)

                            with open("./pdfs/" + MemberI + ".pdf", "wb") as outputStream:
                                output.write(outputStream)
                        else:
                            print("No matching rows found in DF1 for Name and Zip")

                            # Now Check DF 2 for matching NameUp and Zip vars
                            row_numberd2 = df2[df2['Member Name'].str.contains(NameUp)].index.min()
                            print ("Member Name found in df 2 Excels")
                            row_numberd22 = df2[df2['Member Address Line 3'].str.contains(Zip)].index.min()
                            print ("Member Zip found in df 2 Excels")
                            print (row_numberd2 + row_numberd22)

                            if row_numberd2 == row_numberd22: # When rows match of NameUp and Zip var in DF2
                                rowMatched2 = row_numberd2
                                print("No Match Found")
                                print(rowMatched2)

                                MemberID = df2['MRN'][rowMatched2]
                                MemberI = str(MemberID)

                                with open("./pdfs/" + MemberI + ".pdf", "wb") as outputStream:
                                    output.write(outputStream)
                            else:
                                print("Match Not Found in Both DFs")
                                FailedLas = NameUp.replace(NameUp[:5], '')
                                with open("./pdfs/ManualCheck/" + FailedLas + ".pdf", "wb") as outputStream:
                                    output.write(outputStream)
                                    
                    except:
                        print("No matching rows found in DF2 for Name and Zip")

            except:
                print("Exception")
                raise
