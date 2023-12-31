#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
import numpy as np
from rdkit import Chem
from mordred import Calculator, descriptors
import pickle
from scripts.standardise_smiles_local_implementation import standardize_jumpcp
from rdkit.Chem import Draw

def main():
    
    # Create Streamlit app
    st.title("DICTrank Predictor")
    
    # Input SMILES
    smiles = st.text_input("Enter SMILES")
    
    if st.button('Predict DICTrank'):
        with st.spinner('Calculating...'):
            if(smiles==''):
                st.write("No input provided")
                st.success("Fail!")
                st.stop()
            
            try:
    
                # Load data_columns from the .pkl file
                with open('features/data_columns.pkl', 'rb') as file:
                    data_columns = pickle.load(file)
                
                # Create a DataFrame with a single column "SMILES"
                df = pd.DataFrame({'SMILES': [smiles]})
                df['Standardized_SMILES'] = df['SMILES'].apply(standardize_jumpcp)
                
                # Initialize Mordred calculator
                calc = Calculator(descriptors, ignore_3D=True)
                
                # Calculate Mordred descriptors
                Ser_Mol = df['Standardized_SMILES'].apply(Chem.MolFromSmiles)
                Mordred_table = calc.pandas(Ser_Mol)
                Mordred_table = Mordred_table.astype('float')
                
                # Retain only those columns in the test dataset
                Mordred_table = Mordred_table[data_columns]
                
                # Handle NaN and inf values
                X = np.array(Mordred_table)
                X[np.isnan(X)] = 0
                X[np.isinf(X)] = 0
                
                # Load the classifier model
                classifier = pickle.load(open("model/FINAL_Physicochemical_model.sav", 'rb'))
                
                # Predict DICTrank
                prob_test = classifier.predict_proba(X)[:, 1]
                df["Probability"] = prob_test
                df["Prediction"] = (prob_test >= 0.641338).astype(int)
                
                dpi = 300
                molSize = (300, 300)
                
                mol = Chem.MolFromSmiles(df['Standardized_SMILES'].values[0])
                mol_img =  Draw.MolToImage(mol, size=molSize, dpi=dpi)
                st.image(mol_img)
                
                if df["Prediction"][0] == 1:
                    cardiotoxicity_status = "This compound is predicted as **_cardiotoxic_**."
                else:
                    cardiotoxicity_status = "This compound is predicted as **_not cardiotoxic_**."
                
                st.subheader("Cardiotoxicity Prediction:")
                st.write(cardiotoxicity_status)
                
                st.write("Predicted DICTrank:", df["Prediction"].values[0])
                st.write("Predicted DICTrank probability:", np.round(df["Probability"].values[0], 2))
                st.write("Threshold for Cardiotoxicity:", np.round(0.641338, 2))
                
                # Visualization of substructures
                # Convert the substructure strings into Mol objects
                DICT_rank_substructures_ppv1 = [ "C=CCCC(=O)", "CCOCCC[NH+](C)C", "C(CCCCCC(O)CCC)C(=O)", "CC[NH+](CC(=O)[O-])CCNC", "CCC[NH+](C)C(C(=O)[O-])", "CC(C[N+](C)(C))OC"]
                
                DICT_Concern_substructures = ['CCOCCC[NH+](C)C', 'CN(C)c1ccccn1']
                
                DICT_Concern_mols = [Chem.MolFromSmiles(smiles) for smiles in DICT_Concern_substructures]
                
                DICT_rank_mols = [Chem.MolFromSmiles(smiles) for smiles in DICT_rank_substructures_ppv1]
                
                
                
                
                # Create a Streamlit column for the molecule image
                col1, col2 = st.columns(2)
                
                # Define a function to check and display substructures
                def check_and_display_substructure(sub_mol):
                    if mol.HasSubstructMatch(sub_mol):
                        main_img = Draw.MolToImage(mol, size=molSize, highlightAtoms=mol.GetSubstructMatch(sub_mol), dpi=dpi)
                        sub_img = Draw.MolToImage(sub_mol, dpi=dpi)
                        return main_img, sub_img
                    return None, None
                
                # Display DICTrank substructures if alerts are present
                if any(mol.HasSubstructMatch(sub_mol) for sub_mol in DICT_rank_mols):
                    col1.subheader("Structural Alerts for DICTrank 1")
                    for sub_mol in DICT_rank_mols:
                        main_img, sub_img = check_and_display_substructure(sub_mol)
                        if main_img is not None:
                            col1.image(main_img)
                            col1.image(sub_img)
                
                # Display DICT Most-concern category substructures if alerts are present
                if any(mol.HasSubstructMatch(sub_mol) for sub_mol in DICT_Concern_mols):
                    col2.subheader("Structural Alerts for DICT Most-concern category")
                    for sub_mol in DICT_Concern_mols:
                        main_img, sub_img = check_and_display_substructure(sub_mol)
                        if main_img is not None:
                            col2.image(main_img)
                            col2.image(sub_img)

                st.success("Successful")
                
            except: 
                if (smiles==' '):
                    st.write(f"Empty SMILES : Unsuccessful!")
                else:
                    st.write(f"{smiles} Unsuccessful! Check SMILES")
                
                st.success("Unsuccessful")
                    
if __name__ == '__main__': 
    main()   

