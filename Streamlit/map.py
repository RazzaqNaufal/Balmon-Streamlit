import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from logging_util import log_upload
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def load_data(file):
    data = pd.read_excel(file)
    return data


def create_map(data):
    # Remove rows with NaN values in SID_LAT or SID_LONG
    data = data.dropna(subset=['SID_LAT', 'SID_LONG'])

    map_center = [data['SID_LAT'].mean(), data['SID_LONG'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=6)

    for _, row in data.iterrows():
        popup_content = f"""
        <div style="font-family: Arial, sans-serif; color: #333; line-height: 1.4;">
            <h4 style="margin: 0; font-size: 16px;">{row['STN_NAME']}</h4>
            <p style="margin: 5px 0 0; font-size: 14px;">
                <strong>Alamat:</strong> {row['STN_ADDR']}<br>
                <strong>Provinsi:</strong> {row['PROVINCE']}
            </p>
        </div>
        """
        folium.Marker(
            location=[row['SID_LAT'], row['SID_LONG']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=row['STN_NAME']
        ).add_to(my_map)

    return my_map


def map_page():
    st.title('Peta Interaktif')

    username = st.text_input("Enter your username")
    if username:
        st.session_state['username'] = username

    if 'username' not in st.session_state:
        st.warning("Please enter your username first!.")
        return

    uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

    if uploaded_file is not None:
        username = st.session_state.get('username', 'anonymous')
        log_upload(uploaded_file, username)
        new_data = load_data(uploaded_file)

        if 'previous_data' in st.session_state:
            if new_data.equals(st.session_state['previous_data']):
                st.warning(
                    "The uploaded file is no different from the previous upload.")
                return
            else:
                st.session_state['previous_data'] = pd.concat(
                    [st.session_state['previous_data'], new_data]).drop_duplicates().reset_index(drop=True)
        else:
            st.session_state['previous_data'] = new_data

        data = st.session_state['previous_data']

        kota = st.selectbox("Pilih Kota", options=[
                            "Semua"] + list(data['CITY'].unique()))
        if kota != "Semua":
            data = data[data['CITY'] == kota]

        subservice = st.multiselect(
            "Pilih Subservice", options=data['SUBSERVICE'].unique())
        if subservice:
            data = data[data['SUBSERVICE'].isin(subservice)]

        bwidth = st.multiselect(
            "Pilih Bandwidth", options=data['BWIDTH'].unique())
        if bwidth:
            data = data[data['BWIDTH'].isin(bwidth)]

        area_of_service = st.selectbox("Pilih Area of Service", options=[
                                       "Semua"] + list(data['AREA_OF_SERVICE'].unique()))
        if area_of_service != "Semua":
            data = data[data['AREA_OF_SERVICE'] == area_of_service]

        my_map = create_map(data)
        folium_static(my_map)

        st.write("Data Terfilter:", data)

        if st.button("Save Map as Image"):
            map_image_path = save_map_as_image(my_map)
            with open(map_image_path, "rb") as file:
                btn = st.download_button(
                    label="Download Map Image",
                    data=file,
                    file_name="map.png",
                    mime="image/png"
                )


def save_map_as_image(map_obj):
    map_html = map_obj.get_root().render()
    with open("temp_map.html", "w") as f:
        f.write(map_html)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1024x768')

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get("file://" + os.path.abspath("temp_map.html"))
    time.sleep(5)
    driver.save_screenshot("map.png")
    driver.quit()

    st.success("Map saved as image: map.png")
    return "map.png"
