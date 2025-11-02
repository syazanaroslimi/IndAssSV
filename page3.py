import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Define the URL for the dataset
url = 'https://raw.githubusercontent.com/syazanaroslimi/IndAssSV/refs/heads/main/crime_against_women_2013_2022.csv'

# data preparation
@st.cache_data
def load_data(data_url):
    """Loads the dataset and sets the years as the index."""
    try:
        data = pd.read_csv(data_url, index_col=0) 
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data
def prepare_data(caw_dataset):
    """Cleans and prepares the data for visualization and metrics (removing total column)."""
    if caw_dataset.empty: return pd.DataFrame()
    caw_data_numeric = caw_dataset.iloc[1:].copy()
    caw_data_numeric.columns = caw_dataset.iloc[0]
    
    try:
        # Use .astype('Int64') for numeric indexing
        caw_data_numeric.index = pd.to_numeric(caw_data_numeric.index, errors='coerce').astype('Int64')
    except Exception as e:
        st.error(f"Error converting index to numeric: {e}")
        return pd.DataFrame()

    caw_data_numeric = caw_data_numeric.drop(
        columns=['Total Crimes against Women'], 
        errors='ignore'
    )
    return caw_data_numeric.astype(float)

@st.cache_data
def prepare_page3_metrics(data_df):
    """Calculates key metrics for the summary boxes based on 2013 vs 2022 changes and correlations."""
    
    # Largest Absolute Change (2013 vs 2022)
    change = data_df.loc[2022] - data_df.loc[2013]
    largest_abs_change_crime = change.abs().idxmax()
    actual_change = change[largest_abs_change_crime]

    # Correlation Metrics
    corr_matrix = data_df.corr()
    corr_pairs = corr_matrix.unstack()
    
    unique_pairs = corr_pairs[corr_pairs < 1].drop_duplicates().dropna()    # Filter for unique pairs and exclude self-correlation (A=B)

    # Strongest Positive Correlation
    strongest_pos_corr_val = unique_pairs.max()
    (crime_a_pos, crime_b_pos) = unique_pairs[unique_pairs == strongest_pos_corr_val].index[0]
    
    # Strongest Negative Correlation
    strongest_neg_corr_val = unique_pairs.min()
    (crime_a_neg, crime_b_neg) = unique_pairs[unique_pairs == strongest_neg_corr_val].index[0]
    
    # Compound Annual Growth Rate (CAGR) for Rape Cases
    rape_start = data_df.loc[2013, 'Rape']
    rape_end = data_df.loc[2022, 'Rape']
    # Calculate CAGR using the formula: ((Ending Value / Starting Value) ^ (1 / Years)) - 1
    cagr_rape = ((rape_end / rape_start) ** (1/9)) - 1 if rape_start != 0 else np.nan

    return {
        'largest_abs_change_crime': largest_abs_change_crime,
        'actual_change': actual_change,
        'strongest_pos_corr_val': strongest_pos_corr_val,
        'strongest_pos_corr_crimes': f"{crime_a_pos} & {crime_b_pos}",
        'strongest_neg_corr_val': strongest_neg_corr_val,
        'strongest_neg_corr_crimes': f"{crime_a_neg} & {crime_b_neg}",
        'cagr_rape': cagr_rape
    }

caw_dataset = load_data(url)
caw_data_numeric = prepare_data(caw_dataset)

st.title('Objective 3: To assess the comparison of crime rates between 2013 and 2022, the trends of rape cases in 10 years and the relationship between each type of crime against women')

# Calculate Metrics for Summary Boxes
metrics = None
if not caw_data_numeric.empty:
    try:
        metrics = prepare_page3_metrics(caw_data_numeric)
    except Exception as e:
        st.error(f"Error calculating metrics for summary: {e}")

# summary box
if metrics:
    col1, col2, col3, col4 = st.columns(4)
    
    # M1: Largest Absolute Change
    col1.metric(
        label="Largest Change (2013 vs 2022)", 
        value=metrics['largest_abs_change_crime'], 
        delta=f"{metrics['actual_change']:+,.0f} Cases",
        # Use inverse color since crime increase is negative news
        delta_color="inverse", 
        help="The crime category that saw the largest absolute case number difference between 2013 and 2022."
    )
    # M2: Strongest Positive Correlation
    col2.metric(
        label="Strongest Positive Correlation", 
        value=f"{metrics['strongest_pos_corr_val']:.2f}",
        help=f"Highest correlation pair: {metrics['strongest_pos_corr_crimes']}." #Indicates strong co-movement over time."
    )
    # M3: Strongest Negative Correlation
    col3.metric(
        label="Strongest Negative Correlation", 
        value=f"{metrics['strongest_neg_corr_val']:.2f}",
        help=f"Lowest correlation pair: {metrics['strongest_neg_corr_crimes']}." #Suggests one crime decreases when the other increases."
    )
    # M4: Annual Growth Rate (Rape) 
    cagr_value = f"{metrics['cagr_rape'] * 100:.2f}%" if not np.isnan(metrics['cagr_rape']) else "N/A"
    col4.metric(
        label="Annual Growth Rate (Rape)", 
        value=cagr_value,
        # Delta shows whether it's growing (green/positive) or shrinking (red/negative)
        delta=f"Total Change: {metrics['actual_change']:+,.0f}",
        delta_color="inverse", #if metrics['cagr_rape'] > 0 else "normal", 
        help="Compound Annual Growth Rate of 'Rape' cases from 2013 to 2022."
    )

st.markdown("---")
# ----------------------------------------------------
# Visualisation
if not caw_data_numeric.empty:
    # 1st visualisation
    try:
        #st.subheader('1. Crime Count Comparison by Type: 2013 vs 2022')
        # Use numeric index for .loc, then convert back to string for plotting if needed
        crimes_2013 = caw_data_numeric.loc[2013]
        crimes_2022 = caw_data_numeric.loc[2022]

        comparison_df = pd.DataFrame({'2013': crimes_2013, '2022': crimes_2022})
        comparison_df.index.name = 'Type of Crime' 

        plot_data = comparison_df.reset_index().melt(
            id_vars='Type of Crime', 
            var_name='Year', 
            value_name='Number of Crimes'
        )

        fig1 = px.bar(
            plot_data,
            x='Type of Crime',
            y='Number of Crimes',
            color='Year',
            barmode='group',
            title='1. Crime Comparison: 2013 vs 2022',
            labels={'Type of Crime': 'Crime Category', 'Number of Crimes': 'Total Number of Crimes'},
            height=650
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)

    except KeyError as e:
        st.error(f"Data Error: One or more expected labels ('2013', '2022', or 'Type of Crime') were not found. Error detail: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during VIZ 1 plotting: {e}")

    # 2nd visualisation
    try:
        #st.subheader('2. Annual Trend for "Rape" Cases (Zoomed View)')
        rape_trend = caw_data_numeric['Rape']

        plot_data_rape = pd.DataFrame({
            # Convert index (Year) back to string for axis labeling if desired, but index is already correct
            'Year': rape_trend.index.astype(str), 
            'Number of Cases': rape_trend.values
        })

        fig2 = px.line(
            plot_data_rape,
            x='Year',
            y='Number of Cases',
            title='2. Trend of Rape Cases from 2013 to 2022',
            markers=True,
            height=500
        )
        
        # Customizing the Y-axis range and ticks for the 'zoom' effect
        fig2.update_yaxes(
            range=[27000, 40000], 
            dtick=2000,
            tickformat=","
        )
        fig2.update_xaxes(dtick=1) 

        st.plotly_chart(fig2, use_container_width=True)

    except KeyError:
        st.error("Error: Could not find the column 'Rape'. Check the crime category names.")
    except Exception as e:
        st.error(f"An unexpected error occurred during VIZ 2 plotting: {e}")

    # 3rd visualisation
    try:
        #st.subheader('3. Inter-Category Correlation of Crime Rates')
        correlation_matrix = caw_data_numeric.corr()
        
        fig3 = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale=px.colors.diverging.RdBu,
            zmin=-1,
            zmax=1,
            labels=dict(x="Crime Category", y="Crime Category", color="Correlation"),
            title='3. Relationship of Each Crimes Against Women from 2013 to 2022',
            height=700 
        )
        
        fig3.update_traces(hovertemplate="Crime A: %{y}<br>Crime B: %{x}<br>Correlation: %{z}<extra></extra>")
        fig3.update_xaxes(side="bottom", tickangle=45)
        fig3.update_yaxes(automargin=True) 
        
        st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"An unexpected error occurred during VIZ 3 plotting: {e}")

    st.markdown("---")

    # interpretation
    st.markdown("""
    <div style='padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;'>
    <h4>Interpretation</h4>
    <p>The graph show a significant increase in the number of cases in 2022 compared to 2013, with rape cases showing a fluctuating pattern over the period.
    Correlations between crimes shows that one type of crimes against women can influence other crimes as well.</p>
</div>
    """, unsafe_allow_html=True)

else:
    st.error('Data preparation failed. Cannot display page contents.')
