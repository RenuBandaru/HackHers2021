# Dash components - makes it easy to format things

# print("testing...")

# Pandas - allows to manipulate the data easily
import pandas as pd

print("Pandas imported!")

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
print("Dash imported!")
# Graph Components - used to plot graphs
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as po
print("Plotly imported!")

import folium
world = folium.Map(location=[0,0], zoom_start=2)
print("folium imported!")

import numpy as np

app = dash.Dash()
vaccine_df = pd.read_csv("vaccinations-by-manufacturer.csv")
iso_df = pd.read_csv("wikipedia-iso-country-codes.csv")
location_df = pd.read_csv("locations.csv")

#print(vaccine_df)

location_df.drop(['last_observation_date','source_name','source_website'],axis=1,inplace=True)

df = pd.DataFrame(location_df.vaccines.str.split(',').tolist(), index=location_df.iso_code).stack()
print(df)

df = df.reset_index([0, 'iso_code'])
print(df)

print("*****")
df.columns = ['iso_code', 'vaccine']
print(df)

print("splitting done")

#merge df with iso_df so we have the iso code for the countries listed:
df=pd.merge(df, iso_df, left_on="iso_code", right_on="Alpha-3 code")  #merge county an survey on fibs
df.drop(['Alpha-2 code','Alpha-3 code', 'Numeric code', 'ISO 3166-2'], axis=1, inplace=True)
df['use'] = 1

#df = df.rename(columns = {'English short name lower case':'location'})
#merge df with iso_df so we have the iso code for the countries listed:
#df=pd.merge(vaccine_df, iso_df, left_on="location", right_on="English short name lower case")  #merge county an survey on fibs
#df.drop(['English short name lower case', 'Alpha-2 code', 'Numeric code', 'ISO 3166-2'], axis=1, inplace=True)
pd.set_option('display.max_rows', df.shape[0]+1)

#df=pd.merge(df, iso_df, left_on="iso_code", right_on="Alpha-3 code")  #merge county an survey on fibs
#df.drop(['Alpha-3 code','Alpha-2 code', 'Numeric code', 'ISO 3166-2','English short name lower case'], axis=1, inplace=True)
#df['use'] = 1

print("final DF: ^^^^^^^^^^^^^^^^^^^")
#pd.set_option('display.max_rows', df.shape[0]+1)
print(df)

#print('\n \n')
#df.sort_values('vaccine')
#print(df)

print("-----------------------------------------------------------")
# df_sorted = df.sort_values(by='vaccine')
# print(df_sorted)
# vaccineGroups = df.groupby(['vaccine'])
# print(vaccineGroups[])
print("----------------------********-------------------------------------")
#df_pfizer =df.loc[df['vaccine']=='Pfizer/BioNtech']

print("\n")
print("\n" + "ORIGINAL DATAFRAME !!!!!!!!!!!!!!!!!!!!!!!!")
print(df)

print("----------------------****VACCINE DFS: ****-------------------------------------")

#set up dataframes for each vaccine so map can be displayed
df_covaxin = df[df['vaccine'] == 'Covaxin']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_covaxin)
print("\n")

df_jj = df[df['vaccine'] == 'Johnson&Johnson']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_jj)
print("\n")

df_moderna = df[df['vaccine'] == 'Moderna']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_moderna)

print("\n")


print("\n")


df_oxford = df[df['vaccine'] == 'Oxford/AstraZeneca']
#df_oxford.drop(['date'], axis=1, inplace=True)
print(df_oxford)
print("\n")

df_pfizer = df[df['vaccine'] == 'Pfizer/BioNTech']
#df_pfizer = df.loc[df['vaccine']] == ['Pfizer/BioNTech']
#df_pfizer.drop(['date'], axis=1, inplace=True)
print(df_pfizer)
print("\n")

# df_pfizer.groupby(['total_vaccinations'])
# print(df_pfizer['total_vaccinations'].aggregate({'total_vaccinations': np.sum}))
df_sinopharmB = df[df['vaccine'] == 'Sinopharm/Beijing']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinopharmB)
print("\n")

df_sinopharmW = df[df['vaccine'] == 'Sinopharm/Wuhan']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinopharmW)
print("\n")

df_sinovac = df[df['vaccine'] == 'Sinovac']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinovac)
print("\n")

df_moderna = df[df['vaccine'] == 'Moderna']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_moderna)

df_oxford = df[df['vaccine'] == 'Oxford/AstraZeneca']
#df_oxford.drop(['date'], axis=1, inplace=True)
print(df_oxford)
df_sputnik = df[df['vaccine'] == 'Sputnik V']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sputnik)
print("\n")

# df_today = df.loc[df['date'] == df_sorted["date"][0]]
# print(df_today)
print("-----------------------------------------------------------")
#initial dash setup
figure = go.Figure(
    data=go.Choropleth(

        z=df_pfizer['use'], #country the vaccine is used in
        locations=df_pfizer['iso_code'],
        text=df_pfizer['English short name lower case'],
        locationmode="ISO-3",
        autocolorscale=True,

    )
)

figure.update_layout(
    title_text="Vaccinations - Oxford",
    geo_scope='world',
)
#dropdown menu options
vaccineOptions=['Covaxin', 'Johnson&Johnson', 'Moderna', 'Oxford/AstraZeneca', 'Pfizer/BioNTech', 'Sinopharm/Beijing',
                'Sinopharm/Wuhan', 'Sinovac', 'Sputnik']
app.layout = html.Div(
    [
        html.H1("HackHers Covid Dashboard (Global Version 🌏)"),
        dcc.Graph(
            id='main_graph',
            figure=figure,
        ),
        dcc.Dropdown(
            id='data_select',
            options=[{'label': col, 'value': col} for col in vaccineOptions]
        )
    ])
#use this to map input to the correct dataframe
vaccineDict = {
        "Covaxin": df_covaxin,
        "Johnson&Johnson": df_jj,
        "Moderna": df_moderna,
        "Oxford/AstraZeneca": df_oxford,
        "Pfizer/BioNTech": df_pfizer,
        "Sinopharm/Beijing": df_sinopharmB,
        "Sinopharm/W": df_sinopharmW,
        "Sinovac": df_sinovac,
        "Sputnik": df_sputnik
    }


@app.callback(Output("main_graph", "figure"),
              [Input("data_select", "value")])
def update_fig(value):
    df_update = vaccineDict[value]
    print("value passed in: " + str(value))
    figure = go.Figure(
        data=go.Choropleth(
            z=df_update['use'],
            locations=df_update['iso_code'],
            text=df_oxford['English short name lower case'],
            autocolorscale=True,            
        )
    )
    figure.update_layout(
        title_text=value,
    )
    return figure


if __name__ == '__main__':
    app.run_server()
