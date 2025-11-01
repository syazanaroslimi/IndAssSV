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
        # Load data with the first column (Year) as the index
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
    
    # Set human-readable column names from the original first row
    caw_data_numeric.columns = caw_dataset.iloc[0]
    
    # Convert index (Year) to numeric (integer) for consistent access
    try:
        caw_data_numeric.index = pd.to_numeric(caw_data_numeric.index, errors='coerce').astype('Int64')
    except Exception as e:
        st.warning(f"Could not convert index to numeric: {e}")
        
    
    # --- FIX APPLIED HERE: Access column directly by the new, correct name ---
    TOTAL_CRIMES_KEY = 'Total Crimes against Women'
    
    # Access the series using the correct string key
    total_crimes_series = caw_data_numeric[TOTAL_CRIMES_KEY].astype(float)
    
    # Drop total column to get only individual crimes
    individual_crimes_df = caw_data_numeric.drop(
        columns=[TOTAL_CRIMES_KEY], 
        errors='ignore'
    ).astype(float)
    
    return individual_crimes_df, total_crimes_series

# Load and prepare the dataset
caw_dataset = load_data(url)
individual_crimes_df, total_crimes_series = (prepare_data_for_metrics(caw_dataset) 
                                            if not caw_dataset.empty else (None, None))

st.title('Objective 1: Analysis of Overall Trends and Distribution')

# --- 1. SUMMARY METRIC BOX PLACEMENT ---
if total_crimes_series is not None and not total_crimes_series.empty:
    
    # 1. Total Cases over the Decade
    total_decade_cases = total_crimes_series.sum()
    
    # 2. Peak Year & Value
    peak_year = int(total_crimes_series.idxmax())
    peak_value = total_crimes_series.max()

    # 3. Highest Volume Crime
    total_by_crime = individual_crimes_df.sum(axis=0)
    highest_crime = total_by_crime.idxmax()
    
    # Streamlit Metric Columns (3 columns for 3 key metrics)
    col1, col2, col3 = st.columns(3)
    
    col1.metric(
        label="Total Cases (2013-2022)", 
        value=f"{total_decade_cases:,.0f}", 
        help="Cumulative number of all reported crimes over the 10-year period."
    )
    col2.metric(
        label="Peak Reporting Year", 
        value=f"{peak_year}", 
        help=f"Year with the highest total number of reported crimes: {peak_value:,.0f} cases."
    )
    col3.metric(
        label="Primary Crime Category", 
        value=highest_crime, 
        help="The crime category with the highest total volume reported over the entire decade."
    )

st.markdown("---")
# ----------------------------------------------


# _____________________________________________________________________________________________________________________________
# 1st visualization: Total Crimes - Line Chart
if 'caw_dataset' in locals() and not caw_dataset.empty:
    try:
        st.subheader('1. Trend of Total Crimes against Women (2013-2022) - Line View')

        # Use the prepared series for visualization for consistency
        total_crimes_series_vis = total_crimes_series.astype(int) 

        plot_data = pd.DataFrame({
            'Year': total_crimes_series_vis.index,
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # --- Plotly Chart Creation ---
        fig = px.line(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022 (Line)',
            markers=True
        )
        
        fig.update_layout(xaxis_tickformat='d')
        fig.update_xaxes(dtick=1)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting (Vizu 1): {e}")
else:
    st.warning('The `caw_dataset` is not loaded or is empty. Please ensure the data loading step runs successfully.')

# _______________________________________________________________________________________________________________________________________
# 2nd visualization: Total Crimes - Bar Chart
if not caw_dataset.empty:
    try:
        st.subheader('2. Trend of Total Crimes against Women (2013-2022) - Bar View')

        # --- Data Preparation (using prepared data) ---
        total_crimes_series_vis = total_crimes_series.astype(int)

        plot_data = pd.DataFrame({
            'Year': total_crimes_series_vis.index,
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # --- Plotly Bar Chart Creation ---
        fig = px.bar(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='Trend of Total Crimes against Women From 2013 to 2022 (Bar)',
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
        # Ensure year index is numeric for plotting consistency
        heatmap_data_prep.index = pd.to_numeric(heatmap_data_prep.index, errors='coerce').astype('Int64')
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
    <div style='padding: 15px; border-radius: 10px; border-right: 5px solid #FF9800;'>
        <h4>Interpretation & Conclusion for Objective 1</h4>
        <p>The **Line and Bar Charts (1 & 2)** consistently show the overall volume of reported crimes over the decade. We observe a general upward trend, indicating that the total number of reported cases has increased from 2013 to 2022. This could be due to genuine growth in incidence or better reporting mechanisms and increased public awareness.</p>
        <p>The **Heatmap (3)** visually reinforces this by showing that most crime categories display higher numbers in the later years (darker shades at the bottom of the map). Crucially, the heatmap shows that categories like 'Cruelty by Husband or his Relatives' and 'Kidnapping & Abduction' contribute the largest volume to the annual totals, driving the overall upward trend observed in the first two visualizations.</p>
    </div>
    """, unsafe_allow_html=True)
# ----------------------------------------------------
