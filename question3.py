# Pandas - allows to manipulate the data easily
import pandas as pd
print("Pandas imported!")
import numpy as np
import matplotlib.pyplot as plot

vaccinations_df = pd.read_csv("vaccinations.csv")
result=pd.pivot_table(vaccinations_df,index=["location"],values=["total_vaccinations"],aggfunc='count')
print(result.head(30))
# grouped = vaccinations_df.groupby(['location', 'total_vaccinations'])
# print(grouped[['location']].aggregate({'Open':np.mean, 'Volume':np.min}))