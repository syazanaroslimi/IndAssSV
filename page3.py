import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np # Needed for the triangle mask functionality

# Define the URL (assuming this is defined globally in your Streamlit app)
#url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

# --- Data Loading Function (Crucial for correct Year axis) ---

st.title('Crime Comparison: 2013 vs 2022 Analysis 📊')

@st.cache_data
def load_data(data_url):
    """
    Loads the dataset, setting the first column (containing the years) as the index.
    """
    try:
        # Corrected loading: index_col=0 sets the years as the DataFrame index
        data = pd.read_csv(data_url, index_col=0) 
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

caw_dataset = load_data(url)

# --- Data Preparation and Plotly Chart Creation ---
# 1st visualization
if not caw_dataset.empty:
    try:
        st.subheader('Crime Count Comparison by Type: 2013 vs 2022')

        # 1. Prepare Data: Select individual crimes
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        
        # 2. Assign meaningful column names and clean data
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)

        # 3. Extract data for 2013 and 2022
        # .loc['2013'] and .loc['2022'] rely on the corrected index_col=0 during load
        crimes_2013 = caw_data_numeric.loc['2013']
        crimes_2022 = caw_data_numeric.loc['2022']

        # 4. Combine the data into a single DataFrame
        comparison_df = pd.DataFrame({'2013': crimes_2013, '2022': crimes_2022})

        # 5. Reset index and melt the DataFrame for Plotly
        comparison_df_melted = comparison_df.reset_index().melt(
            id_vars='index', var_name='Year', value_name='Number of Crimes'
        )
        
        # 6. Rename the 'index' column to 'Type of Crime' for clarity
        plot_data = comparison_df_melted.rename(columns={'index': 'Type of Crime'})

        # --- Plotly Grouped Bar Chart Creation (Replaces sns.barplot) ---

        fig = px.bar(
            plot_data,
            x='Type of Crime',
            y='Number of Crimes',
            color='Year',          # Group and color the bars by Year
            barmode='group',       # Explicitly set the bars to be grouped side-by-side
            title='Crime Comparison: 2013 vs 2022',
            labels={'Type of Crime': 'Crime Category', 'Number of Crimes': 'Total Number of Crimes'},
            height=650
        )
        
        # Improve readability by rotating the x-axis labels
        fig.update_layout(xaxis_tickangle=-45)
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except KeyError as e:
        st.error(f"Error: Could not find year or column index {e}. Ensure the data is loaded correctly and years '2013' and '2022' exist as the index.")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')
