import plotly.express as px
import streamlit as st
import pandas as pd

def visualize_filtered_training_data(filtered_training_df):

    """Dynamically display visualizations based on filtered training data."""
    
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader("Training Progress Report")

    if filtered_training_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Training Progress by Teams (Line Chart)
    # avg_progress_df = filtered_training_df
    # avg_progress_df['Empcount'] = filtered_training_df.groupby('Team_ID')['Emp_ID'].count()
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
        legend_title="Employee_ID",
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

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
        legend_title="Criteria",
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

    communication_df = filtered_training_df.groupby('Overall_Feedback')['Emp_ID'].count().reset_index().rename(columns={'Emp_ID':'Count'})
    # 3. Average Test Scores by Team (Bar Chart)
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
    fig3.update_layout(legend=dict(x=0, y=0.5))
    st.plotly_chart(fig3, use_container_width=True)
