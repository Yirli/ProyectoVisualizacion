import dash
import pandas as pd
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='GDP',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='GDP values per country during 2000-2021.'
)

# page 1 data


data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/GDP.csv", delimiter = ";") 
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                          dcc.Dropdown(
                            options=[
                                {
                                    "label": x,
                                    "value": x,
                                }
                                for x in range(2000,2022)
                            ],
                            value=2000,
                            id="year-filter",
                            clearable=False,
                            searchable=True,
                            className="dropdown",
                        ),
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='gdp_map', figure={}),
                    ], width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="gdp-tree"),
                    ], width=12
                )
            ]
        )
    ]
)

@callback(
    Output("gdp_map", "figure"),
    Output("gdp-tree", "figure"),
    Input("year-filter", "value"),
)
def update_graph(year):
    df = data.copy()
    df = df[df["year"] == year]



    fig = go.Figure(data=go.Choropleth(
        locations = df['country_code'],
        z = df['total_gdp_million'],
        text = df['country_name'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'GDP<br>Millions US$',
    ))

    fig.update_layout(
        title_text='Global GDP',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        # annotations = [dict(
        #     x=0.55,
        #     y=0.1,
        #     xref='paper',
        #     yref='paper',
        #     text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
        #         CIA World Factbook</a>',
        #     showarrow = False
        # )]
    )

    dff = df.copy()
    dff = dff[dff["total_gdp_million"] != 0]

    treemap_fig = px.treemap(dff, path=[px.Constant("World"),dff['region_name'], dff['country_name']], values='total_gdp_million',
                  color=dff['total_gdp_million'], 
                  hover_data=[dff['country_name'], dff['total_gdp_million']],
                  color_continuous_scale='Blues',
                  )

    return fig, treemap_fig