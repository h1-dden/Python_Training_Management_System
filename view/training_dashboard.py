
import streamlit as st
from database import db_operations
from view import visualization

def display_training_data(connection):
    # Display Training Table with Filters
        st.subheader("Training Data with Filters")

        # Fetch data from the database for training
        training_df = db_operations.fetch_training_data(connection)  # Assumes this function is defined to fetch all training data
        # Set up the layout with two columns: filters on the left, table on the right
        col1, col2 = st.columns([1, 3])  # Make the filter column narrower than the table column

        with col1:
            st.markdown("### Filters")
            # Add filters for various columns
            team_filter = st.multiselect("Team ID", options=training_df['Team_ID'].unique(), default=training_df['Team_ID'].unique())
            min_score = st.slider("Minimum Test Score", min_value=int(training_df['Test_Score'].min()), max_value=int(training_df['Test_Score'].max()), value=int(training_df['Test_Score'].min()))
            max_score = st.slider("Maximum Test Score", min_value=int(training_df['Test_Score'].min()), max_value=int(training_df['Test_Score'].max()), value=int(training_df['Test_Score'].max()))
            rating_filter = st.multiselect("Overall Rating", options=training_df['Overall_Rating'].unique(), default=training_df['Overall_Rating'].unique())

            # Apply filters to the DataFrame
            filtered_training_df = training_df[
                (training_df['Team_ID'].isin(team_filter)) &
                (training_df['Test_Score'] >= min_score) &
                (training_df['Test_Score'] <= max_score) &
                (training_df['Overall_Rating'].isin(rating_filter))
            ]

            # Download button for filtered data
            st.download_button(
                label="Download Filtered Training Data",
                data=filtered_training_df.to_csv(index=False).encode('utf-8'),
                file_name="filtered_training_data.csv",
                mime="text/csv"
            )

        # Display filtered table in the second column
        with col2:
            st.dataframe(filtered_training_df, use_container_width=True)

            # Filtered Data Visualization
            visualization.visualize_filtered_training_data(filtered_training_df)