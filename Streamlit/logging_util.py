import pandas as pd
import os
from datetime import datetime
import streamlit as st

log_file = "upload_log.csv"


def log_upload(file, username):
    log_entry = pd.DataFrame([{
        'Timestamp': datetime.now(),
        'Username': username,
        'Filename': file.name,
        'Filesize (KB)': file.size / 1024
    }])

    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file)
        log_df = pd.concat([log_df, log_entry], ignore_index=True)
    else:
        log_df = log_entry

    log_df.to_csv(log_file, index=False)


def view_logs():
    st.title('Log Upload Files')

    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file)
        st.write(log_df)
    else:
        st.write("No logs found.")
