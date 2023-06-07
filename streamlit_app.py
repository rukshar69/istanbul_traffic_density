import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import folium_static

@st.cache_data()
def load_data():
    # Load your data here
    data = pd.read_csv('./data/geohash_coords_address_info.csv')
    available_data = pd.read_csv('data/geohash_address_available_hourly_data.csv')
    taxi_data = pd.read_csv('data/ist_taxi_stands.csv')
    return data, available_data, taxi_data

# Call the load_data function
data, available_data, taxi_data = load_data()

st.header('Istanbul traffic points')
# Use the data in your Streamlit app
st.write(data)

#SHOW MAP
def show_map(map_data, point_color='red'):
    # Create a folium map centered at the first location
    map = folium.Map(location=[map_data['LATITUDE'][0], map_data['LONGITUDE'][0]], zoom_start=9)
    # Add markers for each location in the DataFrame
    for index, row in map_data.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=2, color=point_color, fill=True, fill_color=point_color, popup=row['road']).add_to(map)
    # Render the map in Streamlit as a static image
    folium_static(map)

#SHOW TRAFFIC POINTS FROM IBB TRAFFIC DENSITY DATA
show_traffic_points = True
if show_traffic_points:
    st.header('All Datapoints')
    show_map(data)

    over_28k_df = available_data[available_data.data_amount>28000]
    st.header('Geohash points ('+str(len(over_28k_df)) +') with over 28k hourly data')
    show_map(over_28k_df, point_color='blue')

    over_20k_df = available_data[available_data.data_amount>20000]
    st.header('Geohash points ('+str(len(over_20k_df)) +') with over 20k hourly data')
    show_map(over_20k_df, point_color='green')

#SHOW TAXI STANDS DATA
show_taxi_stand = True
if show_taxi_stand:
    st.header('Taxi Stands in Istanbul')
    # Create a folium map centered at the first location
    map = folium.Map(location=[taxi_data['LATITUDE'].mean(), taxi_data['LONGITUDE'].mean()], zoom_start=9)
    # Add markers for each location in the DataFrame
    for index, row in taxi_data.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        popup_str = 'Name: '+str(row['Name'])+'\n Road: '+str(row['road'])+ '\n Town: '+str(row['town'])+ '\n Suburb: '+str(row['suburb'])
        folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=2, color='purple', fill=True, fill_color='purple', popup=popup_str).add_to(map)
    # Render the map in Streamlit as a static image
    folium_static(map)

#SHOW TAXI STANDS AND TRAFFIC DENSITY POINTS WITH OVER 28K HOURLY DATA
show_taxi_traffic_density = True
if show_taxi_traffic_density:
    st.header('Taxi Stands and Traffic Density Points w. Over 28k Hourly Data in Istanbul')
    # Create a folium map centered at the mean location
    map2 = folium.Map(location=[taxi_data['LATITUDE'].mean(), taxi_data['LONGITUDE'].mean()], zoom_start=9)

    # Add markers for each location in the DataFrame
    for index, row in taxi_data.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        popup_str = 'Name: '+str(row['Name'])+'\n Road: '+str(row['road'])+ '\n Town: '+str(row['town'])+ '\n Suburb: '+str(row['suburb'])
        folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=2, color='red', fill=True, fill_color='red', popup=popup_str).add_to(map2)

    over_28k_df = available_data[available_data.data_amount>28000]
    # Add markers for each location in the DataFrame
    for index, row in over_28k_df.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        #folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], fill_opacity=0.0, radius=2, color='blue', fill=True, fill_color='blue', popup=row['road']).add_to(map2)
        folium.Circle(location=[row['LATITUDE'], row['LONGITUDE']],
                      color='blue',
                      radius=2,
                      fill=True,
                      opacity=0.4,
                      fill_opacity=0.4,
                      tooltip=row['road']).add_to(map2)
    
    folium_static(map2)

    # folium.Circle(
    # location=[lat, long],
    # color=colormap(city_ratio),
    # radius=50*math.sqrt(city_pop),
    # fill=True,
    # opacity=0.8,
    # fill_opacity=1,
    # tooltip='{}: {}'.format(city_name, city_ratio)
    # ).add_to(m)


