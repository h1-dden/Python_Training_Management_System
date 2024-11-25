
import streamlit as st
from database import db_operations
from view import training_plots, generate_tpr
from services import clean_data

def display_training_data():
    
    """ Display training data from the database"""

    st.markdown(" ")

    # Fetch data from the database
    training_df = db_operations.fetch_training_data()
    training_df.drop(columns=['Test_Name'],inplace=True)
    training_df = training_df.drop_duplicates(subset='Emp_ID')
    schedule_df = db_operations.fetch_training_schedule_data()
    test_dataframe = clean_data.create_test_scores_dataframe()
    
    # Set up layout with filters and table
    col1, col2 = st.columns([1, 3])
 
    with col1:
        st.markdown("### Filters")
        team_filter = st.multiselect("Team ID", 
                                     options=training_df['Team_ID'].unique(), 
                                     default=training_df['Team_ID'].unique()
                                     )
        
        min_score = st.slider("Minimum Test Score", 
                              min_value=int(training_df['Test_Score'].min()), 
                              max_value=int(training_df['Test_Score'].max()), 
                              value=int(training_df['Test_Score'].min())
                              )
        
        max_score = st.slider("Maximum Test Score", 
                              min_value=int(training_df['Test_Score'].min()), 
                              max_value=int(training_df['Test_Score'].max()), 
                              value=int(training_df['Test_Score'].max())
                              )
        
        rating_filter = st.multiselect("Overall Rating", 
                                       options=training_df['Overall_Rating'].unique(), 
                                       default=training_df['Overall_Rating'].unique()
                                       )
        
        feedback_filter = st.multiselect("Feedback", 
                                         options=training_df['Overall_Feedback'].unique(), 
                                         default=training_df['Overall_Feedback'].unique()
                                         )
        
        # Apply filter to training data
        filtered_training_df = training_df[
            (training_df['Team_ID'].isin(team_filter)) &
            (training_df['Test_Score'] >= min_score) &
            (training_df['Test_Score'] <= max_score) &
            (training_df['Overall_Rating'].isin(rating_filter)) &
            (training_df['Overall_Feedback'].isin(feedback_filter))
        ]
        # Apply filter to test scores
        filtered_testscore_df = test_dataframe[
            (test_dataframe['Team_ID'].isin(team_filter))
        ]
 
        # Download filtered data
        st.markdown(" ")
        st.markdown(" ")
        st.download_button(
            label="Download Filtered Training Data",
            data=filtered_training_df.to_csv(index=False).encode('utf-8'),
            file_name="filtered_training_data.csv",
            mime="text/csv"
        )

    with col2:
        st.markdown(" ")
        st.markdown("Trainee Performance Data")
        st.dataframe(filtered_training_df, use_container_width=True)

        st.subheader(" ")
        st.markdown("Test Scores of Trainees")
        st.dataframe(filtered_testscore_df,use_container_width=True)
        # Filtered Data Visualization
        training_plots.visualize_filtered_training_data(filtered_training_df,filtered_testscore_df)

    with col1:
        if st.session_state.role == 'admin':
            if st.download_button:
                # Team performance data
                team_performance_df = filtered_training_df.groupby('Team_ID')["Test_Score"].mean().reset_index()

                # Generate PDF report
                pdf_buffer = generate_tpr.generate_pdf_with_visualizations(schedule_df, 
                                                                           filtered_training_df, 
                                                                           filtered_testscore_df
                                                                           )

                # Provide download button for the PDF
                st.download_button(
                    label="Download TPR",
                    data=pdf_buffer,
                    file_name="Training_Progress_Report.pdf",
                    mime="application/pdf"
                )
