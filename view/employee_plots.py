
import plotly.express as px
import streamlit as st

def visualize_filtered_employee_data(filtered_employee_df):

    """Dynamically display visualizations based on filtered employee data."""

    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader("Employee Report")

    if filtered_employee_df.empty:
        st.warning("No data available after applying filters.")
        return

    # 1. Employee Communication by Grade (Grouped Histogram)
    fig1 = px.histogram(
        filtered_employee_df,
        x='Grade',
        color='Communication_Level',
        title="Gradewise Communication Level",
        barmode='group',
        color_discrete_sequence=px.colors.sequential.Sunsetdark,
        text_auto=True
    )
    fig1.update_layout(
        xaxis_title="Grade",
        yaxis_title="Employee Count",
        legend_title="Communication Level",
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Communication Level by bench Status
    communication_level_count_df = filtered_employee_df['Communication_Level'].value_counts().reset_index()
    communication_level_count_df.columns = ['Communication_Level', 'Count']
    fig2 = px.histogram(
        filtered_employee_df,
        x='Communication_Level',
        color='Bench_Status',
        title="Communication Level by Bench Status",
        barmode='group',
        color_discrete_sequence=["red","yellowgreen"],
        text_auto=True
    )
    
    fig2.update_layout(
        xaxis_title="Communication Level",
        yaxis_title="Employee Count",
        legend_title="Bench Status",
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Communication Level by Stack
    fig3 = px.histogram(
        filtered_employee_df,
        y='Stack',
        title="Communication Level by Stack",
        color='Communication_Level',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text_auto=True
    )
    fig3.update_layout(
            xaxis_title="Employee Count",
            yaxis_title="Stack", 
            template='plotly_dark'
        )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Average Bench duration with Stack
    avg_bench_duration_df = filtered_employee_df.groupby(['Grade','Stack'])['Bench_Duration'].mean().round().reset_index()
    fig4 = px.histogram(
        avg_bench_duration_df,
        x = 'Bench_Duration',
        y ='Grade',
        title="Average bench duration",
        color="Stack",
        color_discrete_sequence=px.colors.sequential.Sunset,
        text_auto=True
    )
    fig4.update_layout(
            xaxis_title="Bench Duration (days)",
            yaxis_title="Grade", 
            template='plotly_dark'
        )
    st.plotly_chart(fig4, use_container_width=True)
