import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_csv(filename):
    """
    Reads data from a CSV file containing World Bank data on renewable energy
    consumption as a percentage of total final energy consumption
    for all countries.

    Parameters:
    filename (str): The name of the CSV file containing the data.

    Returns:
    tuple: A tuple containing two pandas DataFrames. The first DataFrame is a
    year-based DataFrame with each column representing a country and each row
    representing a year. The second DataFrame is a country-based DataFrame with
    each row representing a country and each column representing a year.
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
corr_matrix = df_compare_brazil_features.corr()
plt.figure(figsize = (8, 5))
ax = sns.heatmap(corr_matrix, annot = True)
ax.set_title('Brazil', fontdict = {'fontsize': 12}, pad = 12)
ax.set(xlabel = "", ylabel = "")
