#!/usr/bin/env python

"""
This script is used to re-evaluate the concentration of protists after manual
reclassification of pre-classified images. 

Execute the script inside the 'Output' directory. 
"""

import os
from datetime import datetime

try:
    with open('report.txt', 'r') as file:
        lines = file.readlines()
        # Fetch the last line containing the sample data
        last_line = lines[-1]
        # Split the last line by tab to get the values
        last_line_parts = last_line.split()
        sample = last_line_parts[0]
        volume_imaged = float(last_line_parts[1])
        
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
count_protist = len(os.listdir('Predicted_images/Protist'))
count_missed = len(os.listdir('Predicted_images/Missed'))
count_junk = len(os.listdir('Predicted_images/Junk'))
volume_imaged = float(volume_imaged)

text_to_append = [
    "\n---------------------------------------------------------------",
    f"Manual reclassification \t ({current_time})",
    "\nCategories",
    f"Junk: {count_junk}",
    f"Missed: {count_missed}",
    f"Protist: {count_protist}",
    f"\nEstimated conc. (protists/ml): {count_protist/volume_imaged:.2f}",
    f"\n{sample}\t{volume_imaged}\t{count_junk}\t{count_missed}\t{count_protist}\t{count_protist / volume_imaged:.2f}"
]

with open('report.txt', 'a') as file:
    for line in text_to_append:
        file.write(line + '\n')
        print(line)

