import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


from core.task_1 import fig_task_1
from core.task_2 import fig_task_2
from core.task_3 import fig_task_3



# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' start.
data_set_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
covid19_data_frame_all = pd.read_csv("data/owid-covid-data.csv")
covid19_data_frame = covid19_data_frame_all.loc[
    covid19_data_frame_all['continent'] == 'Africa']  # Filter out data based on Europe continent.
# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' End.

covid19_data_frame_na = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'North America']

covid19_data_frame_sa = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'South America']

covid19_data_frame_eu = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'Europe']

covid19_data_frame_af = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'Africa']

covid19_data_frame_a = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'Asia']


# CSS stylesheet for dash start.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# CSS stylesheet for dash end.

# Task 1 from the concept paper start.
# Coded by Varun Nandkumar Golani

countries_in_africa = covid19_data_frame['location'].unique().tolist()

# Creating color dictionary by combining different discrete plotly maps
color_list = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Dark2
color_dict = {countries_in_africa[index]: color_list[index]
              for index in range(len(countries_in_africa))}

fig_dash_world = px.choropleth(covid19_data_frame, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.OrRd, 
                    scope ="world", 
                    animation_frame ="date")

fig_dash_na = px.choropleth(covid19_data_frame_na, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.Burg, 
                    scope ="north america", 
                    animation_frame ="date")

fig_dash_sa = px.choropleth(covid19_data_frame_sa, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.dense, 
                    scope ="south america", 
                    animation_frame ="date")

fig_dash_eu = px.choropleth(covid19_data_frame_eu, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.Aggrnyl,
                    scope ="europe", 
                    animation_frame ="date")

fig_dash_af = px.choropleth(covid19_data_frame_af, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.Agsunset, 
                    scope ="africa", 
                    animation_frame ="date")

fig_dash_a = px.choropleth(covid19_data_frame_a, 
                    locations ="iso_code", 
                    color ="total_cases", 
                    hover_name ="location",  
                    color_continuous_scale = px.colors.sequential.turbid, 
                    scope ="asia", 
                    animation_frame ="date")



# Task 3 from the concept paper start.
# Coded by Varun Nandkumar Golani

recent_tests_data_frame = pd.DataFrame(columns=['location', 'total_tests', 'date'])
for country in countries_in_africa:
    country_recent_data = covid19_data_frame.loc[(covid19_data_frame['location'] == country)
                                                 & pd.notnull(covid19_data_frame['total_tests']),
                                                 ['location', 'total_tests', 'date']]
    if not country_recent_data.empty:
        recent_tests_data_frame1 = pd.concat([recent_tests_data_frame, country_recent_data.iloc[[-1]]])

fig4 = px.pie(recent_tests_data_frame, values='total_tests', names='location', title='Pie Chart'
              , color='location', color_discrete_map=color_dict, hover_data=['date']
              , labels={'location': 'African country', 'date': 'Recent data available date',
                        'total_tests': 'Total tests'}, height=700)

fig4.update_traces(textposition='inside', textinfo='percent+label'
                   , hovertemplate='Total tests: %{value} <br>Recent data available date,' +
                                   'African country: %{customdata}</br>')
# Task 3 from the concept paper end.

# Task 4 from the concept paper Start.
# coded by Sanjay Gupta

iso_code_list = covid19_data_frame["iso_code"].unique().tolist()
iso_code_color_dict = {iso_code_list[index]: color_list[index] for index in range(len(iso_code_list))}


def calculate_covid19_death_rate(data_frame):
    death_rate_data = []
    for item in range(len(data_frame)):
        death_rate_data.append(
            round(((data_frame["total_deaths"].iloc[[item]] / data_frame["total_cases"].iloc[[item]]) * 100), 2))
    return death_rate_data


def select_recent_data_for_each_countries(data_frame, code_list):
    death_rate_data_frame = pd.DataFrame(columns=['iso_code', 'location', 'date', 'total_cases',
                                                  'new_cases', 'total_deaths', 'new_deaths'])
    for iso_code in code_list:
        recent_data_of_countries = data_frame.loc[(data_frame['iso_code'] == iso_code)
                                                  & pd.notnull(data_frame['total_deaths'])
                                                  & pd.notnull(data_frame['total_cases']),
                                                  ['iso_code', 'location', 'date', 'total_cases',
                                                   'new_cases', 'total_deaths', 'new_deaths']]

        if not recent_data_of_countries.empty:
            death_rate_data_frame = pd.concat([death_rate_data_frame, recent_data_of_countries.iloc[[-1]]])

    death_rate_data_frame['covid19_death_rate'] = calculate_covid19_death_rate(death_rate_data_frame)

    return death_rate_data_frame


recent_death_rate_data_frame = select_recent_data_for_each_countries(covid19_data_frame, iso_code_list)

fig5 = px.choropleth(recent_death_rate_data_frame, color='iso_code', locations='iso_code',
                     hover_name='location', hover_data=['date', 'covid19_death_rate', 'total_deaths', 'total_cases'],
                     labels={'iso_code': 'ISO code', 'date': 'Date', 'location': 'african country',
                             'total_cases': 'Total confirmed cases', 'total_deaths': 'Total deaths',
                             'covid19_death_rate': 'COVID-19 Death rate(%)'},
                     scope="africa", color_discrete_map=iso_code_color_dict)
fig5.update_geos(fitbounds="locations", lataxis_showgrid=True, lonaxis_showgrid=True)
fig5.update_layout(height=700, title='Choropleth map (africa)')
# Task 4 from the concept paper End.

# Dash code start.
app.layout = html.Div([
    html.H1(
        children='Geospatial Multidimensional Glyph Visualization for COVID-19',
        style={
            'textAlign': 'center'}
    ),
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label='World', value='tab-1'),
        dcc.Tab(label='North America', value='tab-2'),
        dcc.Tab(label='South America', value='tab-3'),
        dcc.Tab(label='Europe', value='tab-4'),
        dcc.Tab(label='Africa', value='tab-5'),
        dcc.Tab(label='Asia', value='tab-6'),
        dcc.Tab(label='Australia', value='tab-7')
    ]),
    html.Div(id="tabs-content"),

    dcc.Tabs(id="buttons", value="button-1", children=[
        dcc.Tab(label='Line chart', value='button-1'),
        dcc.Tab(label='Parallel coordinate', value='button-2'),
        dcc.Tab(label='Pie chart', value='button-3')
    ]),
    html.Div(id="tabs-content2"),
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_world)])
    elif tab == 'tab-2':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_na)])
    elif tab == 'tab-3':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_sa)])
    elif tab == 'tab-4':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_eu)])
    elif tab == 'tab-5':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_af)])
    elif tab == 'tab-6':
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_a)])

    

@app.callback(Output('tabs-content2', 'children'),
              [Input('buttons', 'value')])
def render_content(tab):
    if tab == 'button-1':
        fig1 = fig_task_1(["India", "Ukraine"], "", COVID_df=covid19_data_frame_all)
        # fig1 = fig_task_1("", continent = ["Asia"], COVID_df=covid19_data_frame_all)
        return html.Div([dcc.Graph(id='line-graph', figure=fig1)])
    #     return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_world)])
    elif tab == 'button-2':
        fig2 = fig_task_2(["India", "Ukraine"], "", COVID_df=covid19_data_frame_all)
        return html.Div([dcc.Graph(id='parallel-coordinates', figure=fig2)])
    elif tab == 'tab-3':
        return html.Div([dcc.Graph(id='pie-chart', figure=fig3)])
    else:
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig4)])




if __name__ == '__main__':
    app.run_server(debug=True)


    # # Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' start.
# data_set_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
# covid19_data_frame_all = pd.read_csv("data/owid-covid-data.csv")
# covid19_data_frame = covid19_data_frame_all.loc[
#     covid19_data_frame_all['continent'] == 'Europe']  # Filter out data based on Europe continent.
# # Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' End.

# covid19_data_frame_na = covid19_data_frame.loc[
#     covid19_data_frame['continent'] == 'North America']

# covid19_data_frame_sa = covid19_data_frame.loc[
#     covid19_data_frame['continent'] == 'South America']

# covid19_data_frame_eu = covid19_data_frame.loc[
#     covid19_data_frame['continent'] == 'Europe']

# covid19_data_frame_af = covid19_data_frame.loc[
#     covid19_data_frame['continent'] == 'Africa']

# covid19_data_frame_a = covid19_data_frame.loc[
#     covid19_data_frame['continent'] == 'Asia']


# # CSS stylesheet for dash start.
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# # CSS stylesheet for dash end.

# # Task 1 from the concept paper start.
# # Coded by Varun Nandkumar Golani

# countries_in_europe = covid19_data_frame['location'].unique().tolist()

# # Creating color dictionary by combining different discrete plotly maps
# color_list = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Dark2
# color_dict = {countries_in_europe[index]: color_list[index]
#               for index in range(len(countries_in_europe))}

# fig_dash_world = px.choropleth(covid19_data_frame, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.OrRd, 
#                     scope ="world", 
#                     animation_frame ="date")

# fig_dash_na = px.choropleth(covid19_data_frame_na, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.Burg, 
#                     scope ="north america", 
#                     animation_frame ="date")

# fig_dash_sa = px.choropleth(covid19_data_frame_sa, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.dense, 
#                     scope ="south america", 
#                     animation_frame ="date")

# fig_dash_eu = px.choropleth(covid19_data_frame_eu, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.Aggrnyl,
#                     scope ="europe", 
#                     animation_frame ="date")

# fig_dash_af = px.choropleth(covid19_data_frame_af, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.Agsunset, 
#                     scope ="africa", 
#                     animation_frame ="date")

# fig_dash_a = px.choropleth(covid19_data_frame_a, 
#                     locations ="iso_code", 
#                     color ="total_cases", 
#                     hover_name ="location",  
#                     color_continuous_scale = px.colors.sequential.turbid, 
#                     scope ="asia", 
#                     animation_frame ="date")



# # Task 3 from the concept paper start.
# # Coded by Varun Nandkumar Golani

# recent_tests_data_frame = pd.DataFrame(columns=['location', 'total_tests', 'date'])
# for country in countries_in_europe:
#     country_recent_data = covid19_data_frame.loc[(covid19_data_frame['location'] == country)
#                                                  & pd.notnull(covid19_data_frame['total_tests']),
#                                                  ['location', 'total_tests', 'date']]
#     if not country_recent_data.empty:
#         recent_tests_data_frame = pd.concat([recent_tests_data_frame, country_recent_data.iloc[[-1]]])

# fig3 = px.pie(recent_tests_data_frame, values='total_tests', names='location', title='Pie Chart'
#               , color='location', color_discrete_map=color_dict, hover_data=['date']
#               , labels={'location': 'European country', 'date': 'Recent data available date',
#                         'total_tests': 'Total tests'}, height=700)

# fig3.update_traces(textposition='inside', textinfo='percent+label'
#                    , hovertemplate='Total tests: %{value} <br>Recent data available date,' +
#                                    'European country: %{customdata}</br>')
# # Task 3 from the concept paper end.

# # Task 4 from the concept paper Start.
# # coded by Sanjay Gupta

# iso_code_list = covid19_data_frame["iso_code"].unique().tolist()
# iso_code_color_dict = {iso_code_list[index]: color_list[index] for index in range(len(iso_code_list))}


# def calculate_covid19_death_rate(data_frame):
#     death_rate_data = []
#     for item in range(len(data_frame)):
#         death_rate_data.append(
#             round(((data_frame["total_deaths"].iloc[[item]] / data_frame["total_cases"].iloc[[item]]) * 100), 2))
#     return death_rate_data


# def select_recent_data_for_each_countries(data_frame, code_list):
#     death_rate_data_frame = pd.DataFrame(columns=['iso_code', 'location', 'date', 'total_cases',
#                                                   'new_cases', 'total_deaths', 'new_deaths'])
#     for iso_code in code_list:
#         recent_data_of_countries = data_frame.loc[(data_frame['iso_code'] == iso_code)
#                                                   & pd.notnull(data_frame['total_deaths'])
#                                                   & pd.notnull(data_frame['total_cases']),
#                                                   ['iso_code', 'location', 'date', 'total_cases',
#                                                    'new_cases', 'total_deaths', 'new_deaths']]

#         if not recent_data_of_countries.empty:
#             death_rate_data_frame = pd.concat([death_rate_data_frame, recent_data_of_countries.iloc[[-1]]])

#     death_rate_data_frame['covid19_death_rate'] = calculate_covid19_death_rate(death_rate_data_frame)

#     return death_rate_data_frame


# recent_death_rate_data_frame = select_recent_data_for_each_countries(covid19_data_frame, iso_code_list)

# fig4 = px.choropleth(recent_death_rate_data_frame, color='iso_code', locations='iso_code',
#                      hover_name='location', hover_data=['date', 'covid19_death_rate', 'total_deaths', 'total_cases'],
#                      labels={'iso_code': 'ISO code', 'date': 'Date', 'location': 'European country',
#                              'total_cases': 'Total confirmed cases', 'total_deaths': 'Total deaths',
#                              'covid19_death_rate': 'COVID-19 Death rate(%)'},
#                      scope="europe", color_discrete_map=iso_code_color_dict)
# fig4.update_geos(fitbounds="locations", lataxis_showgrid=True, lonaxis_showgrid=True)
# fig4.update_layout(height=700, title='Choropleth map (Europe)')
# # Task 4 from the concept paper End.

# # Dash code start.
# app.layout = html.Div([
#     html.H1(
#         children='Geospatial Multidimensional Glyph Visualization for COVID-19',
#         style={
#             'textAlign': 'center'}
#     ),
#     dcc.Tabs(id="tabs", value="tab-1", children=[
#         dcc.Tab(label='World', value='tab-1'),
#         dcc.Tab(label='North America', value='tab-2'),
#         dcc.Tab(label='South America', value='tab-3'),
#         dcc.Tab(label='Europe', value='tab-4'),
#         dcc.Tab(label='Africa', value='tab-5'),
#         dcc.Tab(label='Asia', value='tab-6'),
#         dcc.Tab(label='Australia', value='tab-7')
#     ]),
#     html.Div(id="tabs-content"),

#     dcc.Tabs(id="buttons", value="button-1", children=[
#         dcc.Tab(label='Line chart', value='button-1'),
#         dcc.Tab(label='Parallel coordinate', value='button-2'),
#         dcc.Tab(label='Pie chart', value='button-3')
#     ]),
#     html.Div(id="tabs-content2"),
# ])


# @app.callback(Output('tabs-content', 'children'),
#               [Input('tabs', 'value')])
# def render_content(tab):
#     if tab == 'tab-1':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_world)])
#     elif tab == 'tab-2':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_na)])
#     elif tab == 'tab-3':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_sa)])
#     elif tab == 'tab-4':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_eu)])
#     elif tab == 'tab-5':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_af)])
#     elif tab == 'tab-6':
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_a)])

    

# @app.callback(Output('tabs-content2', 'children'),
#               [Input('buttons', 'value')])
# def render_content(tab):
#     if tab == 'button-1':
#         fig1 = fig_task_1(["India", "Ukraine"], "", COVID_df=covid19_data_frame_all)
#         fig1 = fig_task_1("", continent = ["Asia"], COVID_df=covid19_data_frame_all)
#         return html.Div([dcc.Graph(id='line-graph', figure=fig1)])
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig_dash_world)])
#     elif tab == 'button-2':
#         fig2 = fig_task_2(["India", "Ukraine"], "", COVID_df=covid19_data_frame_all)
#         return html.Div([dcc.Graph(id='parallel-coordinates', figure=fig2)])
#     elif tab == 'tab-3':
#         return html.Div([dcc.Graph(id='pie-chart', figure=fig3)])
#     else:
#         return html.Div([dcc.Graph(id='choropleth-map', figure=fig4)])

# if __name__ == '__main__':
#     app.run_server(debug=True)

# To view the dash output just open the link http://127.0.0.1:8050/ in the browser
# Dash code end.