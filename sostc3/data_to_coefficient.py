#!/usr/bin/env python

import os
import csv
from sys import argv


def calculate_and_dump(inputdir, outputdir):
    """For each CSV file in input dir, calculates it's data coefficient and generates an output file whith the result.
    Example of usage: $ data_to_coefficient.py <input_dir> <output_dir>"""
    # Get absolute paths, to avoid problems
    abs_input_dir = os.path.abspath(inputdir)
    abs_output_dir = os.path.abspath(outputdir)
    # For every CSV file in input dir
    for file in os.listdir(abs_input_dir):
        if file.endswith(".csv"):
            # Open both source (read-only) and result (write and truncate) CSV files
            with open(os.path.join(abs_input_dir, file)) as source_csv, \
                 open(os.path.join(abs_output_dir, file), 'w') as result_csv:
                # Create reader and writer
                source_reader = csv.reader(source_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                result_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Read the first line and write header row with coefficient column
                next(source_reader)
                result_writer.writerow(["lang", "timelapse", "coefficient"])

                # For each row, calculate coefficient and write along with the other columns
                for source_row in source_reader:
                    if len(source_row) >= 0:  # Ignore blank lines, if any

                        # q*5 + A*15 + (a-A)*10 + q_pv*5 + a_pv*10 - q_nv*2 - a_nv*2
                        coefficient = (int(source_row[2]) * 5) + \
                                      (int(source_row[3]) * 15) + \
                                      ((int(source_row[4]) - int(source_row[3])) * 10) + \
                                      (int(source_row[5]) * 5) + \
                                      (int(source_row[6]) * 10) - \
                                      (int(source_row[7]) * 2) - \
                                      (int(source_row[8]) * 2)
                        # Append coefficient column and write along with the other columns
                        result_writer.writerow([source_row[0], source_row[1], coefficient])

if __name__ == "__main__":
    if len(argv) != 3 or argv[1] == "--help" or argv[1] == "-h":
        print(calculate_and_dump.__doc__)
    else:
        calculate_and_dump(argv[1], argv[2])
