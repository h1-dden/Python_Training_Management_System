import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import pymysql

# MySQL connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "python_training_management_database"

def create_connection():
    """Establish a MySQL database connection."""
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def show_general_visualizations():
    """Display general employee and training statistics."""
    st.subheader("General Employee and Training Statistics")

    # General Employee Data Visualization
    st.markdown("### Employee Statistics Overview")
    query_emp_count = "SELECT COUNT(*) as Total_Employees FROM Employees"
    query_deployment_status = "SELECT Deployment_Status, COUNT(*) as Count FROM Employees GROUP BY Deployment_Status"
    query_grade_distribution = "SELECT Grade, COUNT(*) as Count FROM Employees GROUP BY Grade"
    
    emp_count_df = fetch_data(query_emp_count)
    deployment_status_df = fetch_data(query_deployment_status)
    grade_distribution_df = fetch_data(query_grade_distribution)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Employees", emp_count_df['Total_Employees'].iloc[0])
        fig1 = px.pie(deployment_status_df, values='Count', names='Deployment_Status', title="Deployment Status Distribution")
        fig1.update_traces(textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(grade_distribution_df, x='Grade', y='Count', title="Grade Distribution", color='Grade')
        fig2.update_layout(xaxis_title="Grade", yaxis_title="Number of Employees", template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)

    # General Training Data Visualization
    st.markdown("### Training Statistics Overview")
    query_team_distribution = "SELECT Team_ID, COUNT(*) as Team_Size FROM Python_Training GROUP BY Team_ID"
    query_average_scores = "SELECT Team_ID, AVG(Test_Score) as Avg_Test_Score FROM Python_Training GROUP BY Team_ID"
    
    team_distribution_df = fetch_data(query_team_distribution)
    average_scores_df = fetch_data(query_average_scores)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.bar(team_distribution_df, x='Team_ID', y='Team_Size', title="Training Team Size", color='Team_ID')
        fig3.update_layout(xaxis_title="Team ID", yaxis_title="Number of Employees", template='plotly_white')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.scatter(average_scores_df, x='Team_ID', y='Avg_Test_Score', title="Average Test Scores by Team", color='Team_ID')
        fig4.update_layout(xaxis_title="Team ID", yaxis_title="Average Test Score", template='plotly_dark')
        st.plotly_chart(fig4, use_container_width=True)

def visualize_filtered_employee_data(employee_df):
    """Display visualizations based on filtered employee data."""
    st.subheader("Filtered Employee Data Visualizations")

    # Deployment Status by Grade
    fig1 = px.histogram(employee_df, x='Grade', color='Deployment_Status', barmode='group',
                        title="Grade Distribution by Deployment Status",
                        color_discrete_sequence=px.colors.qualitative.Prism)
    fig1.update_layout(xaxis_title="Grade", yaxis_title="Number of Employees", template='plotly')
    st.plotly_chart(fig1, use_container_width=True)

    # Communication Level Distribution
    fig2 = px.pie(employee_df, names='Communication_Level', title="Communication Level Distribution",
                  color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

    # Deployment Status by Grade (stacked bar)
    fig3 = px.bar(employee_df, x='Grade', y='Emp_ID', color='Deployment_Status', title="Deployment Status by Grade",
                  color_discrete_sequence=px.colors.sequential.Sunset, barmode='stack')
    fig3.update_layout(xaxis_title="Grade", yaxis_title="Employee Count", template='plotly_dark')
    st.plotly_chart(fig3, use_container_width=True)

def visualize_filtered_training_data(training_df):
    """Display visualizations based on filtered training data."""
    st.subheader("Filtered Training Data Visualizations")

    # Test Score by Team (Scatter)
    fig1 = px.scatter(training_df, x='Team_ID', y='Test_Score', color='Overall_Rating',
                      title="Test Scores by Team", size='Test_Score', hover_data=['Test_Score'],
                      color_continuous_scale=px.colors.sequential.Viridis)
    fig1.update_layout(xaxis_title="Team ID", yaxis_title="Test Score", template='plotly')
    st.plotly_chart(fig1, use_container_width=True)

    # Average Test Scores by Team
    avg_scores = training_df.groupby('Team_ID')['Test_Score'].mean().reset_index()
    fig2 = px.bar(avg_scores, x='Team_ID', y='Test_Score', title="Average Test Scores by Team",
                  color='Team_ID', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(xaxis_title="Team ID", yaxis_title="Average Test Score", template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

    # Rating Distribution
    fig3 = px.histogram(training_df, x='Overall_Rating', title="Rating Distribution",
                        color_discrete_sequence=px.colors.sequential.Teal)
    fig3.update_layout(xaxis_title="Overall Rating", yaxis_title="Count", template='plotly_dark')
    st.plotly_chart(fig3, use_container_width=True)

def fetch_data(query):
    """Helper function to fetch data from MySQL database."""
    connection = create_connection()  
    df = pd.read_sql(query, connection)
    connection.close()
    return df
