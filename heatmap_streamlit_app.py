import pandas as pd; import plotly.express as px; import streamlit as st; import plotly.graph_objects as go; import numpy as np

@st.cache_data()
def load_data():
    traffic_density_vehicle_count_df = pd.read_csv('./data/geohash_traffic_density_vehicle_count.csv')
    return traffic_density_vehicle_count_df

traffic_density_vehicle_count_df = load_data()

st.header('Traffic Density Points(with over 28k data) Heatmap using Total Vehicle Count')

#construct a heatmap of vehicle count for traffic density points
def create_heatmap(data_df):

    # Create the density_mapbox trace
    density_mapbox = go.Densitymapbox(
        lat=data_df.LATITUDE,
        lon=data_df.LONGITUDE,
        z=data_df.NUMBER_OF_VEHICLES,
        radius=10
    )

    # Define a custom color scale
    custom_colorscale = [
        [0, 'rgb(255, 255, 0)'],
        [1, 'rgb(255, 0, 0)'],
        #[0.5, 'rgb(0, 255, 0)'],
        
    ]

    # Update the color scale of the density_mapbox trace
    density_mapbox.colorscale = custom_colorscale

    # Create the layout object
    layout = go.Layout(
        mapbox_style="carto-positron",
        mapbox_zoom=9,
        mapbox_center={"lat": np.mean(data_df.LATITUDE), "lon": np.mean(data_df.LONGITUDE)}
    )

    # Create the figure
    fig = go.Figure(data=[density_mapbox], layout=layout)

    # Display the figure
    st.plotly_chart(fig)

create_heatmap(traffic_density_vehicle_count_df)