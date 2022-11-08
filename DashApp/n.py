import folium
import pandas as pd
from folium.plugins import HeatMap

# read file
df = pd.read_csv('C:/Users/ruveb/Desktop/pm (1).csv')

# get latest year
df = df[df['year'] == df.year.max()]

# set attributes
df = df[['latitude', 'longitude', 'PM2.5 (μg/m3)']]

# create map
map = folium.Map([-30.5595, 22.9375], zoom_start=5, control_scale=True)
HeatMap(df).add_to(map)

# save to html to use in Iframe
map.save("output.html")


