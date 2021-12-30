import sys
import pandas as pd
import numpy as np
import json



def csv_to_pd(fp):
    """
    converts CSV to a pandas dataframe object

    """
    return None
if __name__ == "__main__":

    arguments = sys.argv
    dummy, courses_csv, students_csv, tests_csv, marks_csv, output_json = arguments
    for argument in arguments:
        print(argument)
