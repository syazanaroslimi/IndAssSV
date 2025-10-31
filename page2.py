import pandas as pd
import streamlit as st
import plotly.express as px

# --- Data Loading Function (Corrected to set the index) ---

st.title('Top 5 Crimes Against Women Analysis 📊')

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
        st.subheader('Top 5 Crime Types by Total Count (2013-2022)')

        # 1. Select the data for analysis
        # Create a copy of the data, excluding the header/label row (iloc[0])
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        
        # 2. Assign meaningful column names (from the first row of the original data)
        caw_data_numeric.columns = caw_dataset.iloc[0]
        
        # 3. Exclude the 'Total Crimes against Women' column
        caw_data_numeric = caw_data_numeric.drop(columns=['Total Crimes against Women'], errors='ignore')

        # 4. Convert all data values to numeric (floats)
        caw_data_numeric = caw_data_numeric.astype(float)
        
        # 5. Calculate the total number of crimes for each type across all years
        crime_totals = caw_data_numeric.sum()
        
        # 6. Get the top 5 crime types
        top_5_crimes_series = crime_totals.nlargest(5)

        # 7. Create a clean DataFrame for Plotly
        plot_data = pd.DataFrame({
            'Type of Crime': top_5_crimes_series.index,
            'Total Crimes': top_5_crimes_series.values
        }).sort_values(by='Total Crimes', ascending=True) # Sort for horizontal bar chart

        # --- Plotly Chart Creation (Replaces plt.barh) ---

        fig = px.bar(
            plot_data,
            x='Total Crimes',      # Set Total Crimes on the horizontal axis
            y='Type of Crime',     # Set Crime Type on the vertical axis
            orientation='h',       # Specify horizontal orientation
            title='Top 5 Crimes Against Women (Total 2013-2022)',
            labels={'Total Crimes': 'Total Number of Crimes', 'Type of Crime': 'Crime Category'},
            text='Total Crimes',
            color='Total Crimes',  # Color the bars based on the total count
            color_continuous_scale=px.colors.sequential.Teal # Use a sequential color scale
        )
        
        # Customize the layout for better readability
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        
        # 8. Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred during chart generation: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')
#________________________________________________________________________________________________________________________________________
# 2nd visualization
# --- Data Preparation and Plotly Chart Creation ---

if not caw_dataset.empty:
    try:
        # 1. Prepare Data: Select individual crimes
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        
        # 2. Assign meaningful column names and clean data
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)
        
        # 3. Identify the Top 5 Crimes
        crime_totals = caw_data_numeric.sum()
        top_5_crime_names = crime_totals.nlargest(5).index.tolist()
        
        # 4. Filter data to include only the Top 5 crimes over time
        top_5_crimes_over_time = caw_data_numeric[top_5_crime_names]

        # 5. Convert the wide DataFrame to a long format for Plotly Express
        # Plotly Express works best with data where each row is a point (Year, Crime Type, Count)
        plot_data_long = top_5_crimes_over_time.reset_index().melt(
            id_vars='index',
            var_name='Type of Crime',
            value_name='Number of Crimes'
        )
        # Rename the 'index' column (which is the year)
        plot_data_long = plot_data_long.rename(columns={'index': 'Year'})

        st.subheader(f"Trend of Top 5 Most Frequent Crimes")

        # --- Plotly Line Chart Creation (Replaces plt.plot) ---

        fig = px.line(
            plot_data_long,
            x='Year',
            y='Number of Crimes',
            color='Type of Crime',  # Color the lines by crime type
            title='Trend of Top 5 Crimes Against Women (2013-2022)',
            markers=True,           # Add markers to the line points
            hover_data={'Year': True, 'Number of Crimes': ':,', 'Type of Crime': True}
        )
        
        # Customize the layout for better year display
        fig.update_xaxes(dtick=1) # Ensure x-axis ticks show every year
        fig.update_yaxes(rangemode="tozero") # Start y-axis from 0

        # 6. Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')

#_____________________________________________________________________________________________________________________________________
# 3rd visualization
# --- Data Preparation and Plotly Chart Creation ---

if not caw_dataset.empty:
    try:
        st.subheader('Yearly Breakdown of Top 5 Crime Types')

        # 1. Prepare Data: Select individual crimes
        caw_data_numeric = caw_dataset.iloc[1:].copy()
        
        # 2. Assign meaningful column names and clean data
        caw_data_numeric.columns = caw_dataset.iloc[0]
        caw_data_numeric = caw_data_numeric.drop(
            columns=['Total Crimes against Women'], 
            errors='ignore'
        )
        caw_data_numeric = caw_data_numeric.astype(float)

        # 3. Identify the Top 5 Crimes
        crime_totals = caw_data_numeric.sum()
        top_5_crime_names = crime_totals.nlargest(5).index.tolist()

        # 4. Filter data to include only the Top 5 crimes over time
        top_5_crimes_over_time = caw_data_numeric[top_5_crime_names]

        # 5. Reset the index and melt the DataFrame into long format (required for grouped bar chart)
        # This is exactly the same, correct reshaping logic you used for Seaborn!
        top_5_crimes_over_time_melted = top_5_crimes_over_time.reset_index().melt(
            id_vars='index', var_name='Type of Crime', value_name='Number of Crimes'
        )

        # 6. Rename the 'index' column to 'Year'
        plot_data = top_5_crimes_over_time_melted.rename(columns={'index': 'Year'})

        # --- Plotly Grouped Bar Chart Creation (Replaces sns.barplot) ---

        fig = px.bar(
            plot_data,
            x='Year',
            y='Number of Crimes',
            color='Type of Crime',  # This acts as the 'hue' argument for grouping
            barmode='group',        # Explicitly set the bars to be grouped side-by-side
            title='Trend of Top 5 Crimes Against Women Over Time (2013-2022)',
            labels={'Number of Crimes': 'Total Number of Crimes'},
            text='Number of Crimes', # Show text labels on the bars
            height=600
        )
        
        # Customize the layout for better data display
        fig.update_xaxes(type='category', dtick=1) # Treat 'Year' as categorical and show every tick
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        # 7. Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')
  
