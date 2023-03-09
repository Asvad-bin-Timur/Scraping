from dash import Dash, html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from Vis_func import *
import sqlite3
import numpy as np
import os
import flask

server = flask.Flask(__name__)

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
fig = px.line(
    viewers_per_year,
    title='Maximum number of viewers per year of production'
)

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1(children='KinoPoisk Dashboard (top films)',
                style={
                    "text-align": "center",
                    'color': '#FFEBCD',
                    "background-color": "#008080",
                    "font-family": "Arial, sans-serif"}),
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.CardHeader("Select years"),
                        dbc.CardBody(
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
                        ),
                    ],
                    className='range-slider-container',
                    style={'height': '8%'}
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Line graph"),
                        dbc.CardBody(
                            dcc.Graph(
                                id='viewers_per_year',
                                figure=fig,
                                className='line-plot'
                            ),
                        ),
                    ],
                    className='line-plot-container',
                    style={'height': '32%'}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Select bar chart category and measure"),
                                dbc.CardBody(
                                    [
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'Genres', 'value': 'Genres'},
                                                {'label': 'Countries', 'value': 'Countries'}
                                            ],
                                            value='Genres',
                                            id='dropdown_bar_category',
                                            className='dropdown-bar-category'
                                        ),
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'Revenue', 'value': 'Revenue'},
                                                {'label': 'Viewers', 'value': 'Viewers'},
                                                {'label': 'Score', 'value': 'Score'}
                                            ],
                                            value='Revenue',
                                            id='dropdown_bar_measure',
                                            className='dropdown-bar-measure'
                                        ),
                                    ],
                                ),
                            ],
                            className='dropdown-bar-container',
                            style={'height': '10%', 'margin-top': '20px'}
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Bar plot"),
                                dbc.CardBody(
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
                                ),
                            ],
                            className='bar-chart-container',
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader('Words Cloud'),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='word_cloud',
                                        # figure=words_cloud(df=df),
                                        className='graph'
                                    ),
                                ),
                            ],
                            className='words-cloud-container',
                            style={'height': '38%', 'margin-top': '20px'}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Select pie chart category"),
                                dbc.CardBody(
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Genres', 'value': 'Genres'},
                                            {'label': 'Countries', 'value': 'Countries'}
                                        ],
                                        value='Genres',
                                        id='dropdown_pie',
                                        className='dropdown',
                                        labelStyle={"display": "block", "margin-bottom": "10px"},
                                        inputStyle={"margin-right": "5px"}
                                    ),
                                ),
                            ],
                            className='dropdown-container',
                            style={'height': '8%', 'margin-top': '20px'}
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Pie chart"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='number_of_films',
                                        figure=count_plot(
                                            df=df,
                                            name_of_category_column='Жанр',
                                            title_name='The percentage of top films by genre'
                                        ),
                                        className='pie-chart'
                                    ),
                                ),
                            ],
                            className='pie-chart-container',
                            style={'height': '40%'}
                        ),

                        dbc.Card(
                            [
                                dbc.CardHeader("Select x-axis"),
                                dbc.CardBody(
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Сборы в мире', 'value': 'Сборы в мире'},
                                            {'label': 'Кол-во зрителей', 'value': 'Зрители'},
                                            {'label': 'Бюджет', 'value': 'Бюджет'}
                                        ],
                                        value='Зрители',
                                        id='dropdown_box',
                                        className='dropdown',
                                        labelStyle={"display": "block", "margin-bottom": "10px"},
                                        inputStyle={"margin-right": "5px"}
                                    ),
                                ),
                            ],
                            className='dropdown-container',
                            style={'height': '11%', 'margin-top': '20px'}
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Box plot"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='box_plot',
                                        figure=box_plot(
                                            df=df,
                                            measurement_column='Зрители'
                                        ),
                                        className='box-plot'
                                    ),
                                ),
                            ],
                            className='box-plot-container',
                            style={'height': '40%'}
                        ),
                    ],
                    md=6,

                ),
            ],
            style={'background-color': '#FFFAF0'}
        ),
    ],
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
    viewers_per_year = dff.groupby('Год производства')['Зрители'].max()
    fig = px.line(
        viewers_per_year,
        title='Maximum number of viewers per year of production'
    )
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Max viewers'
    )
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
        host = os.getenv("HOST", "127.0.0.1"),
        port = os.getenv("PORT", "8050"),
        debug=True,
        use_reloader=False
    )
