#__________________________________________________________________________________________________________________________________________________________________________________________
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




