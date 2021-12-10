# https://stackoverflow.com/questions/38231591/split-explode-a-column-of-dictionaries-into-separate-columns-with-pandas
import pandas as pd
from ast import literal_eval
import numpy as np

# Fastest
df.join(pd.DataFrame(df.pop('Pollutants').values.tolist()))
# use the above if there is no rows with Nan or nested dict


data = {'Station ID': [8809, 8810, 8811, 8812, 8813, 8814],
        'Pollutants': ['{"a": "46", "b": "3", "c": "12"}', '{"a": "36", "b": "5", "c": "8"}', '{"b": "2", "c": "7"}', '{"c": "11"}', '{"a": "82", "c": "15"}', np.nan]}

df = pd.DataFrame(data)

# display(df)
# Station ID                        Pollutants
# 0        8809  {"a": "46", "b": "3", "c": "12"}
# 1        8810   {"a": "36", "b": "5", "c": "8"}
# 2        8811              {"b": "2", "c": "7"}
# 3        8812                       {"c": "11"}
# 4        8813            {"a": "82", "c": "15"}
# 5        8814                               NaN

# replace NaN with '{}' if the column is strings, otherwise replace with {}
# df.Pollutants = df.Pollutants.fillna('{}')  # if the NaN is in a column of strings
df.Pollutants = df.Pollutants.fillna({i: {} for i in df.index})  # if the column is not strings

# Convert the column of stringified dicts to dicts
# skip this line, if the column contains dicts
df.Pollutants = df.Pollutants.apply(literal_eval)

# reset the index if the index is not unique integers from 0 to n-1
# df.reset_index(inplace=True)  # uncomment if needed

# normalize the column of dictionaries and join it to df
df = df.join(pd.json_normalize(df.Pollutants))

# drop Pollutants
df.drop(columns=['Pollutants'], inplace=True)

# display(df)
# Station ID    a    b    c
# 0        8809   46    3   12
# 1        8810   36    5    8
# 2        8811  NaN    2    7
# 3        8812  NaN  NaN   11
# 4        8813   82  NaN   15
# 5        8814  NaN  NaN  NaN