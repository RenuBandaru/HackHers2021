# Dash components - makes it easy to format things
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Graph Components - used to plot graphs
import plotly.graph_object as go
import plotly.express as px
import plotly.offline as po

# Pandas - allows to manipulate the data easily
import pandas as pd

app = dash.Dash()

df = pd.read_csv("all-states-history.csv")
print(df)

df_sorted = df.sort
df_today = df.loc[df['date'] == df_sorted["date"][0]]
print(df_today)

figure = go.Figure(
    data=go.Choropleth(
        z=df_today['death'],
        locations=df_today['state'],
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
            z=df_today[value],
            locations=df_today['state'],
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


