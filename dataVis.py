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
app = dash.Dash()

df = pd.read_csv("vaccinations-by-manufacturer.csv")
print(df)
print("-----------------------------------------------------------")
# df_sorted = df.sort_values(by='vaccine')
# print(df_sorted)
# vaccineGroups = df.groupby(['vaccine'])
# print(vaccineGroups[])
print("----------------------********-------------------------------------")
df_pfizer = df[df['vaccine'] == 'Pfizer/BioNTech']
print(df_pfizer)

df_sinovac = df[df['vaccine'] == 'Sinovac']
print(df_sinovac)

df_moderna = df[df['vaccine'] == 'Moderna']
print(df_moderna)

df_oxford = df[df['vaccine'] == 'Oxford/AstraZeneca']
print(df_oxford)

# df_today = df.loc[df['date'] == df_sorted["date"][0]]
# print(df_today)
print("-----------------------------------------------------------")
figure = go.Figure(
    data=go.Choropleth(
        z=df_moderna['location'], #country the vaccine is used in
        locations=df_moderna['location'],
        locationmode="USA-states",
        autocolorscale=True,

    )
)

figure.update_layout(
    title_text="Deaths",
    geo_scope='usa',
)

app.layout = html.Div(
    [
        html.H1("HackPSU Covid Dashboard (US)"),
        dcc.Graph(
            id='main_graph',
            figure=figure,
        ),
        dcc.Dropdown(
            id='data_select',
            options=[{'label': col, 'value': col} for col in df.columns.values[3:]]
        )
    ])


@app.callback(Output("main_graph", "figure"),
              [Input("data_select", "value")])
def update_fig(value):
    figure = go.Figure(
        data=go.Choropleth(
            z=df_moderna[value],
            locations=df_moderna['location'],
            locationmode="USA-states",
            autocolorscale=True,
        )
    )
    figure.update_layout(
        titl_text=value,
    )
    return figure


if __name__ == '__main__':
    app.run_server()
