import datetime
from subprocess import call
import os
import sys
import requests
import numpy as np
import pandas as pd

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def exists(URL):
    r = requests.head(URL)
    return r.status_code == requests.codes.ok

def create_url(index, source):
    """
    Return the valid URL for download

    :param variable: string
    :param level: string
    :param date: datetime
    :return: sring
    """
    if source == 'NOAA':
        base_url = 'https://www.esrl.noaa.gov/psd/data/correlation/{index}.data'

    else:
        raise ValueError("Source not supported")

    base_url = base_url.format(index=index)

    return base_url

def get_data(index, source = 'NOAA'):
    URL = create_url(index, source)

    if not exists(URL):
        print(URL)
        raise ValueError("This URL does not exist")


    call(["curl","-s", "-o", 'temp.txt', URL], stdout=open(os.devnull, 'wb'))
    flen = file_len('temp.txt')
    df = pd.read_csv('temp.txt',sep='\s+', skiprows=[0,flen-1])
    call(['rm', 'temp.txt'])
    df = format_data(df)
    return df


def format_data(df):
    colnames=['year']
    [colnames.append(i) for i in range(1,13)]
    df.columns=colnames
    df = df.set_index('year')
    df = df.unstack()
    df = df.reset_index()
    df.columns = ['month','year','value']
    df = df.sort_values(['year','month'])
    df = df.replace('-99.99', np.NaN)
    df = df.dropna()

    print(df)
    print('{year}-{month}-31'.format(year=df['year'].iloc[-1], month=df['month'].iloc[-1]))
    indexes = pd.date_range(start='{year}-{month}-01'.format(year=df['year'].iloc[0], month=df['month'].iloc[0]),
                            end='{year}-{month}-31'.format(year=df['year'].iloc[-1], month=df['month'].iloc[-1]),freq='M')
    print(indexes)
    df['time']=indexes
    df = df.set_index(time)
    df=df.dropna()
    return df

if __name__=='__main__':
    df = get_data('nina34')
    print(df)
