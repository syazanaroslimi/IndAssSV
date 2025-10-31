import pandas as pd
import streamlit as st
import plotly.express as px

# Set the title of the Streamlit app
st.title('Crime Against Women Dataset Viewer 📊')

# Define the URL for the dataset
url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

# Use st.cache_data to load the data efficiently. 
# This tells Streamlit to run the function and cache the return value.
# Future runs will skip executing the function if the inputs haven't changed.
@st.cache_data
def load_data(data_url):
    """Loads the dataset from the specified URL."""
    try:
        data = pd.read_csv(data_url)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on failure

# Load the dataset
caw_dataset = load_data(url)

# Check if the DataFrame is not empty before displaying
if not caw_dataset.empty:
    st.subheader('Head of the Dataset')
    
    # Use st.dataframe to display the entire DataFrame (or st.table for a static table)
    # st.dataframe is generally better for large datasets as it supports interactive features.
    st.dataframe(caw_dataset.head()) 

else:
    st.warning('Could not load or display the dataset.')
