import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Read the CSV file
df = pd.read_csv('data/Indonesia_Province_LatLong_with_Population.csv')

# Initialize the Streamlit app
st.title('Peta Profinsi')

# Create a folium map centered on Indonesia
m = folium.Map(location=[-2.5489, 118.0149], zoom_start=4)

# Add markers for each province
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Province: {row['province']}<br>Population: {row['Population']}",
        tooltip=row['province']
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)
