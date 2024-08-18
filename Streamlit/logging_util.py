import os
import pandas as pd
from datetime import datetime


def log_upload(uploaded_file, username='anonymous'):
    log_file = "upload_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_details = {
        "timestamp": timestamp,
        "username": username,
        "file_name": uploaded_file.name,
        "file_size": uploaded_file.size
    }

    # Check if the log file already exists
    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file)
    else:
        log_df = pd.DataFrame(
            columns=["timestamp", "username", "file_name", "file_size"])

    # Convert the file_details dictionary to a DataFrame
    new_log_entry = pd.DataFrame([file_details])

    # Append the new log entry to the log DataFrame using pd.concat
    log_df = pd.concat([log_df, new_log_entry], ignore_index=True)

    # Save the updated log DataFrame to CSV
    log_df.to_csv(log_file, index=False)
