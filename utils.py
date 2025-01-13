import subprocess
import streamlit as st
import os
import pickle
import base64
import pandas as pd
import gdown

def load_data(uploaded_file):
    org_df = pd.read_csv(uploaded_file, sep=' ', header=None)
    st.header("Original File")
    st.write(org_df)
    org_df.to_csv('fingerprints.smi', sep = '\t', header = False, index = False) # smi file needed for padel to calculate descriptors

# Molecular descriptor calculator using PaDEL
def desc_calc():
    # to automatically run this command in the terminal to execute descriptor calculation
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file padel_descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('fingerprints.smi')

def load_model():
    model = pickle.load(open('acetyl_model.pkl', 'rb'))
    return model

def select_fingerprints():
    fingerprint_columns = list(pd.read_csv('acetyl_padel_selected_descriptors.csv').columns)
    return fingerprint_columns

def prediction_fingerprints():
    df = pd.read_csv("padel_descriptors_output.csv")
    selected_fingerprints = select_fingerprints()
    final_df = df[selected_fingerprints]
    model = load_model()
    prediction = model.predict(final_df)
    return df, final_df, prediction

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

@st.cache_data
def download_model_from_drive():
    file_id = "107f5ZgdZX_e0yFXi7N1jzSBMl9UHkZwB"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, quiet=False)
