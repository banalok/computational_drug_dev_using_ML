
import streamlit as st
import pandas as pd
from utils import *

st.header("File Upload")
uploaded_file = st.file_uploader("Upload", type=['txt'])

if uploaded_file is not None:
    load_data(uploaded_file)
    desc_calc()
    select_fingerprints()
    download_model_from_drive()
    load_model()
    org_fingerprint_df, final_df, prediction = prediction_fingerprints()
    st.header("PaDel-generated Dataset")
    st.write(org_fingerprint_df)
    st.header("Selected Fingerprint Dataset")
    st.write(final_df)
    st.header("Prediction Dataset")
    st.write(prediction)
