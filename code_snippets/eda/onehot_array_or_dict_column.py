import collections
import gc
import os

import numpy as np
import pandas as pd
from utils.compress_pickle import *

os.environ['NUMEXPR_MAX_THREADS'] = '16'


def onehot_list_variable(df, col, lowest_freq_cnt=0, top_n=0,
                         prefix="", encoder_path="", mode='train'):
    """
    When `model` == "test", then `encoder_output_path` must be provided, and
    `lowest_freq_cnt`, and `top_n` will not take effect.
    """
    assert mode in ("train", "test"), "Mode must be 'train' or 'test'"
    if mode == "test":
        assert encoder_path!="" and os.path.exists(encoder_path), "A valid encoder path must be provided!"
        encoded_fields = np.load(encoder_path)
        items_keep = [x.replace(prefix, "").strip("_") for x in encoded_fields]
    else:
        assert lowest_freq_cnt*top_n == 0, "Only either lowest_freq_cnt > 0 or top_n>0 but not both!"
        item_freqs = df[col].explode().value_counts()
        print("number of unique items:", len(item_freqs))
        if top_n > 0:
            items_keep = item_freqs[:top_n].values
        else:
            # filter out the classes with less than lowest_cnt counts
            items_keep = item_freqs.index[item_freqs >= lowest_freq_cnt].values

    print("number of kept items:",len(items_keep))
    df[col] = df[col].apply(lambda x: list(set(x) & set(items_keep)))
    df_out = df.join(
        pd.get_dummies(
            pd.DataFrame(df[col].tolist()).stack(),
            prefix=prefix).sum(level=0)
    )
    del df
    gc.collect()
    encoded_fields = [x for x in df_out.columns if x.startswith(prefix)]
    print("number of encoded items",len(encoded_fields))
    df_out[encoded_fields] = df_out[encoded_fields].fillna(0)
    try:
        df_out[encoded_fields] = df_out[encoded_fields].astype(int).apply(pd.to_numeric, downcast='integer')
    except:
        print("error downcast type, return the dataframe with float dtype")
        return df_out
    if mode == "train":
        np.save(encoder_path, encoded_fields)
    return df_out


def list_to_dict(lst, sep="_"):
    d = {}
    str_to_remove = 'This is an employer-written question. '+ \
                    'You can report inappropriate questions to Indeed through the "Report Job" link '+ \
                    'at the bottom of the job description. '
    for x in lst:
        i = x.split(sep)
        question = i[0].replace(str_to_remove, '').strip().strip('"')
        answer = i[1].strip()
        d[question] = answer
    return d


def explode_dict_field_to_columns(df, col, lowest_freq_cnt=0, top_n=0,
                                  prefix="", encoder_path="", mode='train'):
    """
    When `model` == "test", then `encoder_output_path` must be provided, and
    `lowest_freq_cnt`, and `top_n` will not take effect.
    """
    assert mode in ("train", "test"), "Mode must be 'train' or 'test'"
    if mode == "test":
        assert encoder_path!="" and os.path.exists(encoder_path), "A valid encoder path must be provided!"
        encoded_fields = np.load(encoder_path)
        keys_keep = set([x.replace(prefix, "").strip("_") for x in encoded_fields])
    else:
        assert lowest_cnt*top_n == 0, "Only either lowest_cnt > 0 or top_n>0 but not both!"
        items_lsts = [x.keys() for x in list(df[col].values)]
        items_lst = [item for lst in items_lsts for item in lst]
        items_cnt = collections.Counter(items_lst)
        print("total unique keys:", len(items_cnt))
        if top_n > 0:
            items_keep = items_cnt.most_common(top_n)
        else:
            items_keep = {x: count for x, count in items_cnt.items() if count >= lowest_freq_cnt}
        keys_keep = set(items_keep.keys())

    print("number of kept keys",len(keys_keep))
    df[col] = df[col].apply(lambda x: {k: v for k, v in x.items() if k in keys_keep})

    df_out = df.join(
        pd.DataFrame(df.pop(col).values.tolist(),dtype='category').add_prefix(prefix+"_"))
    del df
    gc.collect()
    encoded_fields = [x for x in df_out.columns if x.startswith(prefix)]
    print("number of encoded items" ,len(encoded_fields))

    if mode == "train":
        np.save(encoder_path, encoded_fields)
    return df_out


def check_item_freq_in_list_column(df, col, freq_to_check=[10, 50, 100, 500, 1000]):

    all_items_lists = list(df[col].values)
    check_item_freq_in_nested_list(all_items_lists)


def check_item_freq_in_nested_list(nested_list, freq_to_check=[10, 50, 100, 500, 1000]):
    all_items = [item for lst in nested_list for item in lst]
    items_cnt = collections.Counter(all_items)
    print("number of unique items:", len(items_cnt))
    print("number of total items:", sum(items_cnt.values()))
    print("least frequent 10 items:", items_cnt.most_common()[:-10:-1])
    print("number of unique items at different cnt threshold:")
    for cnt in freq_to_check:
        items_keep = {x: count for x, count in items_cnt.items() if count >= cnt}
        print(f"{cnt}: {len(items_keep)}")