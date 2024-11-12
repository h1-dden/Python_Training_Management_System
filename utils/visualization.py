import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from database.db_operations import fetch_data_from_mysql

# Generate and display visualizations
def show_visualizations():
    # Employee Skills Distribution
    st.subheader("Employee Skills Distribution")
    skills_df = fetch_data_from_mysql("Employee_Skills").merge(fetch_data_from_mysql("Skills"), on="Skill_ID")
    skill_counts = skills_df["Skill_Name"].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=skill_counts.index, y=skill_counts.values)
    plt.xlabel("Skills")
    plt.ylabel("Number of Employees with Skill")
    plt.title("Distribution of Skills Among Employees")
    st.pyplot(plt)

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
    plt.pie(deployment_status_counts, labels=deployment_status_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Employee Deployment Status Distribution")
    st.pyplot(plt)
