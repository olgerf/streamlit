#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Covid-vs-Gaming_Julius_Slobbe_500916116_Serhat_kokcu_500858425_Bart_Kombee_500914214


# In[19]:


import numpy as np
import pandas as pd
import plotly.express as px
import requests
import plotly.graph_objects as go
import html5lin

# !pip install streamlit
# !pip install html5lib
# !pip install sodapy
# !pip install opendatasets

import streamlit as st
import opendatasets as od
import html5lib
import lxml

# import voor USA dataset, niet wereldwijd
# from sodapy import Socrata


# In[3]:


##Kaggle API imports
#korea corona data 20 Jan - 30 Juni
#od.download('https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=Time.csv')
#Korea_corona_cases = pd.read_csv('coronavirusdataset/Time.csv')


# In[4]:


od.download('https://covid19.who.int/WHO-COVID-19-global-data.csv')
worldwide_corona = pd.read_csv('WHO-COVID-19-global-data.csv', delimiter=',')

world_cases = pd.DataFrame(worldwide_corona.groupby('Date_reported', as_index=False)['Cumulative_cases'].sum())


# In[5]:


#### Loading USA corona data

#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
###client = Socrata("data.cdc.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cdc.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 58560 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
###results = client.get("9mfq-cb36", limit=58560)

# Convert to pandas DataFrame
###results_df = pd.DataFrame.from_records(results)
###results_df['submission_date'] = pd.to_datetime(results_df['submission_date'], infer_datetime_format=True)

###results_df.to_csv('Corona_USA.csv', index=False)
###results_df = pd.read_csv('Corona_USA.csv', delimiter=',')


###new_df = pd.DataFrame(results_df.groupby('submission_date', as_index=False)['tot_cases'].sum())

#save as csv en read as csv zodat het type niet meer als pandas.core.series.series


# In[6]:


pr = pd.period_range(start='2020-01',end='2022-08', freq='M')

dates = pd.DataFrame([(str(period.year) + '-' + str(period.month)) for period in pr], columns=['dates'])
dates['url']= dates['dates'].apply(lambda x: 'https://ps-timetracker.com/statistic/{0}'.format(x))

for i in range(len(dates)):
    #dates['Player count'] = pd.read_html(requests.get(dates['url'][i]).content)[-1]['Players'].sum()
    dates.at[i, 'Player count'] = pd.read_html(requests.get(dates['url'][i]).content)[-1]['Players'].sum()
PS4_concurrent_players = dates[['dates', 'Player count']]


# In[7]:


# steam data
# amount of current players for a game with appID 'X'
# can be looped for all appID's but historical data cannot be retrieved


header = {"Client-ID": "F07D7ED5C43A695B3EBB01C28B6A18E5"}

appId = 570
game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid=' + str(appId)
game_players = requests.get(game_players_url, headers=header)

print(game_players.json()['response']['player_count'])


# Luckily a steam database has been made
# https://steamdb.info/app/753/graphs/
# download concurrent players dataset, have to sign in via steam for dataset with a datapoint per day.

Steam_players = pd.read_csv('chart.csv')
Steam_players['DateTime'] = pd.to_datetime(Steam_players['DateTime'], infer_datetime_format=True)
Steam_players_corona = Steam_players[Steam_players['DateTime']>='2020-01-03']


# In[8]:


od.download('https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv')
energy_df = pd.read_csv('owid-energy-data.csv')
energy_df.drop(energy_df.loc[energy_df['year']<=2018].index, inplace=True)
energy_df.drop(energy_df.loc[energy_df['country']!='World'].index, inplace=True)
energy_df = energy_df[['electricity_demand', 'nuclear_consumption', 'primary_energy_consumption', 'renewables_consumption',]]
energy_usage = pd.DataFrame(energy_df['electricity_demand'])
energy_usage['consumption'] = energy_df['nuclear_consumption'] + energy_df['primary_energy_consumption'] + energy_df['renewables_consumption']
energy_usage['year'] = [2019, 2020, 2021]
#print(energy_df)


# In[9]:


#Resetten van index om NAN waardes te voorkomen, om dit vervolgens te combineren tot 1 dataset! Dit draagt bij tot het maken van een Scatterplot
WC1 = world_cases.reset_index(drop=True, inplace=True)
WC2 = Steam_players_corona.reset_index(drop=True, inplace=True)
#PS4_concurrent_players['dates'] = PS4_concurrent_players['dates'].apply(lambda x: '{0}-01'.format(x))
WC3 = PS4_concurrent_players.reset_index(drop=True, inplace=True)

#Stukje combineren.
WC4 = pd.concat([world_cases['Date_reported'], world_cases['Cumulative_cases'], Steam_players_corona['Users']], axis=1)
WC4.columns = ['Date', 'Corona cases', 'Steam users']
print(WC4)


# In[10]:


WC4.to_csv('Corona and steam.csv')
PS4_concurrent_players.to_csv('PS4.csv')
energy_usage.to_csv('Energy usage.csv')


# In[11]:


st.title('Online gaming vs Covid-19')


# In[12]:


# Create a simple bar chart
fig1 = px.bar(data_frame=energy_usage, x='year', y='consumption')


# Create the buttons
my_buttons = [{'label': "Bar", 'method': "update", 'args': [{"type": "bar"}]},
  {'label': "Line-figure", 'method': "update", 'args': [{"type": "line", 'mode': 'line'}]}]



# Add buttons to the plot and show
fig1.update_layout(
    
    {'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]},

)

fig1.update_layout(
    title="Energy usage (TWH)",
    xaxis_title="Time stamp",
    yaxis_title="Energy usage (TWH)",
    legend_title="Legend Title",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)
# fig1.show()



# In[13]:


# Create a simple bar chart
fig2 = px.bar(data_frame=WC4, x='Date', y='Steam users')

#annotations
value_annotations=[{'text': 'Peak #1 : 4-apr-2020' ,'showarrow': True, 'x': '2020-04-04', 'y': 24900000 },
                  {'text': 'Peak #2 : 5-apr-2021' ,'showarrow': True, 'x': '2021-04-05', 'y': 26900000 },
                  {'text': 'Peak #3 : 3-apr-2022' ,'showarrow': True, 'x': '2022-04-03', 'y': 30000000 }]
sign_clear=[{'text': 'Clear', 'showarrow': False, 'x': 'October', 'y': 24.53 }]



# Create the buttons
my_buttons = [{'label': "Bar", 'method': "update", 'args': [{"type": "bar"}]},
  {'label': "Line-figure", 'method': "update", 'args': [{"type": "line", 'mode': 'line'}]},
             {'label': "Peaks", 'method': "update", 'args': [{}, {"annotations": value_annotations}]},
             {'label': "Clear peaks", 'method': "update", 'args': [{}, {"annotations": sign_clear}]}]



# Add buttons to the plot and show
fig2.update_layout(
    
    {'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]},

)

fig2.update_layout(
    title="Interactive plot displaying unique peaks regarding the Steam dataset",
    xaxis_title="Time stamp",
    yaxis_title="Active users (Millions)",
    legend_title="Legend Title",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)
# fig2.show()


# In[14]:


# Create a simple bar chart
fig3 = px.bar(data_frame=WC4, x='Date', y='Corona cases')

#annotations
sign_clear=[{'text': 'Clear', 'showarrow': False, 'x': 'October', 'y': 24.53 }]


# Create the buttons
my_buttons = [{'label': "Bar", 'method': "update", 'args': [{"type": "bar"}]},
  {'label': "Line-figure", 'method': "update", 'args': [{"type": "line", 'mode': 'line'}]},]




# Add buttons to the plot and show
fig3.update_layout(
    
    {'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]},

)

fig3.update_layout(
    title="Confirmed COVID cases on a global scale",
    xaxis_title="Time stamp",
    yaxis_title="Confirmed COVID cases (Infectants in billions)",
    legend_title="Legend Title",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)
# fig3.show()




# In[15]:


# Create a simple bar chart
fig4 = px.bar(data_frame=PS4_concurrent_players, x='dates', y='Player count')

# Create the buttons
my_buttons = [{'label': "Bar", 'method': "update", 'args': [{"type": "bar"}]},
  {'label': "Line-figure", 'method': "update", 'args': [{"type": "line", 'mode': 'line'}]}]


# Add buttons to the plot and show
fig4.update_layout(
    
    {'updatemenus': [{
      'type':'buttons','direction': 'down',
      'x': 1.3,'y': 0.5,
      'showactive': True, 'active': 0,
      'buttons': my_buttons}]},

)

fig4.update_layout(
    title="Active PS players online",
    xaxis_title="Time stamp",
    yaxis_title="Active users",
    legend_title="Legend Title",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)
# fig4.show()


# In[16]:


#WC3 Houdt nu de combinatie van de 2 dataframes world_cases en Steam_players_corona in.
WC4.head(20)

# Correlation table met pearson methodiek
WC5= WC4[['Corona cases', 'Steam users']]
WC_corr= WC5.corr(method='pearson')

# Heat map instellen
fig5 = go.Figure(go.Heatmap(
        z=WC_corr.values.tolist(),
        x=WC_corr.columns,
        y=WC_corr.columns,
        colorscale='rdylgn', 
        zmin=-1, zmax=1))


fig5.update_layout(
    title="Correlation heatmap",
    xaxis_title=" 'users' = active steam users    |    'Cumulative_cases' = Infected patients ",
    legend_title="Legend Title",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)

# Plot laten zien
# fig5.show()


# In[17]:


fig6 = px.scatter(x=WC4["Corona cases"], y=WC4["Steam users"])


fig6.update_layout(
    title="Scatterplot",
    xaxis_title="Infected patients (millions)",
    yaxis_title="Active steam users (millions)",
    font=dict(
        family="Arial",
        size=14,
        color="RebeccaPurple"
    )
)

# fig6.show()


# In[18]:


st.header('Our figures after analysing our 4 datasets')

st.write('Welcome to our presentation, the 4 datasets that we have used consist of Steam players, Power consumption globally, COVID Cases and playstation network users. With these 4 datasets we are trying to show if there is a correlation between the COVID cases and the remaining datasets mentioned above.')


st.plotly_chart(fig1, use_container_width=False, sharing="streamlit")

st.plotly_chart(fig2, use_container_width=False, sharing="streamlit")

st.plotly_chart(fig3, use_container_width=False, sharing="streamlit")

st.plotly_chart(fig4, use_container_width=False, sharing="streamlit")

st.plotly_chart(fig5, use_container_width=False, sharing="streamlit")

st.plotly_chart(fig6, use_container_width=False, sharing="streamlit")


# In[ ]:





# In[ ]:





# In[ ]:



