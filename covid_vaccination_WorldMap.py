import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

df = pd.read_csv("./covid_data//Worldwide Vaccine Data.csv")


df = df.rename(columns = {'Doses administered per 100 people':'administered_per_100_people'})
df = df.rename(columns = {'Total doses administered':'total_administered'})
df = df.rename(columns = {'% of population vaccinated':'vaccinated'})
df = df.rename(columns = {'% of population fully vaccinated':'fully_vaccinated'})

df.replace(',','',regex = True, inplace = True)




fig = go.Figure(data = go.Choropleth(locations = df['Country'],
                                     z = df['administered_per_100_people'],
                                     locationmode = 'country names',
                                     colorscale = 'twilight',
                                     autocolorscale = False,
                                     reversescale = True,
                                     marker_line_color = 'LightGray',
                                     marker_line_width = 0.3,
                                     colorbar_title = '接种剂数/100人'))

fig.update_traces(colorbar_title_font = dict(family = 'Droid Sans',
                                             size = 12,
                                             color = 'DarkBlue'))
fig.update_layout(
    title_text = '每百人接种剂数',
    title_font = dict(size = 18, family = 'Balto',color = 'white'),
    title_x =0.5,
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection_type= 'equirectangular'))
fig.show()
