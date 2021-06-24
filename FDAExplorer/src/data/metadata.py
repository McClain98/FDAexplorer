import pandas as pd
import numpy as np
import os
from datetime import datetime

root_path = '../data/raw/legacy'
paths = ['data_1978_1980.txt', 'data_1981_1985.txt',  'data_1986_1990.txt', 'data_1991_1995.txt'] #, 'data_1996_curr.txt']

def build_df(clean = False, convert_dt = True):
    """
   This function builds a dataframe that displays all the metadata on 510(k) applications from 1976 to 1995.
    The more recent metadata will need different functionality because it needs to be continuously refreshed.

    Args:
        clean: (bool, default=False) Not yet implemented. If true, will do some basic cleaning like removing NaNs before returning
        convert_dt: (bool, default=True) If true, date columns will bec onverted to datetime objects.

    Returns:
         returns a pandas DataFrame containing metadata on all applications for 510(k) for medical devices from 1976 to 1995 with
         the following columns: ['KNUMBER', 'APPLICANT', 'CONTACT', 'STREET1', 'STREET2', 'CITY',
       'STATE', 'COUNTRY_CODE', 'ZIP', 'POSTAL_CODE', 'DATERECEIVED',
       'DECISIONDATE', 'DECISION', 'REVIEWADVISECOMM', 'PRODUCTCODE',
       'STATEORSUMM', 'CLASSADVISECOMM', 'SSPINDICATOR', 'TYPE', 'THIRDPARTY',
       'EXPEDITEDREVIEW', 'DEVICENAME']

    Raises:
        Exception: Probably means file wasn't found. Did you run ./get_legacy_data.sh in the data/raw directory?
    """

    dfs = []
    for file in paths:
        f = os.path.join(root_path, file)
        try:
            df = pd.read_csv(f, sep='|')
        except:
            raise Exception("Could not read file. Make sure the files in data/raw/legacy exist. If not, run ./get_legacy_data.sh to fetch.")
        dfs.append(df)

    big_df = pd.concat(dfs)

    if clean:
        big_df = clean_df(big_df)

    if convert_dt:
        big_df['DATERECEIVED'] = pd.to_datetime(big_df['DATERECEIVED'])
        big_df['DECISIONDATE'] = pd.to_datetime(big_df['DECISIONDATE'])

    return big_df