"""
ReportLab module to generate PDF advisories.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def generate_advisory_pdf(data_dict: dict, file_path: str):
    """
    Generate a PDF report containing the prediction and advisory.
    data_dict contains: district, crop, season, yield_pred, district_avg, 
                        weather_temp, weather_rain,
                        top_factors (list of dicts), recommendations (list of strings)
    """
    doc = SimpleDocTemplate(file_path, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=18)
                            
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2D6A2A'),
        spaceAfter=16,
        alignment=1 # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1A1A2E'),
        spaceBefore=12,
        spaceAfter=6,
        borderPadding=4,
        backColor=colors.HexColor('#EBE4D1')
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.spaceAfter = 8
    
    bold_style = ParagraphStyle(
        'BoldNormal',
        parent=normal_style,
        fontName='Helvetica-Bold'
    )

    Story = []
    
    # 1. Header
    Story.append(Paragraph("Tamil Nadu Crop Yield Advisory", title_style))
    Story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                           ParagraphStyle('Date', parent=normal_style, alignment=1)))
    Story.append(Spacer(1, 0.5 * inch))
    
    # 2. Farm Summary
    Story.append(Paragraph("1. Farm Summary", heading_style))
    summary_data = [
        ["District", data_dict.get('district', 'N/A')],
        ["Crop", data_dict.get('crop', 'N/A')],
        ["Season", data_dict.get('season', 'N/A')]
    ]
    t_summary = Table(summary_data, colWidths=[2*inch, 4*inch])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7F3E9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    Story.append(t_summary)
    Story.append(Spacer(1, 0.2 * inch))
    
    # 3. Prediction
    Story.append(Paragraph("2. Yield Prediction", heading_style))
    pred_val = data_dict.get('yield_pred', 0)
    avg_val = data_dict.get('district_avg', 0)
    diff = pred_val - avg_val
    diff_text = f"+{diff:.2f}" if diff > 0 else f"{diff:.2f}"
    
    pred_data = [
        ["Predicted Yield", f"{pred_val:.2f} tonnes/hectare"],
        ["Historical District Average", f"{avg_val:.2f} tonnes/hectare"],
        ["Difference", f"{diff_text} tonnes/hectare"]
    ]
    t_pred = Table(pred_data, colWidths=[3*inch, 3*inch])
    t_pred.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2F0CB')), # Light green for prediction
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'), # Bold prediction val
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    Story.append(t_pred)
    Story.append(Spacer(1, 0.2 * inch))
    
    # 4. Current Weather
    Story.append(Paragraph("3. Current Weather Data (Live)", heading_style))
    weather_text = f"Current Temperature: <b>{data_dict.get('weather_temp', 'N/A')} °C</b><br/>"
    weather_text += f"Estimated Daily Rainfall: <b>{data_dict.get('weather_rain', 'N/A')} mm</b>"
    Story.append(Paragraph(weather_text, normal_style))
    Story.append(Spacer(1, 0.2 * inch))
    
    # 5. Key Factors (SHAP)
    Story.append(Paragraph("4. Key Factors Affecting Yield", heading_style))
    Story.append(Paragraph("The following factors are having the biggest impact on your predicted yield:", normal_style))
    
    factors = data_dict.get('top_factors', [])
    for factor in factors:
        direction = "Positive" if factor['impact'] > 0 else "Negative"
        color_hex = '#2D6A2A' if factor['impact'] > 0 else '#D9534F'
        impact_style = ParagraphStyle(
            'Impact', parent=normal_style,
            textColor=colors.HexColor(color_hex),
            bulletText='•'
        )
        text = f"<b>{factor['name']}</b>: {direction} impact ({factor['percentage']:.1f}%)"
        Story.append(Paragraph(text, impact_style))
    
    Story.append(Spacer(1, 0.2 * inch))
    
    # 6. Action Plan
    Story.append(Paragraph("5. Action Plan & Advisory", heading_style))
    recs = data_dict.get('recommendations', ["Maintain current agricultural practices."])
    
    for rec in recs:
        Story.append(Paragraph(rec, ParagraphStyle('Bullet', parent=normal_style, bulletText='→')))
        
    Story.append(Spacer(1, 0.5 * inch))
    Story.append(Paragraph("<i>Disclaimer: This is an AI-generated advisory based on historical data and current conditions. Always consult local agricultural extension officers for critical farming decisions.</i>", 
                           ParagraphStyle('Disclaimer', parent=normal_style, fontSize=9, textColor=colors.grey)))
    
    # Build PDF
    doc.build(Story)
    return file_path
