import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import dask.dataframe as dd


path = '/data/boulder-data/'
df = dd.read_csv(path+'cleaned-*.csv')




