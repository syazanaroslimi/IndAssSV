import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np # Needed for the triangle mask functionality

# --- Data Loading Function (Crucial for correct Year axis) ---

st.title('Objective 3: ')

url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

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

#________________________________________________________________________________________________________________________________________
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

#_____________________________________________________________________________________________________________________________________
# 3rd visualization
# --- Data Preparation and Plotly Chart Creation ---

if not caw_dataset.empty:
    try:
        st.subheader('Inter-Category Correlation of Crime Rates')

        # 1. Prepare Data: Select individual crimes
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)

        # 2. Calculate the correlation matrix
        correlation_matrix = caw_data_numeric.corr()
        
        # 3. Plotly's imshow works best with numpy arrays or DataFrames directly
        # We will use the DataFrame to retain column/index names
        
        # --- Plotly Heatmap Creation (px.imshow replaces sns.heatmap) ---

        fig = px.imshow(
            correlation_matrix,
            text_auto=".2f", # Automatically display correlation values, formatted to 2 decimals
            aspect="auto",
            color_continuous_scale=px.colors.diverging.RdBu, # Use a divergent scale (Red/Blue for correlation)
            zmin=-1, # Set the color scale minimum to -1 (perfect negative correlation)
            zmax=1,  # Set the color scale maximum to 1 (perfect positive correlation)
            labels=dict(x="Crime Category", y="Crime Category", color="Correlation"),
            title='Correlation Heatmap of Crimes Against Women (2013-2022)'
        )
        
        # Customize text appearance and remove tick marks for cleaner look
        fig.update_traces(hovertemplate="Crime A: %{y}<br>Crime B: %{x}<br>Correlation: %{z}<extra></extra>")
        fig.update_xaxes(side="top", tickangle=45)
        
        # 4. Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')
