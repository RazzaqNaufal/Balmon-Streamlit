import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Radio Signal Report in Indonesia'
APP_SUB_TITLE = 'Source: National Communication Agency'

def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
    quarter = st.sidebar.radio('Quarter', [1, 2, 3, 4])
    st.header(f'{year} Q{quarter}')
    return year, quarter

def display_province_filter(df, province_name):
    province_list = [''] + list(df['Region Name'].unique())
    province_list.sort()
    province_index = province_list.index(province_name) if province_name and province_name in province_list else 0
    return st.sidebar.selectbox('Province', province_list, province_index)

def display_map(df, year, quarter):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

    # Center the map on Indonesia
    map = folium.Map(location=[-2.5, 118], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')
    
    # Use the GeoJSON file for Indonesian regions
    choropleth = folium.Choropleth(
        geo_data='data/indonesia-region-boundaries.geojson',  # Update this path to your GeoJSON file for regions
        data=df,
        columns=('Region Name',),  # Update the columns according to your data
        key_on='feature.properties.region_name',  # Assuming your GeoJSON uses 'region_name' for region names
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    st_map = st_folium(map, width=700, height=450)

    region_name = ''
    if st_map['last_active_drawing']:
        region_name = st_map['last_active_drawing']['properties']['region_name']
    return region_name

def display_signal_facts(df, year, quarter, province_name):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    if province_name:
        df = df[df['Region Name'] == province_name]
    df.drop_duplicates(inplace=True)
    st.dataframe(df)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # Load Data
    df_continental = pd.read_csv('data/Indonesia_Province_Data.csv')

    # Display Filters and Map
    year, quarter = display_time_filters(df_continental)
    province_name = display_map(df_continental, year, quarter)
    province_name = display_province_filter(df_continental, province_name)

    # Display DataFrame
    st.subheader(f'{province_name} Signal Data')

    col1 = st.columns(1)
    with col1:
        display_signal_facts(df_continental, year, quarter, province_name)

if __name__ == "__main__":
    main()