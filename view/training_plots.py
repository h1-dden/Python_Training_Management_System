
import plotly.express as px
import streamlit as st

def visualize_filtered_training_data(filtered_training_df):

    """Dynamically display visualizations based on filtered training data."""

    st.subheader("Traing Data Visualizations")

    if filtered_training_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Training Progress by Teams (Line Chart)
    avg_progress_df = filtered_training_df.groupby('Team_ID')['Assessment_Date'].mean().reset_index()
    fig1 = px.histogram(
        avg_progress_df,
        x='Team_ID',
        y='Assessment_Date',
        title="Training Progress by Teams",
        color='Team_ID',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Test Scores by Team (Box Plot)
    fig2 = px.histogram(
        filtered_training_df,
        x='Team_ID',
        y='Test_Score',
        title="Test Scores by Team",
        color='Team_ID',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Average Test Scores by Team (Bar Chart)
    avg_scores_df = filtered_training_df.groupby('Team_ID')['Test_Score'].mean().reset_index()
    fig3 = px.histogram(
        avg_scores_df,
        x='Team_ID',
        y='Test_Score',
        title="Average Test Scores by Team",
        color='Team_ID',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Rating Distribution (Histogram)
    fig4 = px.histogram(
        filtered_training_df,
        x='Overall_Rating',
        title="Rating Distribution",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig4, use_container_width=True)