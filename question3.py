# Pandas - allows to manipulate the data easily
import pandas as pd
print("Pandas imported!")
import numpy as np
import matplotlib.pyplot as plot

vaccinations_df = pd.read_csv("vaccinations.csv")

#vaccinations_df.groupby(['location']).tail(1)

print('----------------------------------------------- \n\n')
country_pop_df = pd.read_csv("covid19_country_population.csv")
pd.set_option('display.max_rows', country_pop_df.shape[0]+1)
print(country_pop_df)

print('----------------------------------------\n\n')
#merge df with iso_df so we have the iso code for the countries listed:
df=pd.merge(vaccinations_df, country_pop_df, left_on="iso_code", right_on="CountryAlpha3Code")  #merge county an survey on fibs
#df.drop(['Alpha-2 code','Alpha-3 code', 'Numeric code', 'ISO 3166-2'], axis=1, inplace=True)
#pd.set_option('display.max_rows', df.shape[0]+1)

df['percentVac'] = df['total_vaccinations']/df['population'] * 100
# df.plot.bar(stacked=True)
# df.plot.bar(subplots=True)

#df=pd.merge(result, country_pop_df, left_on="iso_code", right_on="CountryAlpha3Code") 
#result=pd.pivot_table(vaccinations_df,index=["location","iso_code"],values=["total_vaccinations"],aggfunc='max')
#result=pd.pivot_table(vaccinations_df,index=["location"],values=["daily_vaccinations"],aggfunc='sum')
result=pd.pivot_table(df,index=["location", "iso_code","population"],values=["total_vaccinations","percentVac"],aggfunc='max')

pd.set_option('display.max_rows', result.shape[0]+1)
print(result)

print('----------------------------------------------- \n')



