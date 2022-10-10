#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('pip install streamlit')
import streamlit as st
import pandas as pd
import numpy as np
import htlm5lib
import lxml


# In[6]:


get_ipython().system('pip install dash')
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dash import dcc
from plotly.express import data


# In[ ]:


#AANPAK CASE DASHBOARD:
 #- het aantal vliegtuigcrashes per jaar in een lijndiagram (met een slider dat je kan inzoomen in de jaren)
 #- het aantal vliegtuigcrashes per maand in een barplot
    #met barplot een dropdownmenu
 #- het aantal vliegtuigcrashes per dag in een barplot
 #- het aantal vlietuigcrashes per vluchttype (passagier, militair (onderverdelen in verschillende armys), private etc)
 #- het aantal doden/crashes per vliegtuigmaatschappij (met een checkbox voor de vliegtuigmaatschappijen)


# In[12]:


df = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv')


# In[13]:


df.head()


# In[14]:


df.info()


# In[15]:


df.describe()


# In[16]:


#- het aantal vliegtuigcrashes per jaar in een lijndiagram (met een slider dat je kan inzoomen in de jaren)
df['Year'] = df["Date"].astype(str).str[6:10]
df.head()
aantal_y = df.groupby(['Year'])
aantal_y = pd.DataFrame(aantal_y['Date'].count())
print(aantal_y)


# In[17]:


fig = px.line(aantal_y, title='Aantal vliegtuigongelukken per jaar in de jaren 1908-2019')
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout({'xaxis': {'title': {'text': 'Jaar'}},
                   'yaxis': {'title':{'text': 'Aantal vliegtuigongelukken'}},
                   'legend': {'title':{'text': 'Verloop van het aantal'}}})    
fig.show()
st.plotly_chart(fig)


# In[18]:


#- het aantal vliegtuigcrashes per maand in een barplot

df['Month'] = df["Date"].astype(str).str[0:2]
df.head()
aantal_m = df.groupby(['Month'])
aantal_m = pd.DataFrame(aantal_m['Date'].count())
print(aantal_m)


# In[19]:


fig = px.bar(aantal_m, title='Aantal vliegtuigongelukken per maand in de jaren 1908-2019')
fig.update_layout({'xaxis': {'title': {'text': 'Maand'}},
                   'yaxis': {'title':{'text': 'Aantal vliegtuigongelukken'}},
                   'legend': {'title':{'text': 'Aantal'}}})   
fig.show()
st.plotly_chart(fig)


# In[20]:


#- het aantal vliegtuigcrashes per dag in een barplot
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day_of_week
df.head()
aantal_d = df.groupby(['Day'])
aantal_d = pd.DataFrame(aantal_d['Date'].count())
print(aantal_d)


# In[21]:


fig = px.bar(aantal_d, title='Aantal vliegtuigongelukken per dag in de jaren 1908-2019')
fig.update_layout({'xaxis': {'title': {'text': 'Dag'}},
                   'yaxis': {'title':{'text': 'Aantal vliegtuigongelukken'}},
                   'legend': {'title':{'text': 'Aantal'}}})   
fig.show()
st.plotly_chart(fig)


# In[22]:


df.head()


# In[23]:


#- pie chart met fatalities en survivors en die onderverdeeld in passengers of crew met dropdownmenu
df_drop = df.dropna(subset=['Aboard', 'Fatalities'])
aboard = df_drop['Aboard'].sum()
fatalities = df_drop['Fatalities'].sum()
survived = aboard - fatalities
df_surv = pd.DataFrame(data=[fatalities, survived])
df_surv.head()

fat_crew = df_drop['Fatalities Crew'].sum()
fat_pass = df_drop['Fatalities Passangers'].sum()
ab_crew = df_drop['Aboard Crew'].sum()
ab_pass = df_drop['Aboard Passangers'].sum()
surv_crew = ab_crew - fat_crew
surv_pass = ab_pass - fat_crew
df_surv2 = pd.DataFrame(data=[surv_crew, surv_pass])
df_surv2.head()


# In[24]:


labels = ['Fatalities', 'Survived']
values = [fatalities, survived, surv_crew, surv_pass]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

dropdown_buttons = [
    {'label': 'Passangers', 'method': 'update',
    'args': [{'visible': [True, False]},
            {'title': 'Passangers'}]},
    {'label': 'Crew', 'method': 'update',
    'args': [{'visible': [False, True]},
            {'title': 'Crew'}]}, 
]

fig.update_layout({
    'updatemenus':[{'type': "dropdown",
        'x': 1.3,
        'y': 0.5,
        'showactive': True,
        'active': 0,
        'buttons': dropdown_buttons}]})

fig.show()
st.plotly_chart(fig)


# In[25]:


df_time = df.dropna(subset=['Time'])
df_time['Hour'] = df_time["Time"].astype(str).str[0:2]
df_time.drop(df_time[df_time['Hour'] > '23'].index, inplace=True)
aantal_h = df_time.groupby(['Hour'])
aantal_h = pd.DataFrame(aantal_h['Date'].count())
print(aantal_h)


# In[26]:


tijd1 = df_time.loc[(df_time['Hour'] >= '00') & (df_time['Hour'] <= '08')]
groep1 = tijd1.groupby(['Hour'])
groep1 = pd.DataFrame(groep1['Date'].count())
#print(groep1)

tijd2 = df_time.loc[(df_time['Hour'] >= '09') & (df_time['Hour'] <= '16')]
groep2 = tijd2.groupby(['Hour'])
groep2 = pd.DataFrame(groep2['Date'].count())
#print(groep2)

tijd3 = df_time.loc[(df_time['Hour'] >= '17') & (df_time['Hour'] <= '23')]
groep3 = tijd3.groupby(['Hour'])
groep3 = pd.DataFrame(groep3['Date'].count())
#print(groep3)


# In[27]:


from plotly.offline import plot


# In[28]:


fig = px.line(aantal_h, title='Aantal vliegtuigongelukken per uur op een dag in de jaren 1908-2019')
dcc.Checklist(aantal_h.columns, aantal_h.columns.values)
fig.update_layout({'xaxis': {'title': {'text': 'Uur'}},
                   'yaxis': {'title':{'text': 'Aantal vliegtuigongelukken'}},
                   'legend': {'title':{'text': 'Verloop van het aantal'}}})    
fig.show()
st.plotly_chart(fig)


# In[29]:


#aantal_h = pd.DataFrame({
    ##850: [23, 21, 12],
    #1851: [28, 21, 13],
    #1852: [31, 22, 13]}).set_index('State')

data = [go.Scatter(x=aantal_h.columns,
                   y=aantal_h.loc[hour],
                   name=hour) for hour in aantal_h.index]

layout = go.Layout(
    title='Hour',
    yaxis=dict(title='Aantal'),
    xaxis=dict(title='Hour')
)

fig = go.Figure(data=data, layout=layout)
plot(fig)


# In[ ]:





# In[ ]:





# In[ ]:




