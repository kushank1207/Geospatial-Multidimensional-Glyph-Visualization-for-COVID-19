import pandas as pd
import plotly.express as px

def fig_task_1(country, continent, COVID_df):
    if country:
        data = COVID_df[COVID_df['location'].isin(country)]
        land_data = country
    else:
        data = COVID_df[COVID_df['continent'].isin(continent)]
        land_data = continent

    color_list = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Dark2
    color_dict = {land_data[index]: color_list[index]   for index in range(len(land_data))}

    fig_task_1 = px.line(data, x='date', y='stringency_index',
               labels={'date': 'Date', 'stringency_index': 'Government stringency index (0-100)',
                        'total_cases': 'Total confirmed cases', 'total_deaths': 'Total deaths', 
                        'new_cases': 'New confirmed cases', 'new_deaths': 'New deaths'},
               color='location', color_discrete_map=color_dict,
               hover_data=['total_cases', 'total_deaths', 'new_cases', 'new_deaths'],
               title='Line Graphs for Multivariate Data', height=700)
    return fig_task_1