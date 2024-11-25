import pandas as pd
import streamlit as st
import plotly.express as px

def visualize_filtered_training_data(filtered_training_df,filtered_test_scores):

    """Dynamically display visualizations based on filtered training data."""
    
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader("Training Progress Report")

    if filtered_training_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Training Progress by Teams (Line Chart)
    fig1 = px.histogram(
        filtered_training_df,
        x='Team_ID',
        y='Overall_Rating',
        title="Employee Ratings",
        barmode="group",
        hover_data=["Emp_ID"],
        color='Emp_ID',
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    fig1.update_layout(
        xaxis_title="Team_ID",
        yaxis_title="Rating",
        legend_title="Employee_ID"
    )
    st.plotly_chart(fig1, use_container_width=True)
    fig1.write_image(r"static\visualizations\employee_ratings.png")

    #2. Average of all scores
    avg_progress_df = filtered_training_df.groupby('Team_ID')[['Test_Score','Presentation','Project','Assignment']].mean().reset_index()
    fig2 = px.histogram(
        avg_progress_df,
        x='Team_ID',
        y=['Test_Score','Presentation','Project','Assignment'],
        title="Test Scores by Team",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(
        xaxis_title="Team_ID",
        yaxis_title="Average_Scores",
        legend_title="Criteria"
    )
    st.plotly_chart(fig2, use_container_width=True)
    fig2.write_image(r"static\visualizations\avg_scores.png")

    # 3. Average Test Scores by Team (Bar Chart)
    communication_df = filtered_training_df.groupby('Overall_Feedback')['Emp_ID'].count().reset_index().rename(columns={'Emp_ID':'Count'})
    fig3 = px.pie(
        communication_df,
        values='Count',
        names='Overall_Feedback',
        title="Feedback of trainees",
        color_discrete_sequence = px.colors.qualitative.Pastel1,
        hole=0
    )
    fig3.update_traces(textinfo='percent+label',
                           marker=dict(line=dict(color='#FFFFFF', width=5))
                           )  # Add white border
    st.plotly_chart(fig3, use_container_width=True)
    fig3.write_image(r"static\visualizations\feedback_of_trainees.png")

    #4. Test Scores Average by module
    module_df = filtered_test_scores.drop(columns=['Team_ID','Emp_Name','Email_ID','Avg_Score'])
    module_df = module_df.transpose()
    mean_scores = module_df.mean(axis=1).round().reset_index()
    mean_scores.columns = ['Test_Name', 'Average_Score']  # Rename columns for clarity
    merged_scores = module_df.merge(mean_scores, on='Test_Name', how='left')
    
    fig4 = px.bar(
        merged_scores,
        x='Test_Name',
        y='Average_Score',
        title="Average Test Scores by Module",
        color='Test_Name',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig4.update_layout(
        xaxis_title="Test Name",
        yaxis_title="Average Scores",
        legend_title="Test Name"
    )
    st.plotly_chart(fig4, use_container_width=True)
    fig4.write_image(r"static\visualizations\avg_test_scores_by_module.png")