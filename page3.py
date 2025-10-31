import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np # Needed for the triangle mask functionality

url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

# --- Data Loading Function ---

st.title('Objective 3: ')

@st.cache_data
def load_data(data_url):
    try:
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
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)

        # 2. Extract data for 2013 and 2022
        crimes_2013 = caw_data_numeric.loc['2013']
        crimes_2022 = caw_data_numeric.loc['2022']

        # 3. Combine the data into a single DataFrame
        comparison_df = pd.DataFrame({'2013': crimes_2013, '2022': crimes_2022})
        
        # 💡 FIX 1: Explicitly name the index to guarantee the column name after reset_index()
        comparison_df.index.name = 'Type of Crime' 

        # 4. Reset index and melt the DataFrame for Plotly
        # Now, reset_index() creates a column called 'Type of Crime', which we use for id_vars
        plot_data = comparison_df.reset_index().melt(
            id_vars='Type of Crime',                 # 💡 FIX 2: Use the correct column name
            var_name='Year', 
            value_name='Number of Crimes'
        )

        # --- Plotly Grouped Bar Chart Creation ---

        fig = px.bar(
            plot_data,
            x='Type of Crime',
            y='Number of Crimes',
            color='Year',          
            barmode='group',       
            title='Crime Comparison: 2013 vs 2022',
            labels={'Type of Crime': 'Crime Category', 'Number of Crimes': 'Total Number of Crimes'},
            height=650
        )
        
        # Improve readability by rotating the x-axis labels
        fig.update_layout(xaxis_tickangle=-45)
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except KeyError as e:
        st.error(f"Data Error: One or more expected labels ('2013', '2022', or 'Type of Crime') were not found. Error detail: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')

#_______________________________________________________________________________________________________________________________________
# 2nd visualization
# --- Data Preparation and Plotly Chart Creation ---

if not caw_dataset.empty:
    try:
        st.subheader('Annual Trend for "Rape" Cases')

        # 1. Prepare Data: Select individual crimes and clean
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)

        # 2. Select the data for 'Rape'
        rape_trend = caw_data_numeric['Rape']

        # 3. Create a clean DataFrame for Plotly
        plot_data = pd.DataFrame({
            'Year': rape_trend.index, # The index (Years) is correctly used as the X-axis
            'Number of Cases': rape_trend.values
        })

        # --- Plotly Line Chart Creation (Replaces plt.plot) ---

        fig = px.line(
            plot_data,
            x='Year',
            y='Number of Cases',
            title='Trend of Rape Cases (2013-2022)',
            markers=True,
            # Add a color gradient based on the number of cases
            color_continuous_scale=px.colors.sequential.Sunset,
            height=500
        )
        
        # Customize the layout for better year display
        fig.update_xaxes(dtick=1) # Ensure x-axis ticks show every year
        fig.update_yaxes(rangemode="tozero") # Start y-axis from 0

        # 4. Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except KeyError:
        st.error("Error: Could not find the column 'Rape'. Check the crime category names.")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')

#______________________________________________________________________________________________________________________________________
# 3rd visualization
