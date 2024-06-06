import argparse
import os
import pandas as pd
import numpy as np


def clean_data(country):

    data=pd.read_csv("life_expectancy/data/eu_life_expectancy_raw.tsv",sep='\t', header=0)

    data[['unit', 'sex', 'age','region']]=data['unit,sex,age,geo\\time'].str.split(',', expand=True)
    data = data.drop(['unit,sex,age,geo\\time'], axis=1)

    var_columns = data.iloc[:, 62:66]
    var_values = data.iloc[:, :62]
    data_long = pd.melt(data, id_vars=var_columns, value_vars=var_values,
                        var_name='year', value_name='value')

    data_long['year'].replace([np.inf, -np.inf], np.nan, inplace=True)
    data_long.dropna(subset=['year'], inplace=True)

    data_long['value'] = data_long['value'].str.replace('e', '')
    data_long = data_long[data_long['year'] != 'unit']

    data_long['year'] = pd.to_numeric(data_long['year'], errors='coerce').astype('int')
    data_long['value'] = pd.to_numeric(data_long['value'], errors='coerce').astype('float')
    data_long.dropna(subset=['value'], inplace=True)

    data_pt = data_long[data_long['region'] == 'PT']
    new_directory = os.path.join('life_expectancy/data', 'pt_life_expectancy.csv')
    data_pt.to_csv(new_directory, index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", default="PT", help="Country code to filter the data")
    args = parser.parse_args()
    clean_data(args.country)
