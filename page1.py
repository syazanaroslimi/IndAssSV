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

# Load the dataset
caw_dataset = load_data(url)

st.title('Objective 1: ')

# --- 1. SUMMARY BOX PLACEMENT (Line 23) ---
st.markdown("""
<div style='padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;'>
    <h4>Summary: Decade-Long Overview</h4>
    <p>This page provides a high-level view of crimes against women in India from 2013 to 2022. We begin by analyzing the trend in total reported crimes and then visualize the annual distribution across all individual crime categories to identify where the bulk of the volume lies.</p>
</div>
""", unsafe_allow_html=True)
# ----------------------------------------------


# _____________________________________________________________________________________________________________________________
# 1st visualization: Total Crimes - Line Chart
if 'caw_dataset' in locals() and not caw_dataset.empty:
    try:
        st.subheader('1. Trend of Total Crimes against Women (2013-2022)')

        # --- Data Preparation ---
        column_name = caw_dataset.columns[caw_dataset.iloc[0] == 'Total Crimes against Women'][0]
        total_crimes_series = caw_dataset.iloc[1:][column_name].astype(int)

        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series.index),
            'Number of Crimes': total_crimes_series.values
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
        total_crimes_series = caw_dataset.iloc[1:][column_name].astype(int)

        plot_data = pd.DataFrame({
            'Year': pd.to_numeric(total_crimes_series.index),
            'Number of Crimes': total_crimes_series.values
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

# --- 2. INTERPRETATION BOX PLACEMENT (Line 183) ---
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
