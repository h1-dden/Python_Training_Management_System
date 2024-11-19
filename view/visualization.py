import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import pymysql
from services import database_connection

def show_general_visualizations():
    """Display general employee and training statistics."""

    # General Employee Data Visualization
    st.markdown("### Employee Statistics Overview")
    query_emp_count = "SELECT COUNT(*) as Total_Employees FROM Employees"
    query_deployment_status = "SELECT Deployment_Status, COUNT(*) as Count FROM Employees GROUP BY Deployment_Status"
    query_grade_distribution = "SELECT Grade, COUNT(*) as Count FROM Employees GROUP BY Grade"
    query_bench_status = "SELECT Bench_Status, COUNT(*) as Count FROM Employees GROUP BY Bench_Status"
    stack_count = "SELECT Stack, COUNT(*) as Count FROM Employees GROUP BY Stack"
    
    emp_count_df = fetch_data(query_emp_count)
    deployment_status_df = fetch_data(query_deployment_status)
    grade_distribution_df = fetch_data(query_grade_distribution)
    bench_status_df = fetch_data(query_bench_status)
    stack_count_df = fetch_data(stack_count)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Employees", emp_count_df['Total_Employees'].iloc[0])
        fig1 = px.pie(deployment_status_df, values='Count', names='Deployment_Status', title="Deployment Status Distribution")
        fig5 = px.pie(bench_status_df,values='Count', names='Bench_Status', title='Bench Status')
        fig1.update_traces(textinfo='percent+label')
        fig5.update_traces(textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        fig2 = px.bar(grade_distribution_df, x='Grade', y='Count', title="Grade Distribution", color='Grade')
        fig6 = px.bar(stack_count_df, x='Stack', y='Count', title="Stack Count", color='Stack')
        fig2.update_layout(xaxis_title="Grade", yaxis_title="Number of Employees", template='plotly_dark')
        fig6.update_layout(xaxis_title="Grade", yaxis_title="Bench Duration", template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig6, use_container_width=True)

def general_training_visualisation():

    # General Training Data Visualization
    st.markdown("### Training Statistics Overview")
    query_trainee_count = "SELECT COUNT(*) as Total_Trainees FROM python_training"
    query_team_distribution = "SELECT Team_ID, COUNT(*) as Team_Size FROM Python_Training GROUP BY Team_ID"
    query_average_scores = "SELECT Team_ID, AVG(Test_Score) as Avg_Test_Score FROM Python_Training GROUP BY Team_ID"
    query_average_duration = "SELECT Team_ID, AVG(Duration) as Avg_Duration FROM training_schedule GROUP BY Team_ID"
    query_training_teams = "SELECT COUNT(*) as Total_Trainings FROM training_schedule"
    query_topics_covered = "SELECT Topics_covered, COUNT(*) as Count FROM training_schedule GROUP BY Topics_covered"

    trainee_count_df = fetch_data(query_trainee_count)
    team_distribution_df = fetch_data(query_team_distribution)
    average_scores_df = fetch_data(query_average_scores)
    average_duration_df = fetch_data(query_average_duration)
    training_teams_df = fetch_data(query_training_teams)
    topics_covered_df = fetch_data(query_topics_covered)

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total Trainees", trainee_count_df['Total_Trainees'].iloc[0])
        fig3 = px.bar(team_distribution_df, x='Team_ID', y='Team_Size', title="Training Team Size", color='Team_ID')
        fig6 = px.pie(topics_covered_df, values='Count', names='Topics_covered', title='Topics Covered')
        fig3.update_layout(xaxis_title="Team ID", yaxis_title="Number of Employees", template='plotly_white')
        fig6.update_layout(xaxis_title="Team ID", yaxis_title="Topics Covered", template='plotly_dark')

        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig6, use_container_width=True)

    with col4:
        st.metric("Total Trainings", training_teams_df['Total_Trainings'].iloc[0])
        fig4 = px.scatter(average_scores_df, x='Team_ID', y='Avg_Test_Score', title="Average Test Scores by Team", color='Team_ID')
        fig5 = px.scatter(average_duration_df, x='Team_ID', y='Avg_Duration', title="Average Training Duration by Team", color='Team_ID')
        fig4.update_layout(xaxis_title="Team ID", yaxis_title="Average Test Score", template='plotly_dark')
        fig5.update_layout(xaxis_title="Team ID", yaxis_title="Average Training Duration", template = 'plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)
        st.plotly_chart(fig5, use_container_width=True)

def fetch_data(query):

    """Helper function to fetch data from MySQL database."""

    connection = database_connection.create_connection() 
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def visualize_filtered_employee_data(filtered_employee_df):
    
    """Dynamically display visualizations based on filtered employee data."""

    st.subheader("Dynamic Visualizations for Filtered Employee Data")

    if filtered_employee_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Deployment Status by Grade (Grouped Histogram)
    fig1 = px.histogram(
        filtered_employee_df, 
        x='Grade', 
        color='Deployment_Status', 
        title="Grade Distribution by Deployment Status",
        barmode='group', 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_layout(
        xaxis_title="Grade", 
        yaxis_title="Number of Employees", 
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Communication Level Distribution (Pie Chart)
    fig2 = px.pie(
        filtered_employee_df, 
        names='Communication_Level', 
        title="Communication Level Distribution",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Average Experience by Grade (Bar Chart)
    avg_experience_df = filtered_employee_df.groupby('Grade')['Experience'].mean().reset_index()
    fig3 = px.bar(
        avg_experience_df, 
        x='Grade', 
        y='Experience', 
        title="Average Experience by Grade",
        color='Grade', 
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig3.update_layout(
        xaxis_title="Grade", 
        yaxis_title="Average Experience (Years)", 
        template='plotly_white'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Bench Status by Grade (Stacked Bar Chart)
    fig4 = px.histogram(
        filtered_employee_df, 
        x='Grade', 
        color='Bench_Status', 
        title="Grade Distribution by Bench Status",
        barmode='group', 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig4.update_layout(
        xaxis_title="Grade", 
        yaxis_title="Number of Employees", 
        template='plotly_dark'
    )
    st.plotly_chart(fig4, use_container_width=True)

def visualize_filtered_training_data(filtered_training_df):
    """Dynamically display visualizations based on filtered training data."""
    st.subheader("Dynamic Visualizations for Filtered Training Data")

    if filtered_training_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Training Progress by Teams (Line Chart)
    avg_progress_df = filtered_training_df.groupby('Team_ID')['Assessment_Date'].mean().reset_index()
    fig1 = px.line(
        avg_progress_df, 
        x='Team_ID', 
        y='Assessment_Date', 
        title="Training Progress by Teams",
        markers=True,
        color='Team_ID', 
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig1.update_layout(
        xaxis_title="Team ID", 
        yaxis_title="Average Training Progress (%)", 
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Test Scores by Team (Box Plot)
    fig2 = px.box(
        filtered_training_df, 
        x='Team_ID', 
        y='Test_Score', 
        title="Test Scores by Team",
        color='Team_ID', 
        points="all", 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(
        xaxis_title="Team ID", 
        yaxis_title="Test Score", 
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Average Test Scores by Team (Bar Chart)
    avg_scores_df = filtered_training_df.groupby('Team_ID')['Test_Score'].mean().reset_index()
    fig3 = px.bar(
        avg_scores_df, 
        x='Team_ID', 
        y='Test_Score', 
        title="Average Test Scores by Team",
        color='Team_ID', 
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig3.update_layout(
        xaxis_title="Team ID", 
        yaxis_title="Average Test Score", 
        template='plotly_white'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Rating Distribution (Histogram)
    fig4 = px.histogram(
        filtered_training_df, 
        x='Overall_Rating', 
        title="Rating Distribution",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    fig4.update_layout(
        xaxis_title="Overall Rating", 
        yaxis_title="Count", 
        template='plotly_white'
    )
    st.plotly_chart(fig4, use_container_width=True)
