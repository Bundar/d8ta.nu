import altair as alt
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import dask.dataframe as dd


path = '/data/boulder-data/'
df = dd.read_csv(path+'cleaned-*.csv')
print("Columns: " + str(df.columns))

data = df
chart = alt.Chart(data)

alt.Chart(data).mark_point().encode(
	x='BMI',
	y='Score'
)
