import dash
import pandas as pd
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

inflation_data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/inflation_rate.csv", delimiter = ",").fillna(value = 0)
)

data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/GDP.csv", delimiter = ";") 
)

dash.register_page(__name__,
                   path='/tradingPartners',
                   name='Trading Partners',
                   title='Trading Partners',
                   description='Learn all about the heatmap.'
)

    #GDP Tradin Partners

data_trading_filter = data.copy()
data_trading_filter = data_trading_filter[(data_trading_filter["country_name"] == "Belgium") | (data_trading_filter["country_name"] == "Costa Rica") | (data_trading_filter["country_name"] == "United States of America") | (data_trading_filter["country_name"] == "Netherlands")]
crtrading_lin_fig = px.line(data_trading_filter, x='year', y='total_gdp_million', color='country_name')


    #Inflation Tradin Partners

data_inflation_trading_filter = inflation_data.copy()
data_inflation_trading_filter = data_inflation_trading_filter[(data_inflation_trading_filter["country"] == "Belgium") | (data_inflation_trading_filter["country"] == "Costa Rica") | (data_inflation_trading_filter["country"] == "United States") | (data_inflation_trading_filter["country"] == "Netherlands")]
inflation_crtrading_lin_fig = px.line(data_inflation_trading_filter, x='year', y='Inflation', color='country')

layout = html.Div(
    [
        dcc.Markdown('## Costa Rica vs its Main Trading Partners', style={'textAlign':'center'}),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(
                        id="gdp-crtrading-line", figure=crtrading_lin_fig
                    ),
                ], width=12
            )
        ]),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(
                        id="inflation-crtrading-line", figure=inflation_crtrading_lin_fig
                    ),
                ], width=12
            )
        ])
    ]
)



# @callback(
#     Output("gdp-crtrading-line", "figure"),
#     Output("inflation-crtrading-line", "figure"),
#     # Input("year-filter", "value")
# )

# def update_graph(year):
    
    #GDP Tradin Partners

data_trading_filter = data.copy()
data_trading_filter = data_trading_filter[(data_trading_filter["country_name"] == "Belgium") | (data_trading_filter["country_name"] == "Costa Rica") | (data_trading_filter["country_name"] == "United States of America") | (data_trading_filter["country_name"] == "Netherlands")]
crtrading_lin_fig = px.line(data_trading_filter, x='year', y='total_gdp_million', color='country_name')




    #Inflation Tradin Partners

data_inflation_trading_filter = inflation_data.copy()
data_inflation_trading_filter = data_inflation_trading_filter[(data_inflation_trading_filter["country"] == "Belgium") | (data_inflation_trading_filter["country"] == "Costa Rica") | (data_inflation_trading_filter["country"] == "United States") | (data_inflation_trading_filter["country"] == "Netherlands")]
inflation_crtrading_lin_fig = px.line(data_inflation_trading_filter, x='year', y='Inflation', color='country')


    # return crtrading_lin_fig, inflation_crtrading_lin_fig
