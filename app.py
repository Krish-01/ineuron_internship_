from pathlib import Path

import pandas as pd
import streamlit as st

from src.exception import SensorException
from src.pipeline.batch_prediction import start_batch_prediction
from src.pipeline.training_pipeline import start_training_pipeline

input_fp = Path('input.csv')

if input_fp.exists():
    input_fp.unlink()

st.title(':red[APS Fault Detection System]')
msg = st.empty()


# Train model button
with st.spinner('Training in progress...'):
    if st.button('Train Model', use_container_width=True):
        start_training_pipeline()
        msg.success('Model Training Completed.', icon='✅')


# Upload CSV file button
with st.form("upload_form"):
    st.subheader(':green[Batch Prediction]')
    uploaded_file = st.file_uploader(
        "Choose a CSV file to upload", type=["csv"],
    )

    if st.form_submit_button("Submit") and uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.to_csv(input_fp, index=False)
        msg.success('Your data is submitted successfully.')

# Download button
if input_fp.exists():
    prediction_fp = start_batch_prediction(input_fp)
    df = pd.read_csv(prediction_fp)
    msg.success('Prediction Completed. Download your file.')

    if st.download_button(
        label="Download Prediction DataFrame",
        file_name="prediction.csv",
        data=df.to_csv(index=False),
        mime="csv",
        use_container_width=True
    ):
        st.experimental_rerun()
