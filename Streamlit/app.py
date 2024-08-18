import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Fungsi untuk memuat dan menampilkan data
def load_data(file):
    data = pd.read_excel(file)
    return data

# Fungsi untuk membuat peta
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

# Fungsi halaman utama
def home():
    st.title('Selamat Datang di Dashboard Balai Monitor SDPPI Banda Aceh')
    st.write("""
    Ini adalah dashboard interaktif yang menampilkan data geografis berdasarkan provinsi di Indonesia.
    Visualisasikan data stasiun radio Anda dengan mudah dan cepat. Unggah data Excel Anda, dan saksikan distribusi stasiun radio di seluruh Indonesia terpapar secara jelas pada peta interaktif kami. Dapatkan informasi lengkap mengenai lokasi, koordinat, dan data lainnya hanya dengan beberapa klik.
    """)

# Menambahkan gambar lainnya
    st.image("C:\Kerja Praktik\Streamlit\Geopolitik-Indonesia.webp", caption="Radio Broadcasting")

# Fungsi halaman peta
def map_page():
    st.title('Peta Interaktif')

    # Upload file Excel
    uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        # Menampilkan data sebagai tabel
        st.write("Data Excel:", data)

        # Filter berdasarkan Provinsi
        provinsi = st.selectbox("Pilih Provinsi", options=["Semua"] + list(data['PROVINCE'].unique()))
        if provinsi != "Semua":
            data = data[data['PROVINCE'] == provinsi]

        # Filter berdasarkan SUBSERVICE
        subservice = st.multiselect("Pilih Subservice", options=data['SUBSERVICE'].unique())
        if subservice:
            data = data[data['SUBSERVICE'].isin(subservice)]

        # Filter berdasarkan BWIDTH
        bwidth = st.multiselect("Pilih Bandwidth", options=data['BWIDTH'].unique())
        if bwidth:
            data = data[data['BWIDTH'].isin(bwidth)]

        # Membuat dan menampilkan peta
        my_map = create_map(data)
        folium_static(my_map)

        # Menampilkan data terfilter sebagai tabel
        st.write("Data Terfilter:", data)

# Fungsi utama untuk Streamlit
def main():
    st.sidebar.title('Navigasi')
    page = st.sidebar.radio("Pilih Halaman", ["Home", "Peta Interaktif"])

    if page == "Home":
        home()
    elif page == "Peta Interaktif":
        map_page()

if __name__ == "__main__":
    main()
