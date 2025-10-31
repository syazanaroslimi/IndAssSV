import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt # The pyplot module
import seaborn as sns

# --- Data Loading Function (Crucial for correct Year axis) ---

st.title('Objective 3: ')

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
# --- Data Preparation and Plotting ---

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

        # 3. Create the Matplotlib figure object using plt.figure()
        # This is a pyplot function that creates the Figure (the canvas)
        plt.figure(figsize=(14, 12)) 
        
        # 4. Plot the Seaborn Heatmap. When ax is not specified, 
        # Seaborn plots to the *current* active figure/axes (pyplot's state).
        sns.heatmap(
            correlation_matrix, 
            annot=True, 
            cmap='coolwarm', 
            fmt=".2f"
        )
        
        # 5. Set titles and rotation using pyplot commands (plt. commands)
        plt.title('Correlation Heatmap of Crimes Against Women (2013-2022)')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        # 6. Retrieve the current active figure object and pass it to Streamlit
        # plt.gcf() gets the *current* pyplot Figure object that Seaborn just drew on.
        current_fig = plt.gcf() 
        st.pyplot(current_fig)
        
        # Crucial step: Clear the current figure's state to prevent overlap with future plots
        plt.close(current_fig) 

    except Exception as e:
        st.error(f"An unexpected error occurred during plotting: {e}")
        
else:
    st.warning('The dataset is not loaded or is empty.')
