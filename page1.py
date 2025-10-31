import pandas as pd
import streamlit as st
import plotly.express as px

# Set the title of the Streamlit app
#st.title('Crime Against Women Dataset Viewer 📊')

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
#if not caw_dataset.empty:
    #st.subheader('Head of the Dataset')
    
    # Use st.dataframe to display the entire DataFrame (or st.table for a static table)
    # st.dataframe is generally better for large datasets as it supports interactive features.
    #st.dataframe(caw_dataset.head()) 

#else:
    #st.warning('Could not load or display the dataset.')
#_____________________________________________________________________________________________________________________________
# 1st visualization
# Set the title of the Streamlit app
st.title('Objective 1: ')

# Check if the DataFrame is available and not empty (from the previous steps)
if 'caw_dataset' in locals() and not caw_dataset.empty:
    try:
        # --- Data Preparation Steps from the original code ---
        # 1. Find the column index for 'Total Crimes against Women'
        # The first row contains the crime type names as values
        # Find the index name (column name) where the first row value is 'Total Crimes against Women'
        column_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]

        # 2. Select the data, exclude the first row (crime type names), and convert to integer
        # The index (which should be the year) is kept as the index
        total_crimes_series = caw_dataset.iloc[1:][column_name].astype(int)

        # 3. Create a DataFrame suitable for Plotly
        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series.index), # Convert index (years) to numeric
            'Number of Crimes': total_crimes_series.values
        })
        
        st.subheader('Trend of Total Crimes against Women (2013-2022)')

        # --- Plotly Chart Creation ---
        # Create an interactive line chart using Plotly Express
        fig = px.line(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022',
            markers=True # Add markers to the line
        )
        
        # Customize the layout for better readability
        fig.update_layout(xaxis_tickformat='d') # Ensure years are displayed as integers
        fig.update_xaxes(dtick=1) # Set x-axis ticks to every year

        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except IndexError:
        st.error("Error: Could not find the column 'Total Crimes against Women'. Check the dataset's structure.")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
else:
    st.warning('The `caw_dataset` is not loaded or is empty. Please ensure the data loading step runs successfully.')

#_______________________________________________________________________________________________________________________________________
# 2nd visualization
if not caw_dataset.empty:
    try:
        st.subheader('Trend of Total Crimes against Women (2013-2022)')

        # 1. Find the actual column name that corresponds to 'Total Crimes against Women' 
        # (This is necessary because the data structure is unusual: crime type names are in row 0)
        column_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]

        # 2. Select the data, exclude the first row (the column header row), and convert values to integer
        total_crimes_series = caw_dataset.iloc[1:][column_name].astype(int)

        # 3. Create a clean DataFrame for Plotly (Plotly prefers explicit columns for X and Y)
        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series.index),
            'Number of Crimes': total_crimes_series.values
        })
        
        # --- Plotly Bar Chart Creation (Replaces plt.bar) ---

        fig = px.bar(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022',
            text='Number of Crimes',  # Display the value on top of the bar
            color='Number of Crimes', # Optional: color the bars by the value
            color_continuous_scale=px.colors.sequential.Teal
        )

        # Customizing the layout
        fig.update_traces(textposition='outside') # Move text labels outside the bar
        fig.update_layout(xaxis_tickformat='d') # Ensure years are displayed as integers
        fig.update_xaxes(dtick=1) # Set x-axis ticks to every year

        # 4. Display the Plotly chart in Streamlit (Replaces plt.show())
        st.plotly_chart(fig, use_container_width=True)

    except IndexError:
        st.error("Error: Could not find the column 'Total Crimes against Women'. Check the dataset's structure.")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
else:
    st.warning('The dataset is not loaded or is empty. Please check the URL.')

#_____________________________________________________________________________________________________________________________________
# 3rd visualization
if not caw_dataset.empty:
    try:
        st.subheader('Heatmap of Crimes against Women (2013-2022)')

        # Create a copy to avoid modifying the original DataFrame and potential SettingWithCopyWarning
        heatmap_data_prep = caw_dataset.iloc[1:].copy()

        # Set the column names from the first row of the original dataset
        # This makes the crime types the actual column headers
        heatmap_data_prep.columns = caw_dataset.iloc[0]

        # Convert the index to numeric (Years)
        heatmap_data_prep.index = pd.to_numeric(heatmap_data_prep.index)
        heatmap_data_prep.index.name = 'Year'

        # Exclude the 'Total Crimes against Women' column
        if 'Total Crimes against Women' in heatmap_data_prep.columns:
            heatmap_data_prep = heatmap_data_prep.drop(columns=['Total Crimes against Women'])
        else:
            st.warning("'Total Crimes against Women' column not found for exclusion.")

        # Convert the remaining data to numeric, coercing errors to NaN
        # This is important for Plotly to render the heatmap correctly
        heatmap_data_numeric = heatmap_data_prep.astype(float)

        # Drop any columns that became all NaN after conversion, if necessary
        heatmap_data_numeric = heatmap_data_numeric.dropna(axis=1, how='all')
        
        # --- Plotly Heatmap Creation (Replaces sns.heatmap) ---

        if not heatmap_data_numeric.empty:
            fig = px.imshow(
                heatmap_data_numeric,
                x=heatmap_data_numeric.columns,  # Crime types on x-axis
                y=heatmap_data_numeric.index,    # Years on y-axis
                color_continuous_scale=px.colors.sequential.Hot, # Or 'Hot', 'Viridis', etc.
                title='Heatmap of Crimes against Women (2013-2022)',
                aspect="auto", # Adjust aspect ratio
                text_auto=True # Automatically add text labels to cells
            )
            
            # Optional: Further customize hover info or layout if needed
            fig.update_xaxes(side="top") # Move crime type labels to the top for better readability
            fig.update_layout(
                height=700, # Adjust height for better display of many rows
                margin=dict(l=50, r=50, t=80, b=50) # Adjust margins
            )

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Heatmap data is empty after processing. No heatmap to display.")

    except Exception as e:
        st.error(f"An error occurred during heatmap generation: {e}")
else:
    st.warning('The dataset is not loaded or is empty. Please check the URL and data loading process.')



