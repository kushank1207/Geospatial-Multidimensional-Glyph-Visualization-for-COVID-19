import pandas as pd
import plotly.express as px

def fig_task_3(country, continent, COVID_df):
    if country:
        data = COVID_df[COVID_df['location'].isin(country)]
        land_data = country
    else:
        data = COVID_df[COVID_df['continent'].isin(continent)]
        land_data = data['location'].unique().tolist()


    recent_tests_data_frame = pd.DataFrame(columns=['location', 'total_tests', 'date'])

    color_list = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Dark2
    color_dict = {land_data[index]: color_list[index]   for index in range(len(land_data))}

    for country in land_data:
        # print(country)
        country_recent_data = COVID_df.loc[(COVID_df['location'] == country)
                                                 & pd.notnull(COVID_df['total_tests']),
                                                 ['location', 'total_tests', 'date']]
        if not country_recent_data.empty:
            recent_tests_data_frame = pd.concat([recent_tests_data_frame, country_recent_data.iloc[[-1]]])
    
    fig_task_3 = px.pie(recent_tests_data_frame, values='total_tests', names='location', title='Pie Chart'
              , color='location', color_discrete_map=color_dict, hover_data=['date']
              , labels={'location': 'European country', 'date': 'Recent data available date',
                        'total_tests': 'Total tests'}, height=700)

    fig_task_3.update_traces(textposition='inside', textinfo='percent+label'
                   , hovertemplate='Total tests: %{value} <br>Recent data available date,' +
                                   'European country: %{customdata}</br>')

    return fig_task_3

if __name__ == "__main__":
    df = pd.read_csv("../data/owid-covid-data.csv")
    country = ""
    continent = ["Asia"]
    print(fig_task_3(country, continent, df))