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
                   title='GDP Data',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='GDP values per country during 2000-2021.'
)

# page 1 data
data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/GDP.csv", delimiter = ";") 
)

inflation_data = (
    pd.read_csv("/home/yirlania/Documents/Visualizacion/Proyecto/ProyectoVisualizacion/inflation_rate.csv", delimiter = ",").fillna(value = 0)
)

countries = data['country_name'].unique()
options =[]
for c in countries:
    if c != None and c != "" and c != 0:
        options.append({'label': c, 'value': c})


layout = html.Div(
    [
        dcc.Tabs([

            dcc.Tab(label="Map", children = [
                html.H2('World GDP per year during the period of 2000 - 2021', style={'textAlign':'center', 'margin-top':'40px'}),
                dbc.Row([
                    dbc.Col(
                        [
                            html.P("Select the year: "),
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
                                placeholder="Select a year",
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
                                dcc.Graph(id='gdp_map', figure={}),
                            ], width=6
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="gdp-tree"),
                            ], width=6
                        )
                    ]),
                    dbc.Row([
                        html.H3('Top 3 Countries with Highest GDP', style={'textAlign':'center','margin-bottom':'40px', 'margin-top':'40px'}),
                            dbc.Col(
                                [
                                    html.Img(src='assets/usa-flag.png', style={'margin-top':'40px', 'margin-bottom':'40px', 'width': '150px'}),
                                    html.P("United States"), 
                                    html.P("$20M") 
                                ], width= 4
                            ),
                            dbc.Col(
                                [
                                    html.Img(src='assets/japan-flag.png', style={'margin-top':'40px', 'margin-bottom':'40px',  'width': '150px'}), 
                                    html.P("Japan"),
                                    html.P("$5M") 
                                ], width= 4
                            ),
                            dbc.Col(
                                [
                                    html.Img(src='assets/china-flag.png', style={'margin-top':'40px', 'width': '150px'}), 
                                    html.P("China"),
                                    html.P("$2M") 
                                ], width= 4
                            ),

                    ])
                ]),

            dcc.Tab(label="Data per Country", children = [
                dbc.Row([
                    dbc.Col(
                        [
                            html.P("Select the country: "),
                            dcc.Dropdown(
                                options=options,
                                value="Costa Rica",
                                id="country-filter",
                                placeholder="Select a country",
                                clearable=False,
                                searchable=True,
                                className="dropdown",
                            ),
                        ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4, width=6, style={'margin-bottom':'40px', 'margin-top':'40px'}
                    ),
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                                id="sector-barchart",
                            ),
                        ], width=6
                    ),
                    dbc.Col([
                        dcc.Graph(
                                id="inflation-barchart",
                            ),
                        ], width=6
                    )
                ])
            ])

        ]),

    ]
)

@callback(
    Output("gdp_map", "figure"),
    Output("gdp-tree", "figure"),
    Output("sector-barchart", "figure"),
    Output("inflation-barchart", "figure"),
    Input("year-filter", "value"),
    Input("country-filter", "value"),
)
def update_graph(year, country):
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
        # title_text='World GDP during per year during the period of 2000 - 2021',

        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
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
                  color_continuous_scale='Blues'
                  )
    
    x = dff['country_name']

    #Country GDP 
    country_gdp = data.copy()
    country_gdp = country_gdp[country_gdp["country_name"] == country]

    country_gdp_fig = px.line(country_gdp, x='year', y='total_gdp_million',title="GDP during the period of 2000-2021")
    country_gdp_fig.update_layout(
        xaxis_title = "Year",
        yaxis_title="GDP (Millions of $)",
    )

    country_gdp_fig.update_traces(line_color='blue')


    #Country Inflation 
    country_inflation = inflation_data.copy()
    country_inflation = country_inflation[country_inflation["country"] == country]

    country_inflation_fig = px.line(country_inflation, x='year', y='Inflation',  title="Inflation during the period of 2000-2021",
    )
    country_inflation_fig.update_traces(line_color='red')
    country_inflation_fig.update_layout(
        xaxis_title = "Year",
        yaxis_title="Inflation (%)",
    )


    return fig, treemap_fig,country_gdp_fig, country_inflation_fig