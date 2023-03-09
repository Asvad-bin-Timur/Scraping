import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import re
# from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go


def reformat_large_tick_values(
        tick_val
):
    """
    Turns large tick values (in the billions, millions and thousands)
    such as 4500 into 4.5K and also appropriately turns
    4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val/1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val/1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val/1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values
    # such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + \
                new_tick_format[index_of_decimal+2:]

    return new_tick_format


def bar_plot(
        df,
        name_of_category_column,
        name_of_measerment_column,
        title_name,
        aggregation_func='mean',
        scale_of_axis=None
):

    all_categories = []
    for record in df[name_of_category_column]:
        new_record = record.split(',')
        for word in new_record:
            word = word.strip()
        all_categories.append(word)
    all_categories = list(set(all_categories))
    if aggregation_func == 'mean':
        measurement_by_category = {
            category: df[df[name_of_category_column].str.contains(
                re.escape(category))]
            [name_of_measerment_column].mean()
            for category in all_categories
        }
    elif aggregation_func == 'median':
        measurement_by_category = {
            category: df[df[name_of_category_column].str.contains(category)]
            [name_of_measerment_column].median()
            for category in all_categories
        }
    dictionary = dict(sorted(
        measurement_by_category.items(),
        key=lambda x: x[1],
        reverse=False
    ))
    df_small = pd.melt(pd.DataFrame(
        dictionary,
        index=[0]
    ))
    mask = (df_small['value']/df_small['value'].sum()) < 0.03
    df_small.loc[mask, 'variable'] = 'другое'
    sum_small = df_small[df_small['variable'] == 'другое']['value'].sum()
    df_small.loc[len(df_small.index)] = ['другие', sum_small]
    df_small.drop(
        df_small[df_small['variable'] == 'другое'].index,
        inplace=True
    )
    df_small = df_small.sort_values(
        by=['value'],
        ascending=True
    )
    fig = px.histogram(
        data_frame=df_small,
        y='variable',
        x='value',
        title=title_name,
        text_auto='.2s'
    )
    fig.update_layout(
        barmode='stack',
        xaxis={
            'categoryorder': 'total descending',
            'visible': False,
            'showticklabels': False
        },
        yaxis={
            'visible': True,
            'title': None,
            'showticklabels': True
        },
        xaxis_range=scale_of_axis,
        width=600,
        height=600,
        title={
            'x': 0.5,
            'xanchor': 'center'
        }
    )

    return fig


def count_plot(
    df,
    name_of_category_column,
    title_name
):
    all_categories = []
    for record in df[name_of_category_column]:
        new_record = record.split(',')
        for word in new_record:
            word = word.strip()
        all_categories.append(word)
    all_categories = list(set(all_categories))
    dictionary = {
        category: df[df[name_of_category_column].str.contains(
            re.escape(category))]
        ['Название фильма'].count()
        for category in all_categories
    }
    dictionary = dict(sorted(
        dictionary.items(),
        key=lambda x: x[1],
        reverse=True
    ))
    df_small = pd.melt(pd.DataFrame(
        dictionary,
        index=[0]
    ))
    mask = (df_small['value']/df_small['value'].sum()) < 0.04
    df_small.loc[mask, 'variable'] = 'другие'
    fig = px.pie(
        data_frame=df_small,
        names=df_small['variable'],
        values=df_small['value'],
        title=title_name
    )
    fig.update_layout(
        title={
            'x': 0.5,
            'xanchor': 'center'
        },
        width=600,
        height=500,
        margin=dict(
            l=(1 - 0.8) / 2 * 600,
            r=(1 - 0.8) / 2 * 600,
            t=(1 - 0.8) / 2 * 500,
            b=(1 - 0.8) / 2 * 500
        )
    )

    return fig


def words_cloud(df, column='Слоган'):
    text = " ".join(review for review in df[column])
    stopwords = set(STOPWORDS)
    stopwords.update(["Beyond", "will", 'может'])
    wordcloud = WordCloud(
        stopwords=stopwords,
        background_color="white",
        min_word_length=4,
        collocation_threshold=10,
        scale=2,
        width=700,
        height=400
    ).generate(text)
    # get the dimensions of the word cloud image
    width, height = wordcloud.width, wordcloud.height
    # create a figure using Plotly's make_subplots function
    fig = make_subplots(rows=1, cols=1)
    # add the word cloud trace to the figure
    fig.add_trace(
        go.Image(z=wordcloud.to_array()),
        row=1, col=1
    )
    # configure the layout of the figure
    fig.update_layout(
        margin=dict(l=15, r=15, t=40, b=20),
        paper_bgcolor='white',
        width=width,
        height=height,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False)
    )
    # return the Plotly figure
    return fig


def box_plot(df, measurement_column):
    # create subplot with one row and two columns
    fig = make_subplots(rows=1, cols=1)

    # add box plot trace to first column
    fig.add_trace(
        go.Box(
            x=df[measurement_column],
            y=df['Оценка фильма'],
            orientation='h',
            name='Box Plot',
        ),
        row=1,
        col=1
    )

    # update layout
    fig.update_layout(
        title='Box Plot',
        xaxis=dict(title=measurement_column),
        yaxis=dict(title='Оценка фильма'),
        width=600,
        height=500,
        margin=dict(
            l=(1 - 0.8) / 2 * 600,
            r=(1 - 0.8) / 2 * 600,
            t=(1 - 0.8) / 2 * 500,
            b=(1 - 0.8) / 2 * 500
        ),
    )

    return fig
