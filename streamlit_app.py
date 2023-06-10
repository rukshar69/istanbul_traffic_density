#deployed streamlit app: https://rukshar69-istanbul-traffic-density-streamlit-app-qrqk1p.streamlit.app/
#GitHub Repo with necessary data: https://github.com/rukshar69/istanbul_traffic_density

import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import folium_static
from branca.colormap import linear

@st.cache_data()
def load_data():
    # Load your data here
    data = pd.read_csv('./data/geohash_coords_address_info.csv')
    available_data = pd.read_csv('data/geohash_address_available_hourly_data.csv')
    taxi_data = pd.read_csv('data/ist_taxi_stands.csv')
    football_stadium_data = pd.read_csv('data/sportevents_per_stadium.csv')
    ferry_data = pd.read_csv('data/tr_ist_ferry_trmnls.csv')
    metro_data = pd.read_csv('data/tr_ist_metro_stns.csv')
    bus_data = pd.read_csv('data/tr_ist_bus_stops.csv')
    return data, available_data, taxi_data, football_stadium_data, ferry_data, metro_data, bus_data

# Call the load_data function
data, available_data, taxi_data, football_stadium_data ,ferry_data, metro_data, bus_data= load_data()

st.header('Istanbul traffic points')
# Use the data in your Streamlit app
# st.write(data)

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


page_options = ['vehicle_points', 'traffic_density_points']
page_selected_option = st.selectbox('Select an option',page_options)

if page_selected_option == 'traffic_density_points':
    #SHOW TRAFFIC POINTS FROM IBB TRAFFIC DENSITY DATA
    with st.expander('Traffic Density Points in Istanbul'):
        st.header('All Datapoints')
        show_map(data)

        over_28k_df = available_data[available_data.data_amount>28000]
        st.header('Geohash points ('+str(len(over_28k_df)) +') with over 28k hourly data')
        show_map(over_28k_df, point_color='blue')

        over_20k_df = available_data[available_data.data_amount>20000]
        st.header('Geohash points ('+str(len(over_20k_df)) +') with over 20k hourly data')
        show_map(over_20k_df, point_color='green')

    #SHOW TAXI STANDS DATA
    with st.expander('Taxi Points in Istanbul'):
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
    with st.expander('Traffic Density Points w/ Taxi Stands in Istanbul'):
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

    #SHOW STADIUM LOCATIONS ALONG WITH FOOTBALL MATCH COUNT
    with st.expander('Stadiums in Istanbul'):
        st.header('Stadiums in Istanbul and Football Match Count')
        # Create a color map
        #colormap = linear.PuRd_09.scale(0, 100)  # Adjust the scale as per your data

        # Create a folium map centered at the mean location
        map2 = folium.Map(location=[football_stadium_data['stad_lat'].mean(), football_stadium_data['stad_long'].mean()], zoom_start=9)
        # Add markers for each location in the DataFrame
        for index, row in football_stadium_data.iterrows():
            #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
            popup_str = 'Name: '+str(row['stadium'])+'\n Match count: '+str(row['count'])
            folium.CircleMarker([row['stad_lat'], row['stad_long']], radius=8, color='red', fill=True, fill_color='red', popup=popup_str).add_to(map2)
        folium_static(map2)

elif page_selected_option == 'vehicle_points':
    with st.expander('Ferry/Bus/Metro Stops in Istanbul'):
        st.header('Ferry/Bus/Metro Stops in Istanbul')

        options = ['Ferry', 'Metro', 'Bus']
        selected_option = st.multiselect('Select options', options)
        st.write('Show data for: ')
        for ind, option in enumerate(selected_option):
            st.write(str(ind+1),': ',option)

        # Create a folium map centered at the mean location
        map2 = folium.Map(location=[ferry_data['latitude'].mean(), ferry_data['longitude'].mean()], zoom_start=9)
        
        if 'Ferry' in selected_option:
            # Add markers for each location in the DataFrame
            for index, row in ferry_data.iterrows():
                #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
                popup_str = row['ferry_terminal']
                folium.CircleMarker([row['latitude'], row['longitude']], radius=3, color='blue', fill=True, fill_color='blue', popup=popup_str).add_to(map2)
        
        if 'Metro' in selected_option:
            for index, row in metro_data.iterrows():
                #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
                popup_str = row['Name'] + ' '+ row['LineName']
                folium.CircleMarker([row['Latitude'], row['Longitude']], radius=3, color='green', fill=True, fill_color='green', popup=popup_str).add_to(map2)

        if 'Bus' in selected_option:
            for index, row in bus_data.iterrows():
                popup_str = row['STATION_NAME'] + ' '+ row['DISTRICT']+ ' '+ row['STOP_TYPE']
            #     folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=3, color='red', fill=True, fill_color='red', popup=popup_str).add_to(map2)

                folium.Circle(location=[row['LATITUDE'], row['LONGITUDE']],
                                color='red',
                                radius=2,
                                fill=True,
                                opacity=0.3,
                                fill_opacity=0.3,
                                tooltip=popup_str).add_to(map2)
        folium_static(map2)