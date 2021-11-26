from subprocess import call
import os
import requests
import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError
from datetime import datetime
from copy import deepcopy

SOURCES = ['NOAA', 'CPC']
PID = os.getpid()
TMP_FILE_PATH = os.environ['HOME'] + f'/temp_file_climIndices_{PID}.txt'


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
        if 'nina' in index:
            base_url = 'https://psl.noaa.gov/data/correlation/{index}.anom.data'
        else:
            base_url = 'https://psl.noaa.gov/data/correlation/{index}.data'
    elif source == 'CPC':
        base_url = 'https://www.cpc.ncep.noaa.gov/data/indices/req{index}.for'
    else:
        raise ValueError("Source not supported")

    base_url = base_url.format(index=index)

    return base_url


def format_data(df, index, string_nan):
    colnames=['year']
    [colnames.append(i) for i in range(1,13)]
    df.columns = colnames
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
    def download_df(index, source):
        URL = create_url(index, source)
        if not exists(URL):
            print(URL)
            raise ValueError(f"URL does not exist for index {index}")

        call(["curl", "-s", "-o", TMP_FILE_PATH, URL], stdout=open(os.devnull, 'wb'))

    assert source in SOURCES, f'source {source} not valid.'
    _sources = deepcopy(SOURCES)
    df_list = []

    def format_datetime(x):
        return pd.Timestamp(datetime(day=1, month=x.month, year=x.year))

    for index in indices:
        for source in _sources:
            print(f'Trying source {source}')
            download_df(index, source)

            try:
                df_temp = pd.read_csv(TMP_FILE_PATH, sep='\s+', skiprows=[0], header=None)
            except EmptyDataError:
                print("Data is empty, trying another source")
            else:
                break
        try:
            df_temp
        except NameError:
            raise Exception(f'ClimIndices could not download index {index}')
        try:
            call(['rm', TMP_FILE_PATH])
        except:
            print('Could not remove temp file.')
        if source == 'CPC':
            string_nan = '999.9'
        else:
            df_nan = df_temp[df_temp.isnull().any(1)]
            string_nan = df_nan.iloc[0,0]
        df = df_temp.dropna()
        df = format_data(df, index, string_nan)
        df.index = [format_datetime(x) for x in df.index]
        df_list.append(df)

    df = pd.concat(df_list, axis=1)
    return df


if __name__=='__main__':
    import matplotlib.pyplot as plt
    plt.style.use('bmh')
    df = get_data(['nina34', 'soi'])
    # df.plot(subplots=True, sharex=True, title='Climate indices', legend='False', figsize=[10, 10])
    # plt.savefig('../figs/example.png')
    # plt.close()