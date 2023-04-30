from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from Vis_func import *
import sqlite3
import numpy as np
import os


# Load and prepare data
cnx = sqlite3.connect('KinoPoisk.db')
df = pd.read_sql_query("SELECT * FROM films_data", cnx)
df = df.fillna(value=np.nan)

num_columns = ['Сборы в мире', 'Сборы в США', 'Оценка фильма']
for col in num_columns:
    df[col] = pd.to_numeric(df[col])
df['Год производства'] = pd.to_numeric(
    df['Год производства'],
    downcast="integer"
)

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.LUX])

# Group data by year and find the maximum number of viewers per year
viewers_per_year = df.groupby('Год производства')['Зрители'].max()

# Define the years to display in the range slider and line plot
years = [
    df['Год производства'].min(),
    1950, 1960, 1970, 1980, 1990, 2000, 2010,
    df['Год производства'].max()
]

# Create the line plot


def line_plot(df_viewers_per_year = viewers_per_year):
    fig = px.line(
        df_viewers_per_year,
        title='Maximum number of viewers per year of production',
    )
    fig.update_traces(line_color='red')
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Max viewers',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig


# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1(children='KinoPoisk Dashboard (top films)',
                style={
                    "text-align": "center",
                    'color': '#FFEBCD',
                    "background-color": "#67001F",
                    "font-family": "ui-monospace"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {'label': 'Genres',
                                                             'value': 'Genres'},
                                                            {'label': 'Countries',
                                                             'value': 'Countries'}
                                                        ],
                                                        value='Genres',
                                                        id='dropdown_bar_category',
                                                        className='dropdown-bar-category',
                                                    ),
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {'label': 'Revenue',
                                                             'value': 'Revenue'},
                                                            {'label': 'Viewers',
                                                             'value': 'Viewers'},
                                                            {'label': 'Score',
                                                             'value': 'Score'}
                                                        ],
                                                        value='Revenue',
                                                        id='dropdown_bar_measure',
                                                        className='dropdown-bar-measure',
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dcc.Graph(
                                            id='bar_plot',
                                            figure=bar_plot(
                                                df=df,
                                                name_of_category_column='Жанр',
                                                name_of_measerment_column='Сборы в мире',
                                                title_name='The average Revenue of top films by genre'
                                            ),
                                            className='bar-chart'
                                        ),
                                    ]
                                ),
                            ],
                            className='bar-chart-container',
                            style={'height': '52%', 'margin-top': '20px',
                                   'border-radius': '15px'},
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader('Words Cloud'),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='word_cloud',
                                        figure=words_cloud(df=df),
                                        className='graph',
                                        style={'height': '300px',
                                               'width': '100%'}
                                    ),
                                ),
                            ],
                            className='words-cloud-container',
                            style={'height': '44%', 'margin-top': '20px',
                                   'border-radius': '15px'}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody([
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Genres', 'value': 'Genres'},
                                            {'label': 'Countries',
                                             'value': 'Countries'}
                                        ],
                                        value='Genres',
                                        id='dropdown_pie',
                                        className='dropdown',
                                        labelStyle={"display": "block",
                                                    "margin-bottom": "10px"},
                                        inputStyle={"margin-right": "5px"}
                                    ),
                                    dcc.Graph(
                                        id='number_of_films',
                                        figure=count_plot(
                                            df=df,
                                            name_of_category_column='Жанр',
                                            title_name='The percentage of top films by genre'
                                        ),
                                        className='pie-chart'
                                    ),
                                ]
                                ),
                            ],
                            className='pie-chart-container',
                            style={'height': '46%', 'margin-top': '20px',
                                   'border-radius': '15px'}
                        ),

                        dbc.Card(
                            [
                                dbc.CardBody([
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Сборы в мире',
                                             'value': 'Сборы в мире'},
                                            {'label': 'Кол-во зрителей',
                                             'value': 'Зрители'},
                                            {'label': 'Бюджет', 'value': 'Бюджет'}
                                        ],
                                        value='Зрители',
                                        id='dropdown_box',
                                        className='dropdown',
                                        labelStyle={"display": "block",
                                                    "margin-bottom": "10px"},
                                        inputStyle={"margin-right": "5px"}
                                    ),
                                    dcc.Graph(
                                        id='box_plot',
                                        figure=box_plot(
                                            df=df,
                                            measurement_column='Зрители'
                                        ),
                                        className='box-plot'
                                    ),
                                ])
                            ],
                            className='box-plot-container',
                            style={'height': '50%', 'margin-top': '20px',
                                   'border-radius': '15px'}
                        ),
                    ],
                    md=6,

                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.CardBody([
                            dcc.RangeSlider(
                                min=df['Год производства'].min(),
                                max=df['Год производства'].max(),
                                id='slider_years',
                                marks={
                                    int(year): {'label': str(year)}
                                    for year in years
                                },
                                value=[
                                    df['Год производства'].min(),
                                    df['Год производства'].max()
                                ],
                                step=1,
                                className='range-slider'
                            ),
                            dcc.Graph(
                                id='viewers_per_year',
                                figure=line_plot(),
                                className='line-plot'
                            ),
                        ]
                        ),
                    ],
                    className='line-plot-container',
                    style={'height': '32%', 'width': '100%',
                           'margin-top': '20px', 'border-radius': '15px'}
                ),
            ],
        ),
    ],
    style={'background-color': '#FFEBCD'}
)

# Define the callbacks


@app.callback(
    Output('viewers_per_year', 'figure'),
    Input('slider_years', 'value')
)
def update_graph(years_list):
    dff = df[
        (df['Год производства'] >= years_list[0]) &
        (df['Год производства'] <= years_list[1])
    ]
    viewers_per_years = dff.groupby('Год производства')['Зрители'].max()
    fig = line_plot(df_viewers_per_year=viewers_per_years)
    return fig


@app.callback(
    Output('number_of_films', 'figure'),
    Input('dropdown_pie', 'value')
)
def update_count_plot(category):
    if category == 'Genres':
        category_column = 'Жанр'
        title_name = 'The percentage of top films by genre'
    else:
        category_column = 'Страна'
        title_name = 'The percentage of top films by country'
    figure = count_plot(
        df=df,
        name_of_category_column=category_column,
        title_name=title_name
    )
    return figure


@app.callback(
    Output('bar_plot', 'figure'),
    Input('dropdown_bar_category', 'value'),
    Input('dropdown_bar_measure', 'value')
)
def update_bar_plot(
    category,
    measure
):
    if measure == 'Revenue':
        measure_col = 'Сборы в мире'
        title_name = 'The average Revenue of top films'
        scale = None
    elif measure == 'Viewers':
        measure_col = 'Зрители'
        title_name = 'The average number of viewers of top films'
        scale = None
    else:
        measure_col = 'Оценка фильма'
        title_name = 'The average score of top top films'
        scale = [7.5, 9]
    if category == 'Genres':
        cat_col = 'Жанр'
        title_name = title_name + ' by genre'
    else:
        cat_col = 'Страна'
        title_name = title_name + ' by country'
    fig = bar_plot(
        df=df,
        name_of_category_column=cat_col,
        name_of_measerment_column=measure_col,
        title_name=title_name,
        scale_of_axis=scale
    )

    return fig


@app.callback(
    Output('box_plot', 'figure'),
    Input('dropdown_box', 'value')
)
def update_box_plot(column):
    fig = box_plot(df, measurement_column=column)
    return fig


if __name__ == '__main__':
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=os.getenv("PORT", "8050"),
        debug=True,
        use_reloader=False
    )
