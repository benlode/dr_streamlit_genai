import streamlit as st
import requests

# Function to call your API
def call_api(input_data):
    # Replace with your API endpoint and input format
    api_endpoint = "http://your-api-endpoint.com/predict"
    response = requests.post(api_endpoint, json={"data": input_data})
    return response.json()

# Streamlit app layout
st.title("Model Prediction App")

# UI to take user input
user_input = st.text_input("Enter input for the model")

# Button to call the API
if st.button("Get Prediction"):
    # Call the API and display the result
    result = call_api(user_input)
    st.write("Prediction:", result)

# Run this script using `streamlit run your_script_name.py`
