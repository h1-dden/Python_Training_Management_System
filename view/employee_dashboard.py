import streamlit as st
from database import db_operations
from view import visualization

def display_employee_data(connection):
# Display Employee Table with Filters
        st.subheader("Employee Data with Filters")

        # Fetch data from the database for employees
        employee_df = db_operations.fetch_employee_data(connection)  # Assumes this function is defined to fetch all employee data
        training_schedule_df = db_operations.fetch_training_schedule_data(connection)

        # Set up the layout with two columns: filters on the left, table on the right
        col1, col2 = st.columns([1, 3])  # Make the filter column narrower than the table column

        with col1:
            st.markdown("### Filters")
            # Add filters for various columns
            grade_filter = st.multiselect("Grade", options=employee_df['Grade'].unique(), default=employee_df['Grade'].unique())
            comm_level_filter = st.multiselect("Communication Level", options=employee_df['Communication_Level'].unique(), default=employee_df['Communication_Level'].unique())
            deployment_filter = st.multiselect("Deployment Status", options=employee_df['Deployment_Status'].unique(), default=employee_df['Deployment_Status'].unique())
            bench_status_filter = st.selectbox("Bench Status", options=['All'] + list(employee_df['Bench_Status'].unique()))
            experience_min = st.slider("Minimum Experience (Years)", min_value=int(employee_df['Experience'].min()), max_value=int(employee_df['Experience'].max()), value=int(employee_df['Experience'].min()))
            experience_max = st.slider("Maximum Experience (Years)", min_value=int(employee_df['Experience'].min()), max_value=int(employee_df['Experience'].max()), value=int(employee_df['Experience'].max()))
            stack_filter = st.multiselect("Stack", options=employee_df['Stack'].unique(), default=employee_df['Stack'].unique())

            # Apply filters to the DataFrame
            filtered_employee_df = employee_df[
                (employee_df['Grade'].isin(grade_filter)) &
                (employee_df['Communication_Level'].isin(comm_level_filter)) &
                (employee_df['Deployment_Status'].isin(deployment_filter)) &
                ((employee_df['Bench_Status'] == bench_status_filter) if bench_status_filter != 'All' else True) &
                (employee_df['Experience'] >= experience_min) &
                (employee_df['Experience'] <= experience_max) &
                (employee_df['Stack'].isin(stack_filter))
            ]

            # Download button for filtered data
            st.download_button(
                label="Download Filtered Employee Data",
                data=filtered_employee_df.to_csv(index=False).encode('utf-8'),
                file_name="filtered_employee_data.csv",
                mime="text/csv"
            )

        # Display filtered table in the second column
        with col2:
            st.dataframe(filtered_employee_df, use_container_width=True)
            # Filtered Data Visualization
            st.subheader("Filtered Employee Data Visualization")
            visualization.visualize_filtered_employee_data(filtered_employee_df)