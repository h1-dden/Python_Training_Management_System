import io
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Table, Spacer, 
                                TableStyle, Image, PageBreak, 
                                Paragraph
                            )

def generate_pdf_with_visualizations(schedule_df, training_data_df, test_score_df):

    """Generate a professional PDF with dynamic visualizations."""
    
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, 
                            pagesize=letter, 
                            rightMargin=72, 
                            leftMargin=72, 
                            topMargin=72, 
                            bottomMargin=72
                            )
    elements = []

    # Add logo
    logo = Image("static/images/yash_logo.png", width=1.5*inch, height=1.5*inch)
    elements.append(logo)
    elements.append(Spacer(1, 20))

    # Add a title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.textColor = colors.darkblue
    title = Paragraph("Training Progress Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Prepare Team Members Data Table
    training_data_df.drop(columns=['Assessment_Date','Email_ID'],inplace=True)  # Drop the 'Assessment Date' column if it exists
    elements.append(Paragraph("Team Members Data", styles['Heading2']))
    training_data = [training_data_df.columns.tolist()] + training_data_df.values.tolist()
    training_table = Table(training_data)
    training_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Light blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(training_table)
    elements.append(PageBreak())

    # Add Training Schedule Table
    elements.append(Paragraph("Training Schedule", styles['Heading2']))
    schedule_data = [schedule_df.columns.tolist()] + schedule_df.values.tolist()
    schedule_table = Table(schedule_data)
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(schedule_table)
    elements.append(PageBreak())

    #Prepare Test Score by Team
    #ISSUE IS HERE 
    employee_test_df = test_score_df[['Emp_Name','Team_ID','Avg_Score']]
    elements.append(Paragraph("Test Scores", styles['Heading2']))
    test_score_data = [employee_test_df.columns.tolist()] + employee_test_df.values.tolist()
    test_score_table = Table(test_score_data)
    test_score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(test_score_table)
    elements.append(PageBreak())

    # Add visualizations
    elements.append(Image(r"static\visualizations\employee_ratings.png", width=400, height=300))
    elements.append(Spacer(1, 20))

    elements.append(Image(r"static\visualizations\avg_scores.png", width=400, height=300))
    elements.append(Spacer(1, 40))

    elements.append(Image(r"static\visualizations\feedback_of_trainees.png", width=500, height=300))
    elements.append(Spacer(1, 40))

    elements.append(Image(r"static\visualizations\avg_test_scores_by_module.png", width=500, height=300))
    elements.append(Spacer(1, 40))

    # Build PDF
    pdf.build(elements)
    buffer.seek(0)
    return buffer