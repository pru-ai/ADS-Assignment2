import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import stats
from matplotlib.ticker import FuncFormatter


def read_csv(filename):
    """
    Read CSV file and extract dataframe as per country and year with
    indexes configures as required.

    Parameters:
    filename (String): Name of the CSV file

    Returns:
    Two Dataframes containing Year wise data and Country wise data
    respectively.
    """
    df = pd.read_csv(filename, skiprows=4)
    df.drop(columns = ['Country Code', 'Indicator Code', 'Unnamed: 66'],
            inplace = True)
    country_data = df.set_index('Country Name').T
    year_data = df.set_index('Country Name').reset_index()
    return year_data, country_data


year_data, country_data = read_csv('WorldBank.csv')


def country_wise_data(countryname):
    df = country_data[countryname]
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric)
    df.dropna(thresh = round(len(df) * 0.75), axis = 1, inplace = True)
    return df


df_brazil = country_wise_data("Brazil")
df_india = country_wise_data("India")
df_usa = country_wise_data("United States")
df_sa = country_wise_data("South Africa")

# Statistics
df_brazil.describe()
df_india.describe()
df_usa.describe()
df_sa.describe()

br_low, br_high = stats.bootstrap(df_brazil["Urban population"
                                            " (% of total population)"],
                                  np.mean)

in_low, in_high = stats.bootstrap(df_india["Urban population"
                                           " (% of total population)"],
                                  np.mean)

us_low, us_high = stats.bootstrap(df_usa["Urban population"
                                         " (% of total population)"],
                                  np.mean)

sa_low, sa_high = stats.bootstrap(df_sa["Urban population"
                                        " (% of total population)"],
                                  np.mean)

country_urban_pop_interval = {'Brazil': (br_low, br_high),
                              'India': (in_low, in_high),
                              'USA': (us_low, us_high),
                              'South Africa': (sa_low, sa_high)}

print(country_urban_pop_interval)


indicators = ["CO2 emissions from liquid fuel consumption (kt)",
              "Urban population (% of total population)",
              "Agricultural land (sq. km)",
              "Agriculture, forestry, and fishing, value added (% of GDP)",
              "Foreign direct investment, net inflows (% of GDP)"]


def heat_map(country):
    df_features = country_wise_data(country)[indicators]
    corr_matrix = df_features.corr()
    plt.figure(figsize = (8, 5))
    ax = sns.heatmap(corr_matrix, annot = True)
    ax.set_title(country, fontdict = {'fontsize': 12}, pad = 12)
    ax.set(xlabel = "", ylabel = "")
    return


heat_map("Brazil")
heat_map("India")
heat_map("South Africa")


cntrys = ['Brazil', 'India', 'United States', 'South Africa']


def convert_to_millions(num):
    'The two args are the value and tick position'
    return '%1.1fM' % (num * 1e-6)


def time_series(indicator):
    df_agg = year_data[year_data['Indicator Name'].isin([indicator])]
    df_agg = df_agg[df_agg['Country Name'].isin(cntrys)].reset_index(drop=True)
    df_agg_t = df_agg.T
    df_agg_t = df_agg_t.drop('Indicator Name')
    df_agg_t.columns = df_agg_t.iloc[0]
    df_agg_t = df_agg_t.iloc[1:]
    df_agg_t.index = pd.to_datetime(df_agg_t.index)
    formatter = FuncFormatter(convert_to_millions)
    fig, ax = plt.subplots(figsize = (16, 9))
    ax.yaxis.set_major_formatter(formatter)
    ax.plot(df_agg_t)
    ax.legend(df_agg_t.columns)
    ax.set_title(indicator)
    return


time_series("Urban population")
time_series("CO2 emissions from liquid fuel consumption (kt)")
