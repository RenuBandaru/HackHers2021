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
locations_df = pd.read_csv("locations.csv")

#print(vaccine_df)

# #merge df with iso_df so we have the iso code for the countries listed:
# df = pd.DataFrame(locations_df.vaccines.str.split(',').tolist(), index=locations_df.location)
# df = df.reset_index([0, 'location'])
# #df.columns=['location', 'iso_code', 'vaccines']
# print(df)
print("---------------------------------------------------------")

df=pd.merge(vaccine_df, iso_df, left_on="location", right_on="English short name lower case")  #merge county an survey on fibs
#df.drop(['English short name lower case', 'Alpha-2 code', 'Numeric code', 'ISO 3166-2'], axis=1, inplace=True)
print(df)
print("-----------------------------------------------------------")
# df_sorted = df.sort_values(by='vaccine')
# print(df_sorted)
# vaccineGroups = df.groupby(['vaccine'])
# print(vaccineGroups[])
print("----------------------********-------------------------------------")
df_pfizer = df[df['vaccine'] == 'Pfizer/BioNTech']
df_pfizer.drop(['date'], axis=1, inplace=True)
print(df_pfizer)
# df_pfizer.groupby(['total_vaccinations'])
# print(df_pfizer['total_vaccinations'].aggregate({'total_vaccinations': np.sum}))

df_sinovac = df[df['vaccine'] == 'Sinovac']
df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinovac)

df_moderna = df[df['vaccine'] == 'Moderna']
df_moderna.drop(['date'], axis=1, inplace=True)
print(df_moderna)

df_oxford = df[df['vaccine'] == 'Oxford/AstraZeneca']
df_oxford.drop(['date'], axis=1, inplace=True)
print(df_oxford)

# df_today = df.loc[df['date'] == df_sorted["date"][0]]
# print(df_today)
print("-----------------------------------------------------------")
figure = go.Figure(
    data=go.Choropleth(
        z=df_oxford['total_vaccinations'], #country the vaccine is used in
        locations=df_oxford['Alpha-3 code'],
        text=df_oxford['location'],
        locationmode="ISO-3",
        autocolorscale=True,

    )
)

figure.update_layout(
    title_text="Vaccinations - Oxford",
    geo_scope='world',
)

vaccineOptions=['Moderna', 'Oxford/AstraZeneca', 'Pfizer/BioNTech', 'Sinovac']
app.layout = html.Div(
    [
        html.H1("HackHers Covid Dashboard (Global ._.)"),
        dcc.Graph(
            id='main_graph',
            figure=figure,
        ),
        dcc.Dropdown(
            id='data_select',
            options=[{'label': col, 'value': col} for col in vaccineOptions]
        )
    ])

vaccineDict = {
        "Moderna": df_moderna,
        "Oxford/AstraZeneca": df_oxford,
        "Pfizer/BioNTech": df_pfizer,
        "Sinovac": df_sinovac
    }
    #use this to map input to the correct dataframe

@app.callback(Output("main_graph", "figure"),
              [Input("data_select", "value")])
def update_fig(value):
    df_update = vaccineDict[value]
    print("value passed in: " + str(value))
    figure = go.Figure(
        data=go.Choropleth(
            z=df_update['total_vaccinations'],
            locations=df_update['Alpha-3 code'],
            locationmode="ISO-3",
            autocolorscale=True,
        )
    )
    figure.update_layout(
        title_text=value,
    )
    return figure


if __name__ == '__main__':
    app.run_server()
