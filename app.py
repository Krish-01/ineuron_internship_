from pathlib import Path
from shutil import rmtree
from time import sleep

import pandas as pd
import streamlit as st

from src.entity.config_entity import ModelPusherConfig, TrainingPipelineConfig
from src.pipeline.batch_prediction import start_batch_prediction
from src.pipeline.training_pipeline import start_training_pipeline
from src.predictor import ModelResolver

input_fp = Path('input.csv')

if input_fp.exists():
    input_fp.unlink()

st.title(':red[APS Fault Detection System]')
msg = st.empty()

# --- --- Variables --- --- #
latest_dir_path = ModelResolver().get_latest_dir_path()
saved_model_dir = Path(
    ModelPusherConfig(TrainingPipelineConfig()).saved_model_dir)

# Train model button
if latest_dir_path is None:
    with st.spinner('Training in progress...'):
        if st.button('Train Model', use_container_width=True):
            start_training_pipeline()
            msg.success('Model Training Completed.', icon='✅')
            st.experimental_rerun()
else:
    msg.warning('Model already trained. Start your Batch Prediction.',
                icon='🤖')
    with st.spinner('Deletion in progress...'):
        if st.button('Delete Pre-Trained Model', use_container_width=True):
            rmtree(saved_model_dir)     # Delete saved_model_dir tree
            rmtree(Path('logs'))        # Delete logs folder
            msg.success('Pre-Trained model deleted.', icon='✅')
            sleep(2)
            st.experimental_rerun()


# Upload CSV file button
with st.form("upload_form"):
    st.subheader(':green[Batch Prediction]')
    uploaded_file = st.file_uploader(
        "Choose a CSV file to upload", type=["csv"],
    )

    if st.form_submit_button("Submit") and uploaded_file:
        if (not saved_model_dir.exists() or
            len(list(saved_model_dir.iterdir())) == 0):
            msg.warning('Model is not trained yet. Please train model.')
            st.stop()

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
        use_container_width=True,
    ):
        st.experimental_rerun()
