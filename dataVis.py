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

#merge df with iso_df so we have the iso code for the countries listed:
df=pd.merge(df, iso_df, left_on="iso_code", right_on="Alpha-3 code")  #merge county an survey on fibs
df.drop(['Alpha-3 code','Alpha-2 code', 'Numeric code', 'ISO 3166-2'], axis=1, inplace=True)
df['use'] = 1

print("final DF: ^^^^^^^^^^^^^^^^^^^")
#pd.set_option('display.max_rows', df.shape[0]+1)
print(df)
print("-----------------------------------------------------------")
# df_sorted = df.sort_values(by='vaccine')
# print(df_sorted)
# vaccineGroups = df.groupby(['vaccine'])
# print(vaccineGroups[])
print("----------------------****VACCINE DFS: ****-------------------------------------")

df_covaxin = df[df['vaccine'] == 'Covaxin']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_covaxin)
print("\n")

df_jj = df[df['vaccine'] == 'Johnson&Johnson']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_jj)
print("\n")


print("\n" + "ORIGINAL DATAFRAME !!!!!!!!!!!!!!!!!!!!!!!!")
print(df)
print("\n")

df_moderna = df[df['vaccine'] == 'Moderna']
#df_moderna.drop(['date'], axis=1, inplace=True)
print(df_moderna)
print("\n")
print("\n" + "ORIGINAL DATAFRAME !!!!!!!!!!!!!!!!!!!!!!!!")
print(df)
print("\n")

df_oxford = df[df['vaccine'] == 'Oxford/AstraZeneca']
#df_oxford.drop(['date'], axis=1, inplace=True)
print(df_oxford)
print("\n")

df_pfizer = df[df['vaccine'] == 'Pfizer/BioNTech']
#df_pfizer.drop(['date'], axis=1, inplace=True)
print(df_pfizer)
print("\n")

# df_pfizer.groupby(['total_vaccinations'])
# print(df_pfizer['total_vaccinations'].aggregate({'total_vaccinations': np.sum}))
df_sinopharmB = df[df['vaccine'] == 'Sinopharm/Beijing']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinopharmB)
print("\n")

df_sinopharmW = df[df['vaccine'] == 'Sinopharm/Beijing']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinopharmW)
print("\n")

df_sinovac = df[df['vaccine'] == 'Sinovac']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sinovac)
print("\n")

df_sputnik = df[df['vaccine'] == 'Sputnik V']
#df_sinovac.drop(['date'], axis=1, inplace=True)
print(df_sputnik)
print("\n")

# df_today = df.loc[df['date'] == df_sorted["date"][0]]
# print(df_today)
print("-----------------------------------------------------------")
figure = go.Figure(
    data=go.Choropleth(
        z=df_oxford['use'], #country the vaccine is used in
        locations=df_oxford['iso_code'],
        text=df_oxford['English short name lower case'],
        locationmode="ISO-3",
        colorscale='Blues',

    )
)
figure.add_layout_image(
        dict(
            source="https://staticwordpress.s3.amazonaws.com/blog.luxuryhomemarketing.com/uploads/2020/03/Bonus_BP01-Power-Market-Photo-scaled.jpg",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.1,
            layer="below")
)
figure.update_layout(
    title_text="Which vaccines are used and in which countries?",
    geo_scope='world',
)

vaccineOptions=['Covaxin', 'Johnson&Johnson', 'Moderna', 'Oxford/AstraZeneca', 'Pfizer/BioNTech', 'Sinopharm/Beijing',
                'Sinopharm/Wuhan', 'Sinovac', 'Sputnik']
app.layout = html.Div(
    [
        html.H1("HackHers COVID-19 Dashboard (Global Version 🌏)"),
        dcc.Graph(
            id='main_graph',
            figure=figure,
        ),
        dcc.Dropdown(
            id='data_select',
            options=[{'label': col, 'value': col} for col in vaccineOptions]
        ),
        html.H1("Which country is vaccinating a larger percent of its population?"),
        html.Div(
            children=html.Img(
                src="https://raw.githubusercontent.com/RenuBandaru/HackHers2021/main/Ques_3.png",
                style={
                    'maxWidth': '100%',
                    'maxHeight': '100%',
                    'marginLeft': 'auto',
                    'marginRight': 'auto'
                }
            ),
            style={
                'maxWidth': '100%',
                'maxHeight': '100%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'border': 'thin grey solid'
            }
        )


    ])

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
    #use this to map input to the correct dataframe

@app.callback(Output("main_graph", "figure"),
              [Input("data_select", "value")])
def update_fig(value):
    df_update = vaccineDict[value]
    print("value passed in: " + str(value))
    figure = go.Figure(
        data=go.Choropleth(
            z=df_update['use'],  # country the vaccine is used in
            locations=df_update['iso_code'],
            text=df_update['English short name lower case'],
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
