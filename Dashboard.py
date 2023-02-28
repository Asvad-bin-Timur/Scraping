from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output
from matplotlib import pyplot as plt
from matplotlib import ticker as tick
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.express as px
from Vis_func import bar_plot
from Vis_func import count_plot

df = pd.read_csv('KinoPoisk_processed')
app = Dash()

viewers_per_year = df.groupby('Год производства')['Зрители'].max()
years = [df['Год производства'].min(), 1950, 1960, 1970, 1980, 1990, 2000, 2010, df['Год производства'].max()]
fig = px.line(viewers_per_year, title='Maximum number of viewers per year of production')


app.layout = html.Div(children=[
    html.Div([
            html.H1(children='KinoPoisk Dashboard (top films)'),
            dcc.RangeSlider(
                min = df['Год производства'].min(),
                max = df['Год производства'].max(),
                id = 'slider_years',
                marks = {int(year): {'label': str(year)} for year in years},
                value = [df['Год производства'].min(), df['Год производства'].max()],
                step=1,),
            dcc.Graph(
                id='viewers_per_year', 
                figure=fig)]),
    html.Div([
            dcc.Dropdown(
                ['Genres', 'Countries'], 
                value = 'Genres',
                id = 'dropdown_pie'),
            dcc.Graph(
                id = 'number_of_films', 
                figure = count_plot(df = df, name_of_category_column='Жанр', title_name='The percentage of top films by genre'))]),
            dcc.Dropdown(
                ['Genres', 'Countries'], 
                value = 'Genres',
                id = 'dropdown_bar_category',
                style={'width': '90vh', 'display': 'inline-block'}),
            dcc.Dropdown(
                ['Revenue', 'Viewers', 'Score'], 
                value = 'Revenue',
                id = 'dropdown_bar_measure',
                style={'width': '90vh', 'display': 'inline-block'}),
            dcc.Graph(
                id = 'bar_plot',
                figure = bar_plot(df = df, name_of_category_column = 'Жанр', name_of_measerment_column = 'Сборы в мире', title_name = 'The average Revenue of top films by genre'),
            )])

@callback(
    Output('viewers_per_year', 'figure'),
    Input('slider_years', 'value')
)

def update_graph(years_list):
    dff = df[(df['Год производства']>= years_list[0]) & (df['Год производства']<= years_list[1])]
    viewers_per_year = dff.groupby('Год производства')['Зрители'].max()
    fig = px.line(viewers_per_year)
    return fig

@callback(
    Output('number_of_films', 'figure'),
    Input('dropdown_pie', 'value')
)

def update_count_plot(category):
    if category == 'Genres':
        cols = 'Жанр: '
        title_name = 'The percentage of top films by genre'
    else:
        cols = 'Страна: '
        title_name = 'The percentage of top films by country'
    dictionary = {col.split(': ')[1]: df[df[col]==True]['Название фильма'].count() for col in df.columns if cols in col}
    dictionary = dict(sorted(dictionary.items(), key=lambda x:x[1], reverse=True))
    df_small = pd.melt(pd.DataFrame(dictionary, index=[0]))
    df.small = df_small.loc[(df_small['value']/df_small['value'].sum())<0.04, 'variable'] = 'другие'
    figure_count = px.pie(data_frame=df_small, names=df_small['variable'], values=df_small['value'], title=title_name)
    return figure_count

@callback(
    Output('bar_plot', 'figure'),
    Input('dropdown_bar_category', 'value'),
    Input('dropdown_bar_measure', 'value')
)

def update_bar_plot(category, measure):
    if measure == 'Revenue':
        measure_col = 'Сборы в мире'
        title_name = 'The average Revenue of top films'
    elif measure == 'Viewers':
        measure_col = 'Зрители'
        title_name = 'The average number of viewers of top films'
    else:
        measure_col = 'Оценка фильма'
        title_name = 'The average score of top top films'
    if category == 'Genres':
        cat_col = 'Жанр'
        title_name = title_name + ' by genre'
    else:
        cat_col = 'Страна'
        title_name = title_name + ' by country'
    fig = bar_plot(df= pd.read_csv('KinoPoisk_processed'), name_of_category_column=cat_col, name_of_measerment_column=measure_col, title_name=title_name)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)