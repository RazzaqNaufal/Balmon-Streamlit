import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from logging_util import log_upload  # Import the logging function
import os

# Function to load and display data


def load_data(file):
    data = pd.read_excel(file)
    return data

# Function to create a map


def create_map(data):
    map_center = [data['SID_LAT'].mean(), data['SID_LONG'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=6)

    for _, row in data.iterrows():
        folium.Marker(
            location=[row['SID_LAT'], row['SID_LONG']],
            popup=f"<strong>{row['STN_NAME']}</strong><br>"
                  f"Alamat: {row['STN_ADDR']}<br>"
                  f"Provinsi: {row['PROVINCE']}",
            tooltip=row['STN_NAME']
        ).add_to(my_map)

    return my_map

# Main page function


def home():
    st.title('Selamat Datang di Dashboard Balai Monitor SDPPI Banda Aceh')
    st.write("""
    Ini adalah dashboard interaktif yang menampilkan data geografis berdasarkan provinsi di Indonesia.
    Visualisasikan data stasiun radio Anda dengan mudah dan cepat. Unggah data Excel Anda, dan saksikan distribusi stasiun radio di seluruh Indonesia terpapar secara jelas pada peta interaktif kami. Dapatkan informasi lengkap mengenai lokasi, koordinat, dan data lainnya hanya dengan beberapa klik.
    """)

    st.image("D:\Materi University\Materi University Naufal Vivobook\Kerja Praktik\Balmon-Streamlit\Streamlit\Geopolitik-Indonesia.webp",
             caption="Radio Broadcasting")

# Map page function


def map_page():
    st.title('Peta Interaktif')

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Replace with actual username if available
        username = st.session_state.get('username', 'anonymous')
        log_upload(uploaded_file, username)  # Log file upload
        data = load_data(uploaded_file)

        # # Display data as table
        # st.write("Data Excel:", data)

        # # Filter by Province
        # provinsi = st.selectbox("Pilih Provinsi", options=[
        #                         "Semua"] + list(data['PROVINCE'].unique()))
        # if provinsi != "Semua":
        #     data = data[data['PROVINCE'] == provinsi]

    # Filter berdasarkan Kota
        kota = st.selectbox("Pilih Kota", options=[
                            "Semua"] + list(data['CITY'].unique()))
        if kota != "Semua":
            data = data[data['CITY'] == kota]

        # Filter by SUBSERVICE
        subservice = st.multiselect(
            "Pilih Subservice", options=data['SUBSERVICE'].unique())
        if subservice:
            data = data[data['SUBSERVICE'].isin(subservice)]

        # Filter by BWIDTH
        bwidth = st.multiselect(
            "Pilih Bandwidth", options=data['BWIDTH'].unique())
        if bwidth:
            data = data[data['BWIDTH'].isin(bwidth)]

        # Filter berdasarkan Area of Service
        area_of_service = st.selectbox("Pilih Area of Service", options=[
                                       "Semua"] + list(data['AREA_OF_SERVICE'].unique()))
        if area_of_service != "Semua":
            data = data[data['AREA_OF_SERVICE'] == area_of_service]

        # Create and display map
        my_map = create_map(data)
        folium_static(my_map)

        # Display filtered data as table
        st.write("Data Terfilter:", data)

# Function to view the logs


def view_logs():
    st.title('Log Upload Files')

    log_file = "upload_log.csv"

    # Check if the log file exists
    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file)
        st.write(log_df)
    else:
        st.write("No logs found.")

# Main function for Streamlit


def main():
    st.sidebar.title('Navigasi')
    page = st.sidebar.radio(
        "Pilih Halaman", ["Home", "Peta Interaktif", "View Logs"])

    if page == "Home":
        home()
    elif page == "Peta Interaktif":
        map_page()
    elif page == "View Logs":
        view_logs()


if __name__ == "__main__":
    main()
