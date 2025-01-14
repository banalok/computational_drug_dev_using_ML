
import streamlit as st
import pandas as pd
from utils import *
import base64

def set_page_background(png_file):
    @st.cache_data(show_spinner=False)
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    bin_str = get_base64_of_bin_file(png_file)
    custom_css = f'''
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: scroll;
            }}
            
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            icon {{color: white;}}
            nav-link {{--hover-color: grey; }}
            nav-link-selected {{background-color: #4ABF7E;}}
        </style>
    '''
    st.markdown(custom_css, unsafe_allow_html=True)

set_page_background("./outputtt.jpg")

st.warning("""This application predicts the potency of a molecular compound based on the Machine Learning QSAR (Quantitative Structure-Activity Relationship) approach. The prediction is
         pIC50 to quantify the potency of a drug or compound in inhibiting a specific biological or biochemical function of a target protein acetylcholinesterase.
        The pIC₅₀ value typically ranges from about 0 (less potent) to 12 (highly potent).""")

st.header("Upload a text file with Canonical SMILES notation and its corresponding molecular ID")
uploaded_file = st.file_uploader("Upload", type=['txt'])

if uploaded_file is not None:
    load_data(uploaded_file)
    desc_calc()
    select_fingerprints()
    download_model_from_drive()
    load_model()
    org_fingerprint_df, final_df, prediction = prediction_fingerprints()
    chem_name = org_fingerprint_df[org_fingerprint_df.apply(lambda row: row.astype(str).str.contains('CHEM').any(), axis=1)]
    final_df = pd.concat([pd.Series(chem_name), pd.Series(final_df)], axis=1)
    prediction = pd.concat([pd.Series(chem_name), pd.Series(prediction)], axis=1)
    prediction = prediction.rename(columns={prediction.columns[0]: 'Molecular ID', prediction.columns[1]: 'pIC50'})
    st.header("PaDel-generated Dataset")
    st.write(org_fingerprint_df)
    st.header("Selected Fingerprint Dataset")
    st.write(final_df)
    st.header("Prediction Dataset")
    st.write(prediction)
    filedownload(prediction)
