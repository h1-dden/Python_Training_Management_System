'''
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from database.db_operations import fetch_data_from_mysql

# Generate and display visualizations
def show_visualizations():
    # Employee Skills Distribution
    '''
    st.subheader("Employee Skills Distribution")
    skills_df = fetch_data_from_mysql("employee_skills").merge(fetch_data_from_mysql("skills"), on="Skill_ID")
    skill_counts = skills_df["Skill_Name"].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=skill_counts.index, y=skill_counts.values)
    plt.xlabel("Skills")
    plt.ylabel("Number of Employees with Skill")
    plt.title("Distribution of Skills Among Employees")
    st.pyplot(plt)
    '''

    # Training Scores
    st.subheader("Training Scores in Python Training")
    training_df = fetch_data_from_mysql("Python_Training")
    avg_scores = training_df[["Test_Score", "Presentation", "Project", "Assignment"]].mean()
    avg_scores.plot(kind='bar', figsize=(8, 5), color=["#1f77b4", "#ff7f0e", "#2ca02c", "#0000ff"])
    plt.xlabel("Training Components")
    plt.ylabel("Average Score")
    plt.title("Average Scores in Python Training")
    st.pyplot(plt)

    # Employee Deployment Status
    st.subheader("Employee Deployment Status")
    employees_df = fetch_data_from_mysql("Employees")
    deployment_status_counts = employees_df["Deployment_Status"].value_counts()
    plt.figure(figsize=(6, 6))
    '''



import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymysql
import streamlit as st

# MySQL connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "python_training_management_database"

def create_connection():
    """Establish a MySQL database connection."""
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def fetch_data(query):
    """Fetch data from MySQL and return as DataFrame."""
    connection = create_connection()
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Visualization Functions
def deployment_status_pie_chart():
    """Create a pie chart of employee deployment status."""
    query = "SELECT Deployment_Status, COUNT(*) as Count FROM Employees GROUP BY Deployment_Status"
    df = fetch_data(query)
    fig = px.pie(df, values='Count', names='Deployment_Status', title="Employee Deployment Status Distribution",
                 color_discrete_sequence=px.colors.sequential.Sunset)
    fig.update_traces(textinfo='percent+label', pull=[0.1] * len(df))
    fig.update_layout(title_font_size=20, showlegend=True)
    return fig

def training_team_size_bar_chart():
    """Create a bar chart of the number of employees in each training team."""
    query = "SELECT Team_ID, COUNT(Emp_ID) as Team_Size FROM Python_Training GROUP BY Team_ID"
    df = fetch_data(query)
    fig = px.bar(df, x='Team_ID', y='Team_Size', title="Training Team Size",
                 color='Team_ID', text='Team_Size', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='outside')
    fig.update_layout(title_font_size=20, xaxis_title="Team ID", yaxis_title="Number of Employees",
                      height=400, width=550, template='plotly_dark')
    return fig

def skill_distribution_treemap():
    """Create a treemap showing skill distribution among employees."""
    query = """
    SELECT s.Skill_Name, COUNT(es.Emp_ID) as Count
    FROM Skills s
    JOIN Employee_Skills es ON s.Skill_ID = es.Skill_ID
    GROUP BY s.Skill_Name
    """
    df = fetch_data(query)
    fig = px.treemap(df, path=[px.Constant("Skills"), 'Skill_Name'], values='Count',
                     title="Skill Distribution Among Employees",
                     color='Count', color_continuous_scale=px.colors.sequential.Aggrnyl)
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=0), title_font_size=20, height=400, width=550)
    return fig

def average_test_scores_bar_chart():
    """Create a bar chart of average test scores by team in Python training."""
    query = "SELECT Team_ID, AVG(Test_Score) as Avg_Test_Score FROM Python_Training GROUP BY Team_ID"
    df = fetch_data(query)
    fig = px.bar(df, x='Team_ID', y='Avg_Test_Score', title="Average Test Scores by Team",
                 color='Team_ID', text='Avg_Test_Score', color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_traces(textposition='outside')
    fig.update_layout(title_font_size=20, xaxis_title="Team ID", yaxis_title="Average Test Score",
                      height=400, width=550, template='plotly')
    return fig

def training_duration_line_chart():
    """Create a line chart for training duration over time."""
    query = "SELECT Team_id, start_date, Duration FROM Training_Schedule"
    df = fetch_data(query)
    fig = px.line(df, x='start_date', y='Duration', color='Team_id', title="Training Duration Over Time",
                  markers=True, color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(title_font_size=20, xaxis_title="Start Date", yaxis_title="Duration (Days)",
                      height=400, width=550, template='plotly_white')
    return fig

def show_visualizations():
    """Display the visualizations in a structured layout."""
    st.subheader("Employee and Training Insights")

    # Display each chart in a structured layout with three columns in the first row and two in the second
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(deployment_status_pie_chart(), use_container_width=True)
    with col2:
        st.plotly_chart(training_team_size_bar_chart(), use_container_width=True)
    with col3:
        st.plotly_chart(skill_distribution_treemap(), use_container_width=True)

    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(average_test_scores_bar_chart(), use_container_width=True)
    with col5:
        st.plotly_chart(training_duration_line_chart(), use_container_width=True)

    plt.pie(deployment_status_counts, labels=deployment_status_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Employee Deployment Status Distribution")
    st.pyplot(plt)
