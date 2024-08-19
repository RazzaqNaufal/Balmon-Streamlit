import streamlit as st
from map import map_page
from logging_util import view_logs


def home():
    st.title('Selamat Datang di Dashboard Balai Monitor SDPPI Banda Aceh')
    st.write("""
    Ini adalah dashboard interaktif yang menampilkan data geografis berdasarkan provinsi di Indonesia.
    Visualisasikan data stasiun radio Anda dengan mudah dan cepat. Unggah data Excel Anda, dan saksikan distribusi stasiun radio di seluruh Indonesia terpapar secara jelas pada peta interaktif kami. Dapatkan informasi lengkap mengenai lokasi, koordinat, dan data lainnya hanya dengan beberapa klik.
    """)
    st.image("D:\Materi University\Materi University Naufal Vivobook\Kerja Praktik\Balmon-Streamlit\Streamlit\Geopolitik-Indonesia.webp",
             caption="Radio Broadcasting")


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
