import dash
from dash import dcc, html, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/inflation',  # represents the url text
                   name='Inflation',  # name of page, commonly used as name of link
                   title='Inflation'  # epresents the title of browser's tab
)

# page 2 data

inflation_data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/inflation_rate.csv", delimiter = ";").fillna(value = 0)
)

layout = html.Div(
    [
        html.H2('World Inflation per year during the period of 2000 - 2021', style={'textAlign':'center', 'margin-top':'40px'}),
        dbc.Row([
            dbc.Col([
                html.P("Select the year: "),
                dcc.Dropdown(
                    options=[
                        {
                            "label": x,
                            "value": x,
                        }
                        for x in range(2000,2022)
                    ],
                    value=2008,
                    id="year-filter",
                    clearable=False,
                    searchable=True,
                    className="dropdown",
                ),
            ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4, style={'margin-bottom':'40px', 'margin-top':'40px'}
            )
        ]),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(
                        id="inflation-map",
                    ),
                ], width=6
            ),
            dbc.Col(
                [
                    dcc.Graph(
                        id="inflation-tree",
                    ),
                ], width=6
            )
        ]),
    ]
)


@callback(
    Output("inflation-map", "figure"),
    Output("inflation-tree", "figure"),
    Input("year-filter", "value")
)

def update_graph(year):
    
    #Inflation Map

    df_inflation = inflation_data.copy()
    df_inflation = df_inflation[df_inflation["year"] == year]


    inflation_map = go.Figure(data=go.Choropleth(
        locations = df_inflation['iso3c'],
        z = df_inflation['Inflation'],
        text = df_inflation['country'],
        colorscale = 'Reds',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '%',
        colorbar_title = 'Inflation Rate',
    ))

    inflation_map.update_layout(
        # title_text='World GDP during per year during the period of 2000 - 2021',

        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
        ),
    )

    #Inflation TreeMap

    dff_inflation = inflation_data.copy()
    dff_inflation = dff_inflation[dff_inflation["year"] == year]
    dff_inflation = dff_inflation[dff_inflation["Inflation"] > 0]
    dff_inflation = dff_inflation[dff_inflation["adminregion"] != 0]
    dff_inflation = dff_inflation[dff_inflation["country"] != 0]
 


    inflation_tree = px.treemap(dff_inflation, path=[px.Constant("World"),dff_inflation['adminregion'], dff_inflation['country']], values='Inflation',
                  color=dff_inflation['Inflation'], 
                  hover_data=[dff_inflation['country'], dff_inflation['Inflation']],
                  color_continuous_scale='Reds',
                  )




    return  inflation_map,inflation_tree