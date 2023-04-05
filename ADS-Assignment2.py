import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import stats
import scipy.stats as sc


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

df_compare_brazil_features = df_brazil[["CO2 emissions from liquid fuel"
                                        r" consumption (kt)",
                                        "Urban population (% of total"
                                        r" population)",
                                        "Agricultural land (sq. km)",
                                        "Agriculture, forestry, and fishing,"
                                        r" value added (% of GDP)",
                                        "Foreign direct investment,"
                                        r" net inflows (% of GDP)"]]

# Statistics
df_compare_brazil_features.describe()

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

corr_matrix = df_compare_brazil_features.corr()
plt.figure(figsize = (8, 5))
ax = sns.heatmap(corr_matrix, annot = True)
ax.set_title('Brazil', fontdict = {'fontsize': 12}, pad = 12)
ax.set(xlabel = "", ylabel = "")

indicator = "Population in urban agglomerations of more than 1 million (% of total population)"
countries = ['Brazil', 'India', 'United States', 'South Africa']
urban_agglo = year_data[year_data['Indicator Name'].isin([indicator])]

urban_agglo = urban_agglo[urban_agglo['Country Name'].isin(countries)]
urban_agglo_t = urban_agglo.T

#urban_agglo.plot(x='Country Name',
##        kind='bar',
#        stacked=False,
#        title='Urban Population')


