import streamlit as st

st.set_page_config(
    page_title="DICTrank Predictor",
    page_icon="Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

left_col, right_col = st.columns(2)

right_col.write("# Welcome to DICTrank Predictor")
right_col.write("v1.1.3")
right_col.write("Srijit Seal*[1], Ola Spjuth[2], Layla Hosseini-Gerami[3], Miguel García-Ortegón[4], Shantanu Singh[1], Andreas Bender[4], Anne E. Carpenter[1]")
right_col.write("[1] Imaging Platform, Broad Institute of MIT and Harvard, US; [2] Uppsala University; [3] Ignota Labs, UK; [4] Uppsala University, Sweden")                
left_col.image("Logo.png")



st.sidebar.success("")

st.markdown(
"""
    DICTrank Predictor is an open-source app framework built specifically for
    human drug-induced cardiotoxicity (DICT)  

    DICTrank Predictor employs physicochemical parameters as features.
    
    Select from the sidebar to predict DILI for a single molecule
    For bulk jobs, or local use: see (https://broad.io/DICTrank_Predictor)
    
    ### Want to learn more?
    - Check out our paper at [bioarxiv](https://streamlit.io)
    """
)
st.markdown("---")

left_col, right_col = st.columns(2)

right_col.image("Logo.png")

left_col.markdown(
        """
        ### Usage
        On the left pane is the main menu for navigating to 
        the following pages in the PK Predictor application:
        - **Home Page:** You are here!
        - **Submit single SMILES:** You can enter the smiles of the query compound here to obtain a detailed analysis of the predicted DICTrank and detected structural alerts.
        """
    )
st.markdown("---")


left_info_col, right_info_col = st.columns(2)

left_info_col.markdown(

        f"""
        ### Authors
        
        ##### Srijit Seal 
        - Email:  <seal@broadinstitute.org>
        - GitHub: https://github.com/srijitseal
        """,
        unsafe_allow_html=True,
    )

right_info_col.markdown(
        """
        ### Funding
        Cambridge Centre for Data-Driven Discovery (C2D3) and Accelerate Programme for Scientific Discovery, 
        National Institutes of Health (R35 GM122547 to AEC),
        Swedish Research Council (grants 2020-03731 and 2020-01865), 
        FORMAS (grant 2022-00940), 
        Swedish Cancer Foundation (22 2412 Pj 03 H), 
        Horizon Europe grant agreement #101057014 (PARC) and #101057442 (REMEDI4ALL).
         """
    )

right_info_col.markdown(
        """
        ### License
        Apache License 2.0
        """
    )
