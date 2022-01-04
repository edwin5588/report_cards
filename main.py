import sys
import pandas as pd
import numpy as np
import json
import os



def csv_to_pd(fp, csv_name):
    """
    converts CSV to a pandas dataframe object

    """

    df = pd.read_csv(fp)
    df.columns = [csv_name+ "_" +column for column in df.columns]
    return df


if __name__ == "__main__":

    arguments = sys.argv

    print(csv_to_pd(os.path.join('testdata', 'students.csv'), 'students'))
    print(csv_to_pd(os.path.join('testdata', 'courses.csv'), 'courses'))
    print(csv_to_pd(os.path.join('testdata', 'marks.csv'), 'marks'))
    print(csv_to_pd(os.path.join('testdata', 'tests.csv'), 'tests'))
