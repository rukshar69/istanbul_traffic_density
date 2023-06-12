#deployed streamlit app: https://rukshar69-istanbul-traffic-density-streamlit-app-qrqk1p.streamlit.app/
#GitHub Repo with necessary data: https://github.com/rukshar69/istanbul_traffic_density

import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import folium_static
from branca.colormap import linear
from PIL import Image

@st.cache_data()
def load_data():
    # Load your data here
    #data = pd.read_csv('./data/geohash_coords_address_info.csv')
    available_data = pd.read_csv('data/geohash_address_available_hourly_data.csv')
    taxi_data = pd.read_csv('data/ist_taxi_stands.csv')
    football_stadium_data = pd.read_csv('data/sportevents_per_stadium.csv')
    ferry_data = pd.read_csv('data/tr_ist_ferry_trmnls.csv')
    metro_data = pd.read_csv('data/tr_ist_metro_stns.csv')
    bus_data = pd.read_csv('data/tr_ist_bus_stops.csv')
    #the clustered data only has points with over 28k hourly data
    clustered_traffic_density_data = pd.read_csv('data/geohash_traffic_density_pt_clustered.csv')
    cluster4_traffic_density_data = pd.read_csv('data/geohash_traffic_density_pt_4clusters.csv')
    cluster5_traffic_density_data = pd.read_csv('data/geohash_traffic_density_pt_5clusters.csv')
    cluster6_traffic_density_data = pd.read_csv('data/geohash_traffic_density_pt_6clusters.csv')
    cluster15_traffic_density_data = pd.read_csv('data/geohash_traffic_density_pt_15clusters.csv')
    return available_data, taxi_data, football_stadium_data, ferry_data, metro_data, bus_data, clustered_traffic_density_data, \
            cluster4_traffic_density_data, cluster5_traffic_density_data, cluster6_traffic_density_data, cluster15_traffic_density_data

# Call the load_data function
available_data, taxi_data, football_stadium_data ,ferry_data, metro_data, bus_data, clustered_traffic_density_data, \
    cluster4_traffic_density_data, cluster5_traffic_density_data, cluster6_traffic_density_data, \
    cluster15_traffic_density_data= load_data()

st.header('Istanbul traffic EDA')
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

def show_clusters(colors, header, clustered_data):
    st.header(header)
    
    # Create a folium map centered at the mean location
    map2 = folium.Map(location=[clustered_data['LATITUDE'].mean(), clustered_data['LONGITUDE'].mean()], zoom_start=9)
    #SHOW CLUSTER CENTERS TOO
    cluster_centers = clustered_data[['label',	'centroid_lat',	'centroid_lon',]]
    cluster_centers = cluster_centers.drop_duplicates()
    #st.write(cluster10_centers)
    for index, row in cluster_centers.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        color = 'black'
        popup_str = row['label']
        folium.Marker([row['centroid_lat'], row['centroid_lon']], radius=4, color=color, fill=True, fill_color=color, popup=popup_str).add_to(map2)
    
    # Add markers for each location in the DataFrame
    for index, row in clustered_data.iterrows():
        #folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['road'], icon=folium.Icon(icon="circle", prefix='fa', color='blue')).add_to(map)
        popup_str = row['road']
        color = colors[row['label']]
        folium.CircleMarker([row['LATITUDE'], row['LONGITUDE']], radius=2, color=color, fill=True, fill_color=color, popup=popup_str).add_to(map2)
          
    folium_static(map2)

page_options = ['clustered traffic density pts','vehicle_points', 'traffic_density_points']
page_selected_option = st.selectbox('Select an option',page_options)

if page_selected_option == 'clustered traffic density pts':
    #10 CLUSTERS
    #cluster colors based on label column values
    colors = {0: 'blue', 1: 'red',2: 'green', 3: 'purple',4: 'yellow', 5: 'gray',6: 'orange', 7: 'pink',
              8: 'darkred', 9: 'lightgreen',}
    show_clusters(colors=colors, header='Traffic Density Points(w. over 28k data avaialable) for 10 Clusters',clustered_data= clustered_traffic_density_data)
    
    #15 CLUSTERS
    #cluster colors based on label column values
    colors = {0: 'blue', 1: 'red',2: 'green', 3: 'purple',4: 'yellow', 5: 'gray',6: 'orange', 7: 'pink',
              8: 'darkred', 9: 'green',10: 'darkred', 11: 'cadetblue',12: 'cadetblue', 13: 'purple',14: 'yellow',}
    header = 'Traffic Density Points(w. over 28k data avaialable) 15 clusters'
    show_clusters(colors=colors, header=header, clustered_data= cluster15_traffic_density_data)
    

    #4 CLUSTERS
    colors = {0: 'blue', 1: 'red',2: 'green', 3: 'purple',}
    show_clusters(colors=colors, header='Traffic Density Points(w. over 28k data avaialable) Clustered(4 clusters)', clustered_data=cluster4_traffic_density_data)
    
    #5 CLUSTERS
    colors = {0: 'blue', 1: 'red',2: 'green', 3: 'purple',4: 'yellow'}    
    show_clusters(colors=colors, header='Traffic Density Points(w. over 28k data avaialable) Clustered(5 clusters)', clustered_data=cluster5_traffic_density_data)
    
    #6 CLUSTERS
    colors = {0: 'blue', 1: 'red',2: 'green', 3: 'purple',4: 'yellow',5: 'gray'}
    st.header('Traffic Density Points(w. over 28k data avaialable) Clustered(6 clusters)')
    show_clusters(colors=colors, header='Traffic Density Points(w. over 28k data avaialable) Clustered(6 clusters)', clustered_data=cluster6_traffic_density_data)    

    st.header('Why use 10 clusters')
    st.write('K-means clustering requires us to select K, the number of clusters we want to  \
             group the data into. The elbow method lets us graph the inertia (a distance-based metric) \
             and visualize the point at which it starts decreasing linearly. This point is referred to \
             as the eblow and is a good estimate for the best value for K based on our data.')
    #plot inertia vs k
    inertia_v_k_image = Image.open('data/k_means_inertia.png')
    st.image(inertia_v_k_image, caption='Inertia vs k', use_column_width=True)
    st.write('The elbow method shows that 10 may be a good value for K, so we retrain and visualize the result. \
            **Note**: Others may also prefer another value. The elbow method, as you can see, is an approximate \
             method whose observations differ from person to person.')
if page_selected_option == 'traffic_density_points':
    #SHOW TRAFFIC POINTS FROM IBB TRAFFIC DENSITY DATA
    with st.expander('Traffic Density Points in Istanbul'):
        st.header('All Datapoints')
        show_map(available_data)

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