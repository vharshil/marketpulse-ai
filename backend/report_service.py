

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from datetime import datetime


def generate_report_pdf(
    company: str,
    sentiment: dict,
    ml_prediction: dict,
    fusion_score: dict,
    articles: list,
    summary: str,
    ai_analysis: str,
) -> bytes:
    """
    Generates a professional PDF research report.
    Returns the PDF as bytes which FastAPI sends as a file download.
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    NAVY = HexColor('#0A0E1A')
    BLUE = HexColor('#4F8EF7')
    GREEN = HexColor('#00D68F')
    RED = HexColor('#FF4D6A')
    YELLOW = HexColor('#FFB830')
    GRAY = HexColor('#8B9CC8')
    LIGHT = HexColor('#F0F4FF')
    CARD = HexColor('#1A2236')

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=22,
        fontName='Helvetica-Bold',
        textColor=NAVY,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        textColor=GRAY,
        spaceAfter=2,
    )

    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Normal'],
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=NAVY,
        spaceBefore=16,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=HexColor('#2C3E50'),
        spaceAfter=6,
        leading=16,
    )

    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        textColor=GRAY,
    )

    verdict = sentiment.get('verdict', 'Neutral')
    verdict_color = GREEN if verdict == 'Bullish' else RED if verdict == 'Bearish' else YELLOW

    story = []

    story.append(Paragraph(f"MarketPulse AI — Research Report", subtitle_style))
    story.append(Paragraph(f"{company}", title_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} · Powered by Gemini AI + ML",
        small_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=16))

    sentiment_data = [
        ['Overall Verdict', 'Bullish %', 'Bearish %', 'Neutral %'],
        [
            verdict,
            f"{sentiment.get('bullish', 0)}%",
            f"{sentiment.get('bearish', 0)}%",
            f"{sentiment.get('neutral', 0)}%",
        ]
    ]

    sentiment_table = Table(sentiment_data, colWidths=[1.8 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 0), (-1, -1), 28),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('TEXTCOLOR', (0, 1), (0, 1), verdict_color),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))

    story.append(Paragraph("Sentiment Analysis", heading_style))
    story.append(sentiment_table)
    story.append(Spacer(1, 12))

    if ml_prediction and ml_prediction.get('available'):
        ml_pred = ml_prediction.get('prediction', 'N/A')
        ml_color = GREEN if ml_pred == 'Up' else RED if ml_pred == 'Down' else YELLOW

        ml_data = [
            ['ML Trend', 'Confidence', 'Model Accuracy', 'Current Price', '1D Change'],
            [
                ml_pred,
                f"{ml_prediction.get('confidence', 0)}%",
                f"{ml_prediction.get('model_accuracy', 0)}%",
                f"₹{ml_prediction.get('current_price', 'N/A')}",
                f"{ml_prediction.get('price_change_1d', 0)}%",
            ]
        ]

        ml_table = Table(ml_data, colWidths=[1.3 * inch, 1.2 * inch, 1.3 * inch, 1.3 * inch, 1.2 * inch])
        ml_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1A2236')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWHEIGHT', (0, 0), (-1, -1), 26),
            ('BACKGROUND', (0, 1), (-1, 1), LIGHT),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 1), (0, 1), ml_color),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ]))

        story.append(Paragraph("ML Trend Prediction", heading_style))
        story.append(ml_table)
        story.append(Spacer(1, 12))

    if fusion_score:
        story.append(Paragraph("Fusion Confidence Score", heading_style))
        fusion_text = (
            f"<b>Signal: {fusion_score.get('signal', 'N/A')}</b> · "
            f"Confidence: {fusion_score.get('confidence_level', 'N/A')} · "
            f"Agreement: {fusion_score.get('agreement', 'N/A')}<br/><br/>"
            f"{fusion_score.get('explanation', '')}"
        )
        story.append(Paragraph(fusion_text, body_style))

    story.append(Paragraph("AI News Summary", heading_style))
    story.append(Paragraph(summary or "No summary available.", body_style))

    if ai_analysis:
        story.append(Paragraph("Detailed AI Analysis", heading_style))
        for para in ai_analysis.split('\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))

    if articles:
        story.append(Paragraph("News Headlines Analysed", heading_style))
        for i, article in enumerate(articles[:8], 1):
            sent = article.get('sentiment', 'Neutral')
            sent_color = '#00D68F' if sent == 'Bullish' else '#FF4D6A' if sent == 'Bearish' else '#FFB830'
            story.append(Paragraph(
                f"{i}. <b>{article.get('title', '')}</b> "
                f"<font color='{sent_color}'>[{sent}]</font><br/>"
                f"<font size='8' color='#8B9CC8'>{article.get('source', '')} · {article.get('published_at', '')}</font>",
                body_style
            ))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "⚠️ DISCLAIMER: This report is generated by AI based on publicly available news. "
        "It is NOT financial advice. Always consult a SEBI-registered advisor before making investment decisions. "
        "MarketPulse AI is a research tool, not a trading recommendation service.",
        small_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()