from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('KinoPoisk_processed')
app = Dash()

viewers_per_year = df.groupby('Год производства')['Зрители'].max()
list_years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
years = [
    df['Год производства'].min(),
    *list_years,
    df['Год производства'].max()
]
fig = px.line(
    viewers_per_year,
    title='Maximum number of viewers per year of production'
)


def count_plot(df, name_of_category_column, title_name):
    cols = name_of_category_column+': '
    dictionary = {
        col.split(': ')[1]: df[df[col] == True]['Название фильма'].count()
        for col in df.columns if cols in col
    }
    dictionary = dict(
        sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    )

    df_small = pd.melt(pd.DataFrame(dictionary, index=[0]))
    condition = (df_small['value']/df_small['value'].sum()) < 0.04
    df.small = df_small.loc[condition, 'variable'] = 'другие'

    figure_count = px.pie(
        data_frame=df_small,
        names=df_small['variable'],
        values=df_small['value'],
        title=title_name
    )

    return figure_count


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(children='KinoPoisk Dashboard (top films)'),
                dcc.RangeSlider(
                    min=df['Год производства'].min(),
                    max=df['Год производства'].max(),
                    id='slider_years',
                    marks={int(year): {'label': str(year)} for year in years},
                    value=[df['Год производства'].min(
                    ), df['Год производства'].max()],
                    step=1
                ),
                dcc.Graph(id='viewers_per_year', figure=fig)
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    ['Genres', 'Countries'],
                    value='Genres',
                    id='dropdown'
                ),
                dcc.Graph(
                    id='number_of_films',
                    figure=count_plot(
                        df=df,
                        name_of_category_column='Жанр',
                        title_name='The percentage of top films by genre'
                    )
                )
            ]
        ),
    ]
)


@callback(
    Output('viewers_per_year', 'figure'),
    Input('slider_years', 'value')
)
def update_graph(years_list):
    dff = df[
        (df['Год производства'] >= years_list[0]) &
        (df['Год производства'] <= years_list[1])
    ]
    viewers_per_year = dff.groupby('Год производства')['Зрители'].max()
    fig = px.line(viewers_per_year)

    return fig


@callback(
    Output('number_of_films', 'figure'),
    Input('dropdown', 'value')
)
def update_count_plot(category):
    if category == 'Genres':
        cols = 'Жанр: '
        title_name = 'The percentage of top films by genre'
    else:
        cols = 'Страна: '
        title_name = 'The percentage of top films by country'

    dictionary = {
        col.split(': ')[1]: df[df[col] == True]['Название фильма'].count()
        for col in df.columns if cols in col
    }
    dictionary = dict(
        sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    )

    df_small = pd.melt(pd.DataFrame(dictionary, index=[0]))
    condition = (df_small['value']/df_small['value'].sum()) < 0.04
    df.small = df_small.loc[condition, 'variable'] = 'другие'

    figure_count = px.pie(
        data_frame=df_small,
        names=df_small['variable'],
        values=df_small['value'],
        title=title_name
    )

    return figure_count


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
