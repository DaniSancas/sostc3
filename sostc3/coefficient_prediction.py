#!/usr/bin/env python

import os
import pandas
from sys import argv
from numpy import polyfit
from numpy import poly1d
from numpy import arange


def year_month_iter(start_year, start_month, end_year, end_month):
    """Timelapse (year-month) iterator."""
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end + 1):
        y, m = divmod(ym, 12)
        yield "{}-{}".format(y, str(m+1).zfill(2))


def months_to_predict(number_of_months, last_timelapse):
    """Given the last timelapse and a number of months, outputs the next timelapse values."""
    default_year, default_month = [int(x) for x in last_timelapse.split("-")]

    start_year = int(default_month / 12) + default_year
    start_month = int(default_month % 12) + 1
    end_year = int((number_of_months + start_month - 1) / 12) + start_year
    end_month = int((number_of_months + start_month - 1) % 12)

    return start_year, start_month, end_year, end_month


def predict_and_dump(inputdir, outputdir, number_of_months=3):
    """For each CSV file in input dir, takes it's data coefficient and predicts the next months coefficient.
    The result data is the real data along with the predicted data.
    Example of usage: $ coefficient_prediction.py <input_dir> <output_dir> [<number_of_months>]"""
    # Get absolute paths, to avoid problems
    abs_input_dir = os.path.abspath(inputdir)
    abs_output_dir = os.path.abspath(outputdir)

    # For every CSV file in input dir
    for lang_csv in os.listdir(abs_input_dir):
        if lang_csv.endswith(".csv"):
            # Read CSV file and make a DataFrame with it's data
            lang_df = pandas.read_csv(os.path.join(abs_input_dir, lang_csv))

            x_axis = lang_df.index  # Index numbers
            y_axis = lang_df['coefficient'].tolist()  # Coefficient numbers
            lang_poly = polyfit(x_axis, y_axis, 4)  # 4rd-grade polynomial regression

            poly_line = poly1d(lang_poly)  # Polynomial line
            future_months = arange(number_of_months) + len(lang_df.index)  # Ten more months
            future_coefficient = poly_line(future_months)  # Get the coefficient prediction for the next X months

            last_timelapse = lang_df['timelapse'][len(lang_df.index)-1]  # Get last timelapse from timeseries
            timelapse_range = months_to_predict(number_of_months, last_timelapse)  # List of timelapses to predict
            timelapse_iterator = year_month_iter(
                timelapse_range[0], timelapse_range[1], timelapse_range[2], timelapse_range[3])

            # Add predicted data to the timeseries (bottom of CSV file)
            coefficient_index = 0
            for timelapse in timelapse_iterator:
                lang_df.loc[len(lang_df.index)] = \
                    [os.path.splitext(lang_csv)[0], timelapse, int(future_coefficient[coefficient_index])]
                coefficient_index += 1

            # Save the real data along with predicted data in a CSV file, overwriting it if exists
            lang_df.to_csv(os.path.join(abs_output_dir, lang_csv), index=False, float_format='%.0f')


if __name__ == "__main__":
    if len(argv) not in (3, 4) or argv[1] == "--help" or argv[1] == "-h":
        print(predict_and_dump.__doc__)
    elif len(argv) == 4:
        predict_and_dump(argv[1], argv[2], argv[3])
    else:
        predict_and_dump(argv[1], argv[2])
