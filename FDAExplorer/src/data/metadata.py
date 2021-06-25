import pandas as pd
import numpy as np
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

root_path = '../data/raw/legacy'
paths = ['data_1978_1980.txt', 'data_1981_1985.txt',  'data_1986_1990.txt', 'data_1991_1995.txt'] #, 'data_1996_curr.txt']

def build_df(clean = False, convert_dt = True):
    """Builds DF of metadata from FDA 510(k) applications

    This function builds a dataframe that displays all the metadata on 510(k) applications from 1976 to 1995.The more recent
    metadata will need different functionality because it needs to be continuously refreshed.


    Args:
        clean: (bool, default = False)  Not yet implemented. If true, will do some basic cleaning like removing NaNs before returning
        convert_dt: (bool, default =True) If true, date columns will bec converted to datetime objects.

    Returns:
        pandas.DataFrame: returns a pandas DataFrame containing metadata on all applications for 510(k) for medical devices from 1976 to 1995 with the following columns: ['KNUMBER', 'APPLICANT', 'CONTACT', 'STREET1', 'STREET2', 'CITY', 'STATE', 'COUNTRY_CODE', 'ZIP', 'POSTAL_CODE', 'DATERECEIVED', DECISIONDATE', 'DECISION', 'REVIEWADVISECOMM', 'PRODUCTCODE', 'STATEORSUMM', 'CLASSADVISECOMM', 'SSPINDICATOR', 'TYPE', 'THIRDPARTY', 'EXPEDITEDREVIEW', 'DEVICENAME']

    Raises:
        Error: Probably means file wasn't found. Did you run ./get_legacy_data.sh in the data/raw directory?


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

def find_pdf(k_number):
    """Finds the URL for a PDF summary for a k_number

    This function will take a k_number you provide and look on the FDA site to try to find a summary
    pdf to go along with it. If it finds a summary pdf it will return the link to it.

    Args:
        k_number: (str) the string of the k_number of the document you are looking for

    Returns:
        str:  url of the link to the pdf if found

    Raises:
        ValueError: This will raise an error if the k_number provided doesn't have a url associated with
                                    it on the FDA website
         Error: This will be thrown if the site doensn't have an associated summary document with it

    """


    root_url = 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={}'
    response = requests.get(root_url.format(k_number))
    soup = BeautifulSoup(response.text)


    for x in soup.findAll('tr'):
        th= x.findNext('th')
        th_text = th.text.replace('\n', '').replace('\t', '')
        td = x.findNext('td')
        if th_text == 'summary':
            pdf_link = td.findNext('a', href=True)['href']
            return pdf_link

    raise Exception("Could not find PDF. This probably means that this application was submitted without a summary or that the robot killer finally found me. ")


def fetch_summary_pdf(k_number, save_location='data/raw/pdf'):
    """Downloads a pdf of a summary given a k_number

    Fetches a pdf given a k number and saves it to a given directory. Note that many of these applications
    don't hav e summaries associated with them (especially the older ones.) If you enter a k_number value
    that doesn't have a summary this will raise an error.

    Args:
        k_number: (str) The k number of the document. This is the number that the FDA uses to identify these docs
        save_location: ( str, pathlike, default = data/raw/pdf')= The directory you want to save this in

    Returns:
        save_path (str) the filepath where the file was saved

    Raises:
        Exception: If there is no pdf accoiated with the k_number or the k_number cannot be found

    """
    try:
        url = find_pdf(k_number)
    except:
        raise FileExistsError("Could not retrive URL of pdf for accosiated k_number. It probably just doesn't exist")

    response = requests.get(url)
    filepath = "{}.pdf".format(k_number)
    save_path = os.path.join(save_location, filepath)
    with open(save_path, 'wb') as pdf:
        pdf.write(response.content)
    return save_path