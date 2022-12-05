import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def fig_task_2(country, continent, COVID_df):
    imp_cols = ['location', 'total_cases', 'total_deaths', 'date', 'population','hospital_beds_per_thousand', 'gdp_per_capita', 'life_expectancy']

    recent_deaths_data_frame = pd.DataFrame(columns=imp_cols)
    if country:
        data = COVID_df[COVID_df['location'].isin(country)]
        all_countries = country
    else:
        data = COVID_df[COVID_df['continent'].isin(continent)]
        all_countries = data['location'].unique().tolist()

    data = data.dropna(axis = 0, subset = ["total_deaths", "total_cases"])

    for country_ in all_countries:
        # recent_data = land_data.loc[(covid19_data_frame['location'] == country_)
        #                                     & pd.notnull(covid19_data_frame['total_deaths']) & pd.notnull(
        #     covid19_data_frame['total_cases']),imp_cols]

        recent_data = data.loc[data['location'] == country_ , imp_cols]
        if not recent_data.empty:
            recent_deaths_data_frame = pd.concat([recent_deaths_data_frame, recent_data.iloc[[-1]]])
    

# adding death rates to the data frame 'recent_deaths_data_frame'
    covid19_death_rate = []
    for i in range(0, len(recent_deaths_data_frame)):
        covid19_death_rate.append(
            (recent_deaths_data_frame['total_deaths'].iloc[i] / recent_deaths_data_frame['total_cases'].iloc[i]) * 100)

    recent_deaths_data_frame['covid19_death_rate'] = recent_deaths_data_frame['total_deaths'] / recent_deaths_data_frame['total_cases'] * 100
    recent_deaths_data_frame.fillna(0)

    # getting number of countries for color
    c = [i for i in range(0, len(all_countries))]

    # Allocating the countries unique numbers
    lookup = dict(zip(all_countries, c))
    num = []
    for i in recent_deaths_data_frame['location']:
        if i in lookup.keys():
            num.append(lookup[i])

    # plotting Parallel Coordinates for the data frame
    fig2 = go.Figure(data=go.Parcoords(
        line=dict(color=num, colorscale='HSV', showscale=False, cmin=0,  cmax=len(all_countries)),
        dimensions=list([dict(range=[0, len(all_countries)],tickvals=c, ticktext=all_countries, label="countries", values=num),
            dict(range=[0, max(recent_deaths_data_frame['hospital_beds_per_thousand'])], label="Hospitals beds per 1000", values=recent_deaths_data_frame['hospital_beds_per_thousand']),
            dict(range=[0, max(recent_deaths_data_frame['median_age'])],   label='Median Age', values=recent_deaths_data_frame['median_age']),
            dict(range=[0, max(recent_deaths_data_frame['population'])],  label='Population', values=recent_deaths_data_frame['population']),
            dict(range=[0, max(recent_deaths_data_frame['gdp_per_capita'])], label='GDP Per Capita', values=recent_deaths_data_frame['gdp_per_capita']),
            dict(range=[0, max(recent_deaths_data_frame['covid19_death_rate'])], label='COVID-19 Death rate', values=recent_deaths_data_frame['covid19_death_rate']),
        ])
    ), layout=go.Layout( autosize=True, height=800, hovermode='closest', margin=dict(l=170, r=85, t=75)))

    # updating margin of the plot
    fig2.update_layout(
        title={ 'text': "Parallel Coordinates", 'y': 0.99,  'x': 0.2, 'xanchor': 'center', 'yanchor': 'top'}, font=dict(size=15, color="#000000"))
    
    return fig2



if __name__ == "__main__":
    df = pd.read_csv("../data/owid-covid-data.csv")
    country = ""
    continent = ["Asia"]
    fig_task_2(country, continent, df)

