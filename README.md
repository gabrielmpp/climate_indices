# climate_indices

Tools to download climate indices from NOAA (soi, qbo, pna etc) and format as Pandas dataframe.

## Installation 

>> pip install git+https://github.com/gabrielmpp/climate_indices

## Usage 

>> import climIndices as ci

>> import matplotlib.pyplot as plt

>> df = get_data(['nina34', 'oni', 'nao', 'qbo'])

>> df.plot(subplots=True, sharex=True, title='Climate indices', legend='False', figsize=[10, 10])

>> plt.show()

<img src="https://github.com/gabrielmpp/climate_indices/blob/master/figs/example.png?raw=true" width="500">
