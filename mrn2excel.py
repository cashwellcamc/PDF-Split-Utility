import re
import config
import xlrd
import math
import os, csv

with open(config.CSV, 'w+', newline='') as f:
    writer = csv.writer(f)
    for path, dirs, files in os.walk(config.MRN):
        for filename in files:
            writer.writerow([filename])

