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

# Helper function to prepare data for metrics and visualization
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
        
    TOTAL_CRIMES_KEY = 'Total Crimes against Women'   # access column directly
    total_crimes_series = caw_data_numeric[TOTAL_CRIMES_KEY].astype(float)       # access the series using string key
    
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

st.title('Objective 1: To analyse the annual trends and patterns of crimes against women in India from 2013 to 2022')

# summary box
if total_crimes_series is not None and not total_crimes_series.empty:
    
    # 1. Total Cases over the Decade
    total_decade_cases = total_crimes_series.sum()
    
    # 2. Peak Year & Value
    peak_year = int(total_crimes_series.idxmax())
    peak_value = total_crimes_series.max()

    # 3. Highest Volume Crime
    total_by_crime = individual_crimes_df.sum(axis=0)
    highest_crime = total_by_crime.idxmax()
    
    # metrics column (3 columns for 3 key metrics)
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
        help="The crime with the highest total volume reported over the entire decade."
    )

st.markdown("---")
# ----------------------------------------------

# _____________________________________________________________________________________________________________________________
# 1st visualisation - line chart
if 'caw_dataset' in locals() and not caw_dataset.empty:
    try:
        #st.subheader('1. Trend of Total Crimes against Women (2013-2022) - Line View')
        # Use the prepared series for visualization for consistency
        total_crimes_series_vis = total_crimes_series.astype(int) 

        plot_data = pd.DataFrame({
            'Year': total_crimes_series_vis.index,
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # Plotly Chart Creation
        fig = px.line(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='1. Trend of Total Crimes against Women From 2013 to 2022',
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
# 2nd visualisation - bar chart
if not caw_dataset.empty:
    try:
        #st.subheader('2. Trend of Total Crimes against Women (2013-2022) - Bar View')
        total_crimes_series_vis = total_crimes_series.astype(int)

        plot_data = pd.DataFrame({
            'Year': total_crimes_series_vis.index,
            'Number of Crimes': total_crimes_series_vis.values
        })
        
        # Chart Creation
        fig = px.bar(
            plot_data,
            x='Year',
            y='Number of Crimes',
            title='2. Total Crimes against Women From 2013 to 2022',
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
# 3rd visualisation: heatmap of all crimes vs. year
if not caw_dataset.empty:
    try:
        #st.subheader('3. Annual Distribution of All Crime Categories')
        # data preparation
        heatmap_data_prep = caw_dataset.iloc[1:].copy()
        heatmap_data_prep.columns = caw_dataset.iloc[0]
        # Ensure year index is numeric for plotting consistency
        heatmap_data_prep.index = pd.to_numeric(heatmap_data_prep.index, errors='coerce').astype('Int64')
        heatmap_data_prep.index.name = 'Year'

        if 'Total Crimes against Women' in heatmap_data_prep.columns:
            heatmap_data_prep = heatmap_data_prep.drop(columns=['Total Crimes against Women'])

        heatmap_data_numeric = heatmap_data_prep.astype(float)
        heatmap_data_numeric = heatmap_data_numeric.dropna(axis=1, how='all')
        
        # Heatmap Creation 
        if not heatmap_data_numeric.empty:
            fig = px.imshow(
                heatmap_data_numeric,
                x=heatmap_data_numeric.columns,
                y=heatmap_data_numeric.index,
                color_continuous_scale=px.colors.sequential.Teal,
                title='3. Heatmap of Crimes by Category and Year',
                aspect="auto",
                text_auto=True
            )
            
            fig.update_xaxes(side="bottom", tickangle=45)
            fig.update_layout(
                height=700,
                margin=dict(l=50, r=50, t=80, b=50)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Heatmap data is empty after processing. No heatmap to display.")

    except Exception as e:
        st.error(f"An error occurred during heatmap generation (Vizu 3): {e}")

# interpretation box
if not caw_dataset.empty:
    st.markdown("---")
    st.markdown("""
    <div style='padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;'>
    <h4>Interpretation</h4>
    <p>All graph show the overall trend of crimes against women in India increasing gradually from 2013 to 2022 with a slight decrease in 2020. 
    This pattern shows woman's safety in India is still at a low level.</p>
</div>
    """, unsafe_allow_html=True)
# ----------------------------------------------------
