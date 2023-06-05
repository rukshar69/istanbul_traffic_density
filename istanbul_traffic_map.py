import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import folium_static

@st.cache_data()
def load_data():
    # Load your data here
    data = pd.read_csv('./data/geohash_coords_address_info.csv')
    return data

# Call the load_data function
data = load_data()

st.header('Istanbul traffic points')
# Use the data in your Streamlit app
st.write(data)

#SHOW MAP

# Create a folium map centered at the first location
map = folium.Map(location=[data['LATITUDE'][0], data['LONGITUDE'][0]], zoom_start=9)
# Add markers for each location in the DataFrame
for index, row in data.iterrows():
    #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
    folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=2, color='red', fill=True, fill_color='red', popup=row['road']).add_to(map)
# Render the map in Streamlit as a static image
folium_static(map)




