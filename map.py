"""
We are going to create Webmaps with the help of Python and Folium
"""
import folium
import pandas as pd
import os

"""
We are going to create an object using folium module.
Folium module helps us to automatically convert our python script into necessary JavaScript,HTML and CSS language
as the browser reads this languages.
"""

map = folium.Map(location = [21.146633, 79.088860], zoom_start = 7)  # You can check out more about folium.Map using help(folium.Map)

"""
Now we can get a marker to our map at a location
we can directly use add_child method to add a feature to our map object
or better we can use folium.FeatureGroup to keep our code organized for further use also
using this ensures that we have LayerControl

This is the code...
fg = folium.FeatureGroup()
fg.add_child(folium.Marker(location = [19.29, 72.86], popup = "Hey there, this is my HOME!!!", icon = folium.Icon(color = 'blue')))
map.add_child(fg)
"""

"""
Now we can create more than one markers using the above code repeatedly
or we can do one thing is that we can get a list containing latitudes and longitudes
and further using pandas and foilum we can mark them on a map...
"""
# Creating a pandas dataframe
data = pd.read_csv(os.path.join(os.getcwd(),'worldcities.csv'))
data_india = data[data['country'] == 'India']
lat = list(data_india['lat'])
lon = list(data_india['lng'])
city = list(data_india['city'])
state = list(data_india['admin_name'])
pop = list(data_india['population'])


def color_producer(city):
    # This is done to distinguish several cities from others on the basis of color
    # the following is list of metro cities in India
    metro = ['Kanpur', 'Visakhapatnam', 'Surat', 'Chennai', 'Hyderabad', 'Pune', 'Banglore', 'Kolkata', 'Mumbai', 'New Delhi']
    if c in metro:
        # The metro cities are displayed in red colors while the rest in green
        return 'red'
    else:
        return 'green'

fg_for_marker = folium.FeatureGroup(name = 'Indian Cities')

for lt, ln, c, s, p in zip(lat,lon, city, state, pop):
    fg_for_marker.add_child(folium.Marker(location = [lt, ln] ,popup ='Welcome to ' +  c  + ' in ' + s  + " with population = " + str(p),
    icon = folium.Icon(color_producer(c))))
    """
     We can also use folium.CircleMarker to use a circle as a Marker

     fg.add_child(folium.CircleMarker(location = [lt, ln] ,radius = 5,color = 'grey',
     popup ='Welcome to ' +  c  + ' in ' + s  + " with population = " + str(p), fill_color = color_producer(c),fill_opacity=0.7))
    """

"""
We can also add an extra layer to the Map
Now we will add a polygon layer to the map displaying the various countries around the world
We'll use a json file having all the data about the polygons and adding this feature to fg and then to map...
"""
fg_for_population = folium.FeatureGroup(name = 'Population')

fg_for_population.add_child(folium.GeoJson(data = (open(os.path.join(os.getcwd(), 'world.json'), 'r',encoding= 'utf-8-sig').read()),
style_function = lambda x: {'fillColor': 'blue' if x['properties']['POP2005'] < 1500000
else 'yellow' if 1500000 < x['properties']['POP2005'] < 3000000
else 'red'}))

map.add_child(fg_for_marker)
map.add_child(fg_for_population)

"""
Now we'll us folium.LayerControl() for controlling the several layers which we added
i.e the marker layer and the polygon layer
We can turn them on/off from the top right corner of the map
"""
map.add_child(folium.LayerControl())

map.save("map.html") # saving this object as a HTML file
# Opening this file loads the browser and our map
