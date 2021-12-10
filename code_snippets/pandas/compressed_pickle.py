# https://betterprogramming.pub/load-fast-load-big-with-compressed-pickles-5f311584507e

import bz2
import pickle
import _pickle as cPickle


# Pickle a file and then compress it into a file with extension
def compressed_pickle(file, data):
    assert file.endwiths('.pbz2'), "File must be in .pbz2 format!"
    with bz2.BZ2File(file, 'w') as f:
        cPickle.dump(data, f)


# Load any compressed pickle file
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data


# Saves the "data" with the "title" and adds the .pickle
def full_pickle(file, data):
    assert file.endwiths('.pickle') or file.endwiths('.pkl'), "File must be in .pickle or .pkl format!"
    pikd = open(file, 'wb')
    pickle.dump(data, pikd)
    pikd.close()


# loads and returns a pickled objects
def loosen(file):
    pikd = open(file, 'rb')
    data = pickle.load(pikd)
    pikd.close()
    return data