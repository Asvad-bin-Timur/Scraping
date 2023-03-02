import pandas as pd
import numpy as np
import plotly.express as px
import re


def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
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
    
    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")
    
    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]
            
    return new_tick_format

def show_values(axs, orient="v", space=0):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = reformat_large_tick_values(p.get_height(), 0)
                ax.text(_x, _y, value, ha="center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = reformat_large_tick_values(p.get_width(), 0)
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

def bar_plot(df, name_of_category_column, name_of_measerment_column, title_name, aggregation_func='mean', scale_of_axis=None):
    all_categories = []
    for record in df[name_of_category_column]:
        new_record = record.split(',')
        for word in new_record:
            word = word.strip()
        all_categories.append(word)
    all_categories = list(set(all_categories))
    if aggregation_func == 'mean':
        measurement_by_category = {category: df[df[name_of_category_column].str.contains(re.escape(category))][name_of_measerment_column].mean()
                                   for category in all_categories}
    elif aggregation_func == 'median':
        measurement_by_category = {category: df[df[name_of_category_column].str.contains(category)][name_of_measerment_column].median() 
                                   for category in all_categories}
    dictionary = dict(sorted(measurement_by_category.items(), 
                                key=lambda x:x[1], 
                                reverse=False))
    df_small = pd.melt(pd.DataFrame(dictionary, 
                                    index=[0]))
    df_small.loc[(df_small['value']/df_small['value'].sum())<0.03, 'variable'] = 'другое'
    df_small.loc[len(df_small.index)] = ['другие', df_small[df_small['variable']=='другое']['value'].sum()] 
    df_small.drop(df_small[df_small['variable']=='другое'].index, 
                  inplace=True)
    df_small = df_small.sort_values(by=['value'], 
                                    ascending=True)
    fig = px.histogram(data_frame=df_small,
                       y='variable', 
                       x='value', 
                       title=title_name, 
                       text_auto='.2s')
    fig.update_layout(barmode='stack', 
                      xaxis={'categoryorder': 'total descending', 
                             'visible': False, 
                             'showticklabels' : False}, 
                      yaxis={'visible': True, 
                             'title' : None, 
                             'showticklabels' : True},
                      xaxis_range=scale_of_axis,
                      width=600,
                      height=600,
                      title={'x':0.5,
                             'xanchor': 'center'}
                      )
    return fig


def count_plot(df, name_of_category_column, title_name):
    all_categories = []
    for record in df[name_of_category_column]:
        new_record = record.split(',')
        for word in new_record:
            word = word.strip()
        all_categories.append(word)
    all_categories = list(set(all_categories))
    dictionary = {category: df[df[name_of_category_column].str.contains(re.escape(category))]['Название фильма'].count()
              for category in all_categories}
    dictionary = dict(sorted(dictionary.items(), 
                             key=lambda x:x[1], 
                             reverse=True))
    df_small = pd.melt(pd.DataFrame(dictionary, 
                                    index=[0]))
    df_small.loc[(df_small['value']/df_small['value'].sum())<0.04, 
                 'variable'] = 'другие'
    fig = px.pie(data_frame=df_small, 
                 names=df_small['variable'], 
                 values=df_small['value'], 
                 title=title_name)
    fig.update_layout(title={'x':0.5,
                             'xanchor': 'center'},
                      width=500,
                      height=450)
    return fig



