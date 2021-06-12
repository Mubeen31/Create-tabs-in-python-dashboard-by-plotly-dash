import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('gapminderDataFiveYear.csv'))

year_list = list(data['year'].unique())

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "1.3vh",
    "color": '#AEAEAE',
    "fontSize": '.9vw',
    "backgroundColor": '#010914',
    'border-bottom': '1px white solid',

}

tab_selected_style = {
    "fontSize": '.9vw',
    "color": '#F4F4F4',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '0px 0px 0px 0px',
}

tab_selected_style1 = {
    "fontSize": '.9vw',
    "color": '#F4F4F4',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '0px 0px 0px 0px',
}

life_expectancy = dcc.Graph(id = 'line_chart1',
                            config = {'displayModeBar': False}, className = 'line_chart_width')
population = dcc.Graph(id = 'line_chart2',
                       config = {'displayModeBar': False}, className = 'line_chart_width')
gdp_per_cap = dcc.Graph(id = 'line_chart3',
                        config = {'displayModeBar': False}, className = 'line_chart_width')

life_expectancy_bar = dcc.Graph(id = 'bar_chart1',
                                config = {'displayModeBar': False}, className = 'bar_chart_height')
population_bar = dcc.Graph(id = 'bar_chart2',
                           config = {'displayModeBar': False}, className = 'bar_chart_height')
gdp_per_cap_bar = dcc.Graph(id = 'bar_chart3',
                            config = {'displayModeBar': False}, className = 'bar_chart_height')



app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.P('', className = 'fix_label', style = {'color': 'white'}),
                html.P('Select Continent:', className = 'fix_label', style = {'color': 'white'}),
                html.P('Select Country:', className = 'fix_label', style = {'color': 'white'}),
            ], className = 'adjust_title'),
            html.Div([
                html.H5('World Countries Information 1952 - 2007', className = 'title_text'),

                dcc.Dropdown(id = 'select_continent',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             value = 'Asia',
                             placeholder = 'Select Continent',
                             options = [{'label': c, 'value': c}
                                        for c in data['continent'].unique()], className = 'dcc_compon'),

                dcc.Dropdown(id = 'select_countries',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select Country',
                             options = [], className = 'dcc_compon'),

            ], className = 'adjust_drop_down_lists')
        ], className = "title_container twelve columns")
    ], className = "row flex-display"),

    html.Div([
        html.Div([
            dcc.Tabs(id = "tabs-styled-with-inline", value = 'population', children = [
                dcc.Tab(life_expectancy,
                        label = 'Life Expectancy',
                        value = 'life_expectancy',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        className = 'font_size'),
                dcc.Tab(population,
                        label = 'Population',
                        value = 'population',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        className = 'font_size'),
                dcc.Tab(gdp_per_cap,
                        label = 'gdpPercap',
                        value = 'gdp_per_cap',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        className = 'font_size'),
            ], style = tabs_styles,
                     colors = {"border": None,
                               "primary": None,
                               "background": None}, className = 'tabs_width'),

        ], className = 'create_container six columns'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div(id = 'text1', className = 'grid_height'),
                    html.Div(id = 'text2', className = 'grid_height'),
                    html.Div(id = 'text3', className = 'grid_height'),
                ], className = 'grid_one_column'),

                dcc.Tabs(id = "tabs-styled-with-inline1", value = 'population', children = [
                    dcc.Tab(life_expectancy_bar,
                            label = 'Life Expectancy',
                            value = 'life_expectancy',
                            style = tab_style,
                            selected_style = tab_selected_style1,
                            className = 'font_size'),
                    dcc.Tab(population_bar,
                            label = 'Population',
                            value = 'population',
                            style = tab_style,
                            selected_style = tab_selected_style1,
                            className = 'font_size'),
                    dcc.Tab(gdp_per_cap_bar,
                            label = 'gdpPercap',
                            value = 'gdp_per_cap',
                            style = tab_style,
                            selected_style = tab_selected_style1,
                            className = 'font_size'),
                ], style = tabs_styles,
                         colors = {"border": None,
                                   "primary": None,
                                   "background": None}),

            ], className = 'adjust_grids')
        ], className = 'create_container six columns')

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('select_countries', 'options'),
    Input('select_continent', 'value'))
def get_country_options(select_continent):
    data1 = data[data['continent'] == select_continent]
    return [{'label': i, 'value': i} for i in data1['country'].unique()]


@app.callback(
    Output('select_countries', 'value'),
    Input('select_countries', 'options'))
def get_country_value(select_countries):
    return [k['value'] for k in select_countries][0]



@app.callback(Output('line_chart1', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def update_graph(select_continent, select_countries):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent) & (data1['country'] == select_countries)]

    return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['lifeExp'],
                mode = 'text + markers + lines',
                text = data2['lifeExp'],
                texttemplate = '%{text:.0f}',
                textposition = 'bottom right',
                line = dict(width = 3, color = '#38D56F'),
                marker = dict(size = 10, symbol = 'circle', color = '#38D56F',
                              line = dict(color = '#38D56F', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Life Expectancy</b>: ' + [f'{x:,.3f}' for x in data2['lifeExp']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>Life expectancy' + ' ' + 'in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#38D56F',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b>Life Expectancy</b>',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }


@app.callback(Output('line_chart2', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def update_graph(select_continent, select_countries):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()

    data2 = data1[(data1['continent'] == select_continent) & (data1['country'] == select_countries)]

    return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['pop'],
                mode = 'text + markers + lines',
                text = data2['pop'],
                texttemplate = '%{text:,.2s}',
                textposition = 'top center',
                line = dict(width = 3, color = '#9A38D5'),
                marker = dict(size = 10, symbol = 'circle', color = '#9A38D5',
                              line = dict(color = '#9A38D5', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Population</b>: ' + [f'{x:,.0f}' for x in data2['pop']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>Population' + ' ' + 'in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#9A38D5',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b>Population</b>',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(Output('line_chart3', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def update_graph(select_continent, select_countries):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()

    data2 = data1[(data1['continent'] == select_continent) & (data1['country'] == select_countries)]

    return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['gdpPercap'],
                mode = 'text + markers + lines',
                text = data2['gdpPercap'],
                texttemplate = '%{text:,.0f}',
                textposition = 'bottom right',
                line = dict(width = 3, color = '#FFA07A'),
                marker = dict(size = 10, symbol = 'circle', color = '#FFA07A',
                              line = dict(color = '#FFA07A', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>gdpPercap</b>: ' + [f'{x:,.6f}' for x in data2['gdpPercap']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>gdpPercap' + ' ' + 'in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#FFA07A',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b>gdpPercap</b>',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(Output('text1', 'children'),
              [Input('select_continent', 'value')])

def update_text(select_continent):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(1, columns = ['pop'])
    data_continent = data2['continent'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_pop = data2['pop'].iloc[0]

    return [

               html.H6('Top country by population in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6',
                                'margin-top': '15px'}
                       ),

               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '20px'
                               }
                      ),
               html.P('Population:' + '  ' + '{0:,.0f}'.format(top_pop),
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]

@app.callback(Output('text2', 'children'),
              [Input('select_continent', 'value')])

def update_text(select_continent):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(1, columns = ['lifeExp'])
    data_continent = data2['continent'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_lifeexp = data2['lifeExp'].iloc[0]

    return [

               html.H6('Top country by life expectancy in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6',
                                'margin-top': '15px'}
                       ),
               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '20px'
                               }
                      ),
               html.P('Life Expectancy:' + '  ' + '{0:,.0f}'.format(top_lifeexp),
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]

@app.callback(Output('text3', 'children'),
              [Input('select_continent', 'value')])

def update_text(select_continent):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(1, columns = ['gdpPercap'])
    data_continent = data2['continent'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_gdppercap = data2['gdpPercap'].iloc[0]

    return [

               html.H6('Top country by gdpPercap in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6',
                                'margin-top': '15px'}
                       ),
               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '20px'
                               }
                      ),
               html.P('gdpPercap:' + '  ' + '{0:,.0f}'.format(top_gdppercap),
                      style = {'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]

@app.callback(Output('bar_chart1', 'figure'),
              [Input('select_continent', 'value')])
def update_graph(select_continent):
    data1 = data.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].mean().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(10, columns = ['lifeExp'])

    return {
        'data':[
            go.Bar(
                x = data2['lifeExp'],
                y = data2['country'],
                text = data2['lifeExp'],
                texttemplate = '%{text:.0f}',
                textposition = 'outside',
                orientation = 'h',
                marker = dict(color = '#38D56F'),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Life Expectancy</b>: ' + [f'{x:,.3f}' for x in data2['lifeExp']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>Top countries by Life Expectancy' + ' ' + 'in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#38D56F',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 35, r = 0, l = 130),

             xaxis = dict(title = '<b>Life Expectancy</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b></b>',
                          autorange = 'reversed',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(Output('bar_chart2', 'figure'),
              [Input('select_continent', 'value')])
def update_graph(select_continent):
    data1 = data.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].mean().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(10, columns = ['pop'])

    return {
        'data':[
            go.Bar(
                x = data2['pop'],
                y = data2['country'],
                text = data2['pop'],
                texttemplate = '%{text:.2s}',
                textposition = 'auto',
                orientation = 'h',
                marker = dict(color = '#9A38D5'),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Population</b>: ' + [f'{x:,.3f}' for x in data2['pop']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>Top countries by Population' + ' ' + 'in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#9A38D5',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 35, r = 0, l = 130),

             xaxis = dict(title = '<b>Life Expectancy</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b></b>',
                          autorange = 'reversed',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(Output('bar_chart3', 'figure'),
              [Input('select_continent', 'value')])
def update_graph(select_continent):
    data1 = data.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].mean().reset_index()
    data2 = data1[(data1['continent'] == select_continent)].nlargest(10, columns = ['gdpPercap'])

    return {
        'data':[
            go.Bar(
                x = data2['gdpPercap'],
                y = data2['country'],
                text = data2['gdpPercap'],
                texttemplate = '%{text:.0f}',
                textposition = 'auto',
                orientation = 'h',
                marker = dict(color = '#FFA07A'),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>gdpPercap</b>: ' + [f'{x:,.3f}' for x in data2['gdpPercap']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010914',
             paper_bgcolor='#010914',
             title={
                'text': '<b>Top countries by gdpPercap' + ' ' + 'in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#FFA07A',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 35, r = 0, l = 130),

             xaxis = dict(title = '<b>gdpPercap</b>',
                          visible = True,
                          color = 'white',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             yaxis = dict(title = '<b></b>',
                          autorange = 'reversed',
                          visible = True,
                          color = 'white',
                          showline = False,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'white',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

             legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)