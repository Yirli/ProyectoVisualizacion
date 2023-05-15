# import pandas as pd
# import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
# from dash import Dash, Input, Output, dcc, html
# import numpy as np

# data = (
#     pd.read_csv("GDP.csv", delimiter = ";")
# )

# inflation_data = (
#     pd.read_csv("inflation_rate.csv", delimiter = ",").fillna(value = 0)
# )


# external_stylesheets = [
#     {
#         "href": (
#             "https://fonts.googleapis.com/css2?"
#             "family=Lato:wght@400;700&display=swap"
#         ),
#         "rel": "stylesheet",
#     },
# ]

# app = Dash(__name__, external_stylesheets=external_stylesheets)
# app.title = "Análisis entre la inflación y el PIB en el mundo"

# # ------------------------------------------------------------------------------
# # App layout

# app.layout = html.Div(
#     children=[
#         html.Div(
#             children=[
#                 html.P(children="🥑", className="header-emoji"),
#                 html.H1(
#                     children="Finance Analytics", className="header-title"
#                 ),
#                 html.P(
#                     children=(
#                         "Analyze relantioship between GDP and inflation between"
#                         " differet countries in the world"
#                     ),
#                     className="header-description",
#                 ),
#             ],
#             className="header",
#         ),
#         html.Div(
#             children=[
#                 html.Div(
#                     children=[
#                         html.Div(children="Year", className="menu-title"),
#                         dcc.Dropdown(
#                             options=[
#                                 {
#                                     "label": x,
#                                     "value": x,
#                                 }
#                                 for x in range(1980,2022)
#                             ],
#                             value=1980,
#                             id="year-filter",
#                             clearable=False,
#                             searchable=True,
#                             className="dropdown",
#                         ),
#                     ],
#                 ),
#             ],
#             className="menu",
#         ),
#         html.Div(
#             children=[
#                 html.Div(
#                     children = dcc.Graph(id='gdp_map', figure={}),
#                     className="card",
#                 ),
#                 html.Div(
#                     children=dcc.Graph(
#                         id="gdp-tree",
#                     ),
#                     className="card",
#                 ),
#                 html.Div(
#                     children=dcc.Graph(
#                         id="gdp-crtrading-line",
#                     ),
#                     className="card",
#                 ),
#                 html.Div(
#                     children=dcc.Graph(
#                         id="inflation-map",
#                     ),
#                     className="card",
#                 ),
#                 html.Div(
#                     children=dcc.Graph(
#                         id="inflation-tree",
#                     ),
#                     className="card",
#                 ),
#                 html.Div(
#                     children=dcc.Graph(
#                         id="inflation-crtrading-line",
#                     ),
#                     className="card",
#                 ),
#             ],
#             className="wrapper",
#         ),
#     ]
# )


# @app.callback(
#     Output("gdp_map", "figure"),
#     Output("gdp-tree", "figure"),
#     Output("gdp-crtrading-line", "figure"),
#     Output("inflation-map", "figure"),
#     Output("inflation-tree", "figure"),
#     Output("inflation-crtrading-line", "figure"),
#     Input("year-filter", "value"),
# )
# def update_charts(year):
    
#     #GDP Map
#     df = data.copy()
#     df = df[df["year"] == year]


#     fig = go.Figure(data=go.Choropleth(
#         locations = df['country_code'],
#         z = df['total_gdp_million'],
#         text = df['country_name'],
#         colorscale = 'Blues',
#         autocolorscale=False,
#         reversescale=True,
#         marker_line_color='darkgray',
#         marker_line_width=0.5,
#         colorbar_tickprefix = '$',
#         colorbar_title = 'GDP<br>Millions US$',
#     ))

#     fig.update_layout(
#         title_text='Global GDP',
#         geo=dict(
#             showframe=False,
#             showcoastlines=False,
#             projection_type='equirectangular'
#         ),
#         # annotations = [dict(
#         #     x=0.55,
#         #     y=0.1,
#         #     xref='paper',
#         #     yref='paper',
#         #     text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
#         #         CIA World Factbook</a>',
#         #     showarrow = False
#         # )]
#     )

#     #Inflation Map

#     df_inflation = inflation_data.copy()
#     df_inflation = df_inflation[df_inflation["year"] == year]


#     inflation_map = go.Figure(data=go.Choropleth(
#         locations = df_inflation['iso3c'],
#         z = df_inflation['Inflation'],
#         text = df_inflation['country'],
#         colorscale = 'Reds',
#         autocolorscale=False,
#         reversescale=False,
#         marker_line_color='darkgray',
#         marker_line_width=0.5,
#         colorbar_tickprefix = '%',
#         colorbar_title = 'Inflation Rate',
#     ))

#     #GDP TreeMap

#     dff = df.copy()
#     dff = dff[dff["total_gdp_million"] != 0]

#     treemap_fig = px.treemap(dff, path=[px.Constant("world"),dff['region_name'], dff['country_name']], values='total_gdp_million',
#                   color=dff['total_gdp_million'], 
#                   hover_data=[dff['country_name'], dff['total_gdp_million']],
#                   color_continuous_scale='Blues',
#                   )

#     #Inflation TreeMap

#     dff_inflation = df_inflation.copy()
#     dff_inflation = dff_inflation[dff_inflation["Inflation"] != 0]

#     treemap_inflation_fig = px.treemap(dff_inflation, path=[px.Constant("world"),dff_inflation['adminregion'], dff_inflation['country']], values='Inflation',
#                   color=dff_inflation['Inflation'], 
#                   hover_data=[dff_inflation['country'], dff_inflation['Inflation']],
#                   color_continuous_scale='Reds',
#                   )


#     #GDP Tradin Partners

#     data_trading_filter = data.copy()
#     data_trading_filter = data_trading_filter[(data_trading_filter["country_name"] == "Belgium") | (data_trading_filter["country_name"] == "Costa Rica") | (data_trading_filter["country_name"] == "United States of America") | (data_trading_filter["country_name"] == "Netherlands")]
#     crtrading_lin_fig = px.line(data_trading_filter, x='year', y='total_gdp_million', color='country_name')

#     #Inflation Tradin Partners

#     data_inflation_trading_filter = inflation_data.copy()
#     data_inflation_trading_filter = data_inflation_trading_filter[(data_inflation_trading_filter["country"] == "Belgium") | (data_inflation_trading_filter["country"] == "Costa Rica") | (data_inflation_trading_filter["country"] == "United States") | (data_inflation_trading_filter["country"] == "Netherlands")]
#     inflation_crtrading_lin_fig = px.line(data_inflation_trading_filter, x='year', y='Inflation', color='country')


#     return fig, treemap_fig, crtrading_lin_fig, inflation_map, treemap_inflation_fig, inflation_crtrading_lin_fig


# if __name__ == "__main__":
#     app.run_server(debug=True)


import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)

app.layout = dbc.Container([
    # dbc.Row([
    #     dbc.Col(html.Div("Análisis del GDP e Inflación en el mundo en el período de 2000-2021",
    #                      style={'fontSize':50, 'textAlign':'center'}))
    # ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)