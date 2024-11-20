import plotly.express as px
import streamlit as st
from database import retrieve_data

def show_general_visualizations():

    """Display general employee and training statistics."""

    # General Employee Data Visualization
    st.markdown("### Employee Statistics Overview")
    query_grade_count = "SELECT Grade FROM Employees GROUP BY Grade"
    query_emp_count = "SELECT COUNT(*) as Total_Employees FROM Employees"
    query_employment_status = (
        "SELECT Employment_Status, COUNT(*) as Count "
        "FROM Employees GROUP BY Employment_Status"
    )
    query_grade_distribution = (
        "SELECT Grade, Bench_Status, COUNT(*) as Count "
        "FROM Employees GROUP BY Grade, Bench_Status"
    )
    query_bench_status = (
        "SELECT Bench_Status, COUNT(*) as Count "
        "FROM Employees GROUP BY Bench_Status"
    )
    stack_count = (
        "SELECT Stack, Grade, COUNT(*) as Count "
        "FROM Employees GROUP BY Stack, Grade"
    )

    grade_count_df = retrieve_data.fetch_data(query_grade_count)
    emp_count_df = retrieve_data.fetch_data(query_emp_count)
    employment_status_df = retrieve_data.fetch_data(query_employment_status)
    grade_distribution_df = retrieve_data.fetch_data(query_grade_distribution)
    bench_status_df = retrieve_data.fetch_data(query_bench_status)
    stack_count_df = retrieve_data.fetch_data(stack_count)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Employees", emp_count_df['Total_Employees'].iloc[0])

        fig1 = px.pie(
            employment_status_df, 
            values='Count', 
            names='Employment_Status', 
            title="Employee Status Distribution",
            hole=0.45
        )
        fig1.update_layout(legend=dict(x=0, y=0.5))
        fig1.update_traces(textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(
            stack_count_df,
            x='Grade',
            y='Count',
            title="Stack Count",
            color='Stack',
            color_discrete_sequence=px.colors.qualitative.Pastel1,
            text_auto=True
        )
        fig2.update_layout(
            xaxis_title="Grade", 
            yaxis_title="Employee Count", 
            template='plotly_dark'
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.metric("Total Grades", grade_count_df['Grade'].count())

        fig3 = px.histogram(
            grade_distribution_df,
            x='Grade',
            y='Count',
            title="Grade Distribution",
            color='Bench_Status',
            barmode='group',
            color_discrete_sequence=["red","yellowgreen"],
            text_auto=True
        )
        fig3.update_layout(
            xaxis_title="Grade", 
            yaxis_title="Employee Count", 
            template='plotly_dark'
        )
        st.plotly_chart(fig3, use_container_width=True)


def general_training_visualisation():
    """General Training Data Visualization."""
    
    st.markdown(" ")
    st.markdown("### Training Statistics Overview")

    query_trainee_count = "SELECT COUNT(*) as Total_Trainees FROM python_training"
    query_team_distribution = (
        "SELECT Team_ID, COUNT(*) as Team_Size FROM Python_Training GROUP BY Team_ID"
    )
    query_average_scores = (
        "SELECT Team_ID, ROUND(AVG(Test_Score), 0) as Avg_Test_Score,"
        "COUNT(*) as Team_Size FROM Python_Training GROUP BY Team_ID"
    )
    query_average_duration = (
        "SELECT Team_ID, AVG(Duration) as Avg_Duration, Status FROM training_schedule "
        "GROUP BY Team_ID"
    )
    query_training_teams = "SELECT COUNT(*) as Total_Trainings FROM training_schedule"
    query_topics_covered = (
        "SELECT Topics_covered, COUNT(*) as Count FROM training_schedule GROUP BY Topics_covered"
    )

    trainee_count_df = retrieve_data.fetch_data(query_trainee_count)
    team_distribution_df = retrieve_data.fetch_data(query_team_distribution)
    average_scores_df = retrieve_data.fetch_data(query_average_scores)
    average_duration_df = retrieve_data.fetch_data(query_average_duration)
    training_teams_df = retrieve_data.fetch_data(query_training_teams)
    topics_covered_df = retrieve_data.fetch_data(query_topics_covered)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Total Trainees", trainee_count_df['Total_Trainees'].iloc[0])

        fig4 = px.bar(
            average_scores_df,
            x='Team_ID',
            y='Avg_Test_Score',
            title="Average Test Scores",
            text_auto=True,
            color_discrete_sequence=["lightsteelblue"],
            hover_data=["Team_Size"]
        )
        fig4.update_layout(
            xaxis_title="Team ID",
            yaxis_title="Average Test Score",
            template='plotly_dark'
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.metric("Total Teams", training_teams_df['Total_Trainings'].iloc[0])

        fig5 = px.histogram(
            average_duration_df,
            x='Avg_Duration',
            y='Team_ID',
            title="Training Status",
            color='Status',
            color_discrete_sequence=px.colors.qualitative.Pastel2
        )
        fig5.update_layout(
            xaxis_title="Team ID",
            yaxis_title="Average Training Duration",
            template='plotly_dark'
        )
        st.plotly_chart(fig5, use_container_width=True)


