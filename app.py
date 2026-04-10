import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.set_page_config(
    page_title="Water Potability Predictor",
    layout="centered"
)

model = joblib.load("best_water_potability_model.pkl")

st.title(" Water Potability Prediction System")

st.write(
"""
Enter the water quality parameters below to determine  
whether the water is **safe to drink** or **not potable**.
"""
)

st.header("Water Quality Inputs")

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH", 0.0, 14.0, 7.0)
    hardness = st.number_input("Hardness", value=150.0)
    solids = st.number_input("Solids", value=10000.0)
    chloramines = st.number_input("Chloramines", value=7.0)
    sulfate = st.number_input("Sulfate", value=300.0)

with col2:
    conductivity = st.number_input("Conductivity", value=400.0)
    organic_carbon = st.number_input("Organic Carbon", value=10.0)
    trihalomethanes = st.number_input("Trihalomethanes", value=60.0)
    turbidity = st.number_input("Turbidity", value=4.0)

if st.button("Predict Water Quality"):

    input_data = pd.DataFrame([{
        "ph": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "Organic_carbon": organic_carbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.header("Water Quality Report")

    if prediction == 1:
        st.success(" Water is POTABLE (Safe to Drink)")
    else:
        st.error(" Water is NOT POTABLE")

    st.metric(
        label="Potability Probability",
        value=f"{probability:.2f}"
    )

    st.subheader("Input Summary")

    st.dataframe(input_data)

    st.subheader("Interpretation")

    if probability > 0.75:
        st.success("Water quality is highly likely safe.")

    elif probability > 0.50:
        st.warning("Water quality is borderline safe.")

    else:
        st.error("Water quality is unsafe.")