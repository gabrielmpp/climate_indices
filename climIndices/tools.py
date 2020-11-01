from subprocess import call
import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime

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
        base_url = 'https://psl.noaa.gov/data/correlation/{index}.data'

    else:
        raise ValueError("Source not supported")

    base_url = base_url.format(index=index)

    return base_url


def format_data(df, index, string_nan):
    colnames=['year']
    [colnames.append(i) for i in range(1,13)]
    df.columns=colnames
    df = df.set_index('year')
    df = df.unstack()
    df = df.reset_index()
    df.columns = ['month','year','value']
    df = df.sort_values(['year','month'])
    #df = df.replace('-99.99', np.NaN)
    #df = df.dropna()

    indexes = pd.date_range(start='{year:0d}-{month}-01'.format(year=int(df['year'].iloc[0]), month=int(df['month'].iloc[0])),
                            end='{year:0d}-{month}-31'.format(year=int(df['year'].iloc[-1]), month=int(df['month'].iloc[-1])),freq='M')
    df['time']=indexes
    df = df.set_index('time')
    df = df.drop(['month','year'], axis=1)
    df.columns = [index]
    df[index] = df[index].astype(float)
    df = df.replace(float(string_nan), np.NaN)

    df = df.dropna()
    return df


def get_data(indices, source='NOAA'):
    df_list = []

    def format_datetime(x):
        return pd.Timestamp(datetime(day=1, month=x.month, year=x.year))

    for index in indices:
        URL = create_url(index, source)
        if not exists(URL):
            print(URL)
            raise ValueError(f"URL does not exist for index {index}")

        call(["curl", "-s", "-o", 'temp.txt', URL], stdout=open(os.devnull, 'wb'))
        df = pd.read_csv('temp.txt', sep='\s+', skiprows=[0], header=None)
        try:
            call(['rm', 'temp.txt'])
        except:
            print('Could not remove temp file.')
        df_nan = df[df.isnull().any(1)]
        string_nan = df_nan.iloc[0,0]
        df = df.dropna()
        df = format_data(df, index, string_nan)
        df.index = [format_datetime(x) for x in df.index]
        df_list.append(df)

    df = pd.concat(df_list, axis=1)
    return df


if __name__=='__main__':
    import matplotlib.pyplot as plt
    plt.style.use('bmh')
    df = get_data(['nina34', 'oni', 'nao', 'qbo'])
    df.plot(subplots=True, sharex=True, title='Climate indices', legend='False', figsize=[10, 10])
    plt.savefig('../figs/example.png')
    plt.close()