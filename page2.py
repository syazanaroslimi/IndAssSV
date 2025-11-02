import pandas as pd
import streamlit as st
import plotly.express as px

# Define the URL for the dataset
url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'
TOTAL_CRIMES_KEY = 'Total Crimes against Women'

# data preparation
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

@st.cache_data
def prepare_page2_data(caw_dataset):
    """Prepares data specifically for Objective 2 metrics and visualizations."""
    if caw_dataset.empty:
        return None, None, None, None

    # Clean DataFrames
    caw_data_numeric = caw_dataset.iloc[1:].copy()
    caw_data_numeric.columns = caw_dataset.iloc[0]
    
    caw_data_numeric.index = pd.to_numeric(caw_data_numeric.index, errors='coerce').astype('Int64')     # convert index (year) to numeric
    
    # Isolate individual crime data
    individual_crimes_df = caw_data_numeric.drop(
        columns=[TOTAL_CRIMES_KEY], 
        errors='ignore'
    ).astype(float)
    
    total_crimes_series = caw_data_numeric[TOTAL_CRIMES_KEY].astype(float)    # isolate total crimes data

    # Identify Top 5 Crimes
    crime_totals = individual_crimes_df.sum()
    top_5_crime_names = crime_totals.nlargest(5).index.tolist()
    
    top_5_crimes_over_time = individual_crimes_df[top_5_crime_names]    # filter data for top 5 crimes over time
    
    # Melt the Top 5 data for Plotly Express (Long Format)
    plot_data_long = top_5_crimes_over_time.reset_index().melt(
        id_vars='index',
        var_name='Type of Crime',
        value_name='Number of Crimes'
    ).rename(columns={'index': 'Year'})

    # Calculate Metrics
    # M1: Most Frequent Crime (The name) 
    most_frequent_crime = top_5_crime_names[0]  # not use in summary box
    
    total_top_5_cases = top_5_crimes_over_time.sum().sum()     # M2: Total Top 5 Cases

    # M3: Contribution of Top 5 (%)
    grand_total_all_crimes = total_crimes_series.sum()
    contribution_percent = (total_top_5_cases / grand_total_all_crimes) * 100

    # M4: Fastest Growing Crime (Top 5 only)
    # Calculate % change from 2013 to 2022 for each of the Top 5
    start_year_data = top_5_crimes_over_time.loc[2013]
    end_year_data = top_5_crimes_over_time.loc[2022]
    
    change = ((end_year_data - start_year_data) / start_year_data) * 100
    fastest_growing_crime = change.idxmax()
    fastest_growth_percent = change.max()

    return top_5_crimes_over_time, plot_data_long, most_frequent_crime, total_top_5_cases, contribution_percent, fastest_growing_crime, fastest_growth_percent

# Load the dataset
caw_dataset = load_data(url)

(
    top_5_crimes_df, plot_data_long, 
    most_frequent_crime, total_top_5_cases, 
    contribution_percent, fastest_growing_crime, 
    fastest_growth_percent
) = prepare_page2_data(caw_dataset)

st.title('Objective 2: To identify the top 5 crime categories and access the changing patterns of major crime rates from 2013 to 2022')

# summary box
if top_5_crimes_df is not None:
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric(
        label="Total Cases (Top 5)", 
        value=f"{total_top_5_cases:,.0f}", 
        help="Cumulative cases reported across the top 5 categories for 10-decade."
    )
    col2.metric(
        label="Top 5 Contribution", 
        value=f"{contribution_percent:,.1f}%", 
        help="Percentage of the grand total of all crimes accounted for by the top 5 categories."
    )
    col3.metric(
        label="Fastest Growing Top 5 Crime", 
        value=fastest_growing_crime, 
        delta=f"{fastest_growth_percent:+.1f}%",
        delta_color="inverse", # Red for growth in crime
        help="The Top 5 crime type that saw the largest percentage increase from 2013 to 2022."
    )

st.markdown("---")
# ----------------------------------------------

# --- 3. Visualizations ---

if not caw_dataset.empty and top_5_crimes_df is not None:
    try:
        # --- VIZ 1: Top 5 Crime Totals (Horizontal Bar Chart) ---
        st.subheader('1. Total Count of Top 5 Crime Categories')
        
        # Calculate totals for Vizu 1
        crime_totals = top_5_crimes_df.sum().sort_values(ascending=True)
        plot_data_v1 = pd.DataFrame({
            'Type of Crime': crime_totals.index,
            'Total Crimes': crime_totals.values
        })

        fig1 = px.bar(
            plot_data_v1,
            x='Total Crimes', 
            y='Type of Crime',
            orientation='h',
            title='Top 5 Most Frequent Crimes Against Women (Total 2013-2022)',
            labels={'Total Crimes': 'Total Number of Crimes', 'Type of Crime': 'Crime Category'},
            text='Total Crimes',
            color='Total Crimes',
            color_continuous_scale=px.colors.sequential.Teal
        )
        
        fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

        
        # --- VIZ 2: Trend of Top 5 (Multi-Line Chart) ---
        st.subheader(f"2. Trend of Top 5 Most Frequent Crimes Over Time")

        fig2 = px.line(
            plot_data_long,
            x='Year',
            y='Number of Crimes',
            color='Type of Crime',
            title='Annual Trend of Top 5 Crimes Against Women (2013-2022)',
            markers=True,
            hover_data={'Year': True, 'Number of Crimes': ':,', 'Type of Crime': True}
        )
        
        fig2.update_xaxes(dtick=1)
        fig2.update_yaxes(rangemode="tozero") 

        st.plotly_chart(fig2, use_container_width=True)


        # --- VIZ 3: Yearly Breakdown (Grouped Bar Chart) ---
        st.subheader('3. Yearly Breakdown of Top 5 Crime Types (Grouped View)')

        fig3 = px.bar(
            plot_data_long,
            x='Year',
            y='Number of Crimes',
            color='Type of Crime',
            barmode='group',
            title='Trend of Top 5 Crimes Against Women Over Time (2013-2022)',
            labels={'Number of Crimes': 'Total Number of Crimes'},
            height=600
        )
        
        fig3.update_xaxes(type='category', dtick=1)
        st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')

# --- 4. INTERPRETATION CONCLUSION ---
if not caw_dataset.empty:
    st.markdown("---")
    st.markdown("""
    <div class='interpretation-box' style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; border-left: 6px solid #2196F3;'>
        <h4>Interpretation & Conclusion for Objective 2</h4>
        <p>The analysis clearly demonstrates the **dominance** of the Top 5 crime categories, which account for a significant portion of all cases reported. The initial horizontal bar chart (1) confirms that **Cruelty by Husband or his Relatives** is the most frequent crime by a wide margin.</p>
        <p>The **Line (2) and Grouped Bar Charts (3)** show that while most Top 5 categories have fluctuated, the largest drivers of the overall trend are the two most frequent categories. Identifying these primary volume drivers is crucial for allocating resources and developing targeted prevention strategies.</p>
    </div>
    """, unsafe_allow_html=True)
# ----------------------------------------------------
