import pandas as pd
import streamlit as st
import plotly.express as px

# Define the URL for the dataset
url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

# Use st.cache_data to load the data efficiently. 
@st.cache_data
def load_data(data_url):
    """Loads the dataset from the specified URL."""
    try:
        data = pd.read_csv(data_url, index_col=0)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Helper function to prepare data for metrics and visualizations
@st.cache_data
def prepare_data_for_metrics(caw_dataset):
    if caw_dataset.empty: return None, None
    
    caw_data_numeric = caw_dataset.iloc[1:].copy()
    caw_data_numeric.columns = caw_dataset.iloc[0]
    
    # Find the 'Total Crimes against Women' series
    total_col_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]
    total_crimes_series = caw_data_numeric[total_col_name].astype(float)
    
    # Drop total column to get only individual crimes
    individual_crimes_df = caw_data_numeric.drop(
        columns=[total_col_name], 
        errors='ignore'
    ).astype(float)
    
    return individual_crimes_df, total_crimes_series

# Load and prepare the dataset
caw_dataset = load_data(url)
individual_crimes_df, total_crimes_series = (prepare_data_for_metrics(caw_dataset) 
                                            if not caw_dataset.empty else (None, None))

st.title('Objective 1: ')

# --- 1. SUMMARY METRIC BOX PLACEMENT ---
if total_crimes_series is not None:
    # 1. Total Cases over the Decade
    total_decade_cases = total_crimes_series.sum()
    
    # 2. Peak Year & Value
    peak_year = int(total_crimes_series.idxmax())
    peak_value = total_crimes_series.max()

    # 3. Overall Change (2022 vs 2013)
    start_value = total_crimes_series.loc['2013']
    end_value = total_crimes_series.loc['2022']
    absolute_change = end_value - start_value
    percent_change = (absolute_change / start_value) * 100
    
    # 4. Highest Volume Crime
    total_by_crime = individual_crimes_df.sum(axis=0)
    highest_crime = total_by_crime.idxmax()
    
col1, col2, col3, col4 = st.columns(4)
    
col1.metric(
    label="Total Cases (2013-2022)", 
    value=f"{total_decade_cases:,.0f}", 
    help="Cumulative number of all reported crimes.",
    delta="Decade Volume"
)
col2.metric(
    label="Peak Year Reported", 
    value=f"{peak_year}", 
    help=f"Year with the highest number of reported total crimes: {peak_value:,.0f}",
    delta="Highest Volume"
)
col3.metric(
    label="Decade Change (2013 vs 2022)", 
    value=f"{percent_change:+.2f}%", 
    help=f"Total percent change in reported cases from 2013 to 2022. Absolute change: {absolute_change:+,0f} cases.",
    delta_color="normal"
)
col4.metric(
    label="Highest Volume Category", 
    value=highest_crime, 
    help=f"Crime category with the most reported cases over the entire decade: {highest_crime[:20]}...",
    delta="Largest Category"
)

st.markdown("---")
# ----------------------------------------------


# _____________________________________________________________________________________________________________________________
# 1st visualization: Total Crimes - Line Chart
if 'caw_dataset' in locals() and not caw_dataset.empty:
    try:
        st.subheader('1. Trend of Total Crimes against Women (2013-2022)')

        # --- Data Preparation ---
        column_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]
        total_crimes_series_vis = caw_dataset.iloc[1:][column_name].astype(int)

        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series_vis.index),
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # --- Plotly Chart Creation ---
        fig = px.line(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022',
            markers=True
        )
        
        fig.update_layout(xaxis_tickformat='d')
        fig.update_xaxes(dtick=1)

        st.plotly_chart(fig, use_container_width=True)

    except IndexError:
        st.error("Error: Could not find the column 'Total Crimes against Women'. Check the dataset's structure.")
    except Exception as e:
        st.error(f"An unexpected error occurred during plotting (Vizu 1): {e}")
else:
    st.warning('The `caw_dataset` is not loaded or is empty. Please ensure the data loading step runs successfully.')

# _______________________________________________________________________________________________________________________________________
# 2nd visualization: Total Crimes - Bar Chart
if not caw_dataset.empty:
    try:
        st.subheader('2. Trend of Total Crimes against Women (2013-2022)')

        # --- Data Preparation (using data from previous block) ---
        column_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]
        total_crimes_series_vis = caw_dataset.iloc[1:][column_name].astype(int)

        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series_vis.index),
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # --- Plotly Bar Chart Creation ---
        fig = px.bar(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022',
            text='Number of Crimes',
            color='Number of Crimes',
            color_continuous_scale=px.colors.sequential.Teal
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickformat='d')
        fig.update_xaxes(dtick=1)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting (Vizu 2): {e}")

# _____________________________________________________________________________________________________________________________________
# 3rd visualization: Heatmap of all Crimes vs. Year
if not caw_dataset.empty:
    try:
        st.subheader('3. Annual Distribution of All Crime Categories')

        # --- Data Preparation ---
        heatmap_data_prep = caw_dataset.iloc[1:].copy()
        heatmap_data_prep.columns = caw_dataset.iloc[0]
        heatmap_data_prep.index = pd.to_numeric(heatmap_data_prep.index)
        heatmap_data_prep.index.name = 'Year'

        if 'Total Crimes against Women' in heatmap_data_prep.columns:
            heatmap_data_prep = heatmap_data_prep.drop(columns=['Total Crimes against Women'])

        heatmap_data_numeric = heatmap_data_prep.astype(float)
        heatmap_data_numeric = heatmap_data_numeric.dropna(axis=1, how='all')
        
        # --- Plotly Heatmap Creation ---
        if not heatmap_data_numeric.empty:
            fig = px.imshow(
                heatmap_data_numeric,
                x=heatmap_data_numeric.columns,
                y=heatmap_data_numeric.index,
                color_continuous_scale=px.colors.sequential.Teal,
                title='Magnitude of Crimes by Category and Year',
                aspect="auto",
                text_auto=True
            )
            
            fig.update_xaxes(side="bottom", tickangle=90)
            fig.update_layout(
                height=700,
                margin=dict(l=50, r=50, t=80, b=50)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Heatmap data is empty after processing. No heatmap to display.")

    except Exception as e:
        st.error(f"An error occurred during heatmap generation (Vizu 3): {e}")

# --- 2. INTERPRETATION BOX PLACEMENT ---
if not caw_dataset.empty:
    st.markdown("---")
    st.markdown("""
    <div style='padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;'>
    <h4>Summary: Decade-Long Overview</h4>
    <p>This page provides a high-level view of crimes against women in India from 2013 to 2022. We begin by analyzing the trend in total reported crimes and then visualize the annual distribution across all individual crime categories to identify where the bulk of the volume lies.</p>
</div>
    """, unsafe_allow_html=True)
# ----------------------------------------------------
