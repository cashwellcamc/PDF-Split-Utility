import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import config
import xlrd
import numpy as np
import pandas as pd
import math
import os

with open(config.ENCRYPTED_FILE_PATH, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        if reader.isEncrypted:
            reader.decrypt('VPHP061419')
        #     print(f"Number of page: {reader.getNumPages()}")

            for i in range(reader.numPages):

                    output = PdfFileWriter()
                    output.addPage(reader.getPage(i))  

                    pageObj = reader.getPage(i)
                    page_content = pageObj.extractText()
                    print(page_content)
                    clean_content = re.sub(r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])|(?<=[a-z])(?=[A-Z])', ' ', page_content)
                    #  last_rinse = clean_content.encode('ascii', 'ignore')
                    print(clean_content)
                    s = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", clean_content)
                    print(s)

                    find_name = ' '.join(s.split(' ')[0:2])

                    if find_name:
                        NameUp = find_name.upper()

                        if NameUp:
                                NameClean = NameUp.replace("/", "")
                                NameCleanR = NameClean.replace("---", "")
                                NameCleanST = NameCleanR.replace("\n90", "")
                                NameNothing = NameCleanST.replace("#", "")
                                NameNada = NameCleanST.replace("%", "")

                                zip_code = re.search(r'(?:[^\d]|^)(\d{5}\-\d{4})(?:[^\d]|$)', clean_content)
                                zip_trail = re.search(r'(?<=,\s[A-Z]{2}\s)\d{5}\b', clean_content)

                                if zip_code:
                                        Zip = zip_code.group(0)[:6]
                                        zip_dash = Zip.replace("-","")

                                        print (NameNada)
                                        print(Zip)
                                        with open("./pdfs/TOTAL/" + NameNada + " " + zip_dash + ".pdf", "wb") as outputStream:
                                                output.write(outputStream)

                                else:
                                        if zip_trail:
                                                zip_traild = zip_trail.group()

                                                with open("./pdfs/TOTAL/ChkZip/" + NameNada + " " + zip_traild + ".pdf", "wb") as outputStream:
                                                        output.write(outputStream)
                                        else:
                                                with open("./pdfs/TOTAL/ChkZip/document-page%s.pdf" % i, "wb") as outputStream:
                                                        output.write(outputStream)

