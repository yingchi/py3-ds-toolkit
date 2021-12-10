import pandas as pd
from typing import List


def optimize_floats(df: pd.DataFrame) -> pd.DataFrame:
    floats = df.select_dtypes(include=['float64']).columns.tolist()
    df[floats] = df[floats].apply(pd.to_numeric, downcast='float')
    return df


def optimize_ints(df: pd.DataFrame) -> pd.DataFrame:
    ints = df.select_dtypes(include=['int64']).columns.tolist()
    df[ints] = df[ints].apply(pd.to_numeric, downcast='integer')
    return df


def optimize_objects(df: pd.DataFrame, datetime_features: List[str]) -> pd.DataFrame:
    for col in df.select_dtypes(include=['object']):
        if col not in datetime_features:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if float(num_unique_values) / num_total_values < 0.5:
                df[col] = df[col].astype('category')
        else:
            df[col] = pd.to_datetime(df[col])
    return df


def optimize(df: pd.DataFrame, datetime_features: List[str] = []):
    return optimize_floats(optimize_ints(optimize_objects(df, datetime_features)))


# example usage: optimized_listings = optimize(example_df, ['apply_date'])

from sklearn.datasets import load_iris
import pandas as pd

X, y = load_iris(as_frame=True, return_X_y=True)
df = pd.concat([X, pd.DataFrame(y, columns=['target'])], axis=1)
print(df.memory_usage())
""" 
Index                 128
sepal length (cm)    1200
sepal width (cm)     1200
petal length (cm)    1200
petal width (cm)     1200
target               1200
dtype: int64
"""
df['target'] = df['target'].astype('category')
print(df.memory_usage())
""" 
Index                 128
sepal length (cm)    1200
sepal width (cm)     1200
petal length (cm)    1200
petal width (cm)     1200
target                282
dtype: int64
"""