#!/usr/bin/env python3
"""
GEO-SEO PDF Report Generator
Generates professional, client-ready PDF reports from GEO audit data.

Usage:
    python3 GeneratePdfReport.py <json_data_file> [output_file.pdf]
    cat audit_data.json | python3 GeneratePdfReport.py - output.pdf

Without arguments, generates a sample report for demonstration.

Ported from: github.com/zubair-trabzada/geo-seo-claude (MIT License)
Requires: pip install reportlab
"""

import sys
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, lightgrey
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, KeepTogether
    )
    from reportlab.graphics.shapes import Drawing, Rect, String, Circle
    from reportlab.graphics.charts.barcharts import VerticalBarChart
except ImportError:
    print("ERROR: ReportLab is required. Run: pip install reportlab")
    sys.exit(1)


# Color palette
PRIMARY = HexColor("#1a1a2e")
SECONDARY = HexColor("#16213e")
ACCENT = HexColor("#0f3460")
HIGHLIGHT = HexColor("#e94560")
SUCCESS = HexColor("#00b894")
WARNING = HexColor("#fdcb6e")
DANGER = HexColor("#d63031")
INFO = HexColor("#0984e3")
LIGHT_BG = HexColor("#f8f9fa")
MEDIUM_BG = HexColor("#e9ecef")
TEXT_PRIMARY = HexColor("#2d3436")
TEXT_SECONDARY = HexColor("#636e72")
WHITE = white


def get_score_color(score):
    if score >= 80: return SUCCESS
    elif score >= 60: return INFO
    elif score >= 40: return WARNING
    else: return DANGER


def get_score_label(score):
    if score >= 85: return "Excellent"
    elif score >= 70: return "Good"
    elif score >= 55: return "Moderate"
    elif score >= 40: return "Below Average"
    else: return "Needs Attention"


def create_score_gauge(score, width=120, height=120):
    d = Drawing(width, height)
    d.add(Circle(width/2, height/2, 50, fillColor=LIGHT_BG, strokeColor=lightgrey, strokeWidth=2))
    d.add(Circle(width/2, height/2, 45, fillColor=get_score_color(score), strokeColor=None))
    d.add(Circle(width/2, height/2, 35, fillColor=WHITE, strokeColor=None))
    d.add(String(width/2, height/2 + 5, str(score), fontSize=24, fontName='Helvetica-Bold',
                 fillColor=TEXT_PRIMARY, textAnchor='middle'))
    d.add(String(width/2, height/2 - 12, "/100", fontSize=10, fontName='Helvetica',
                 fillColor=TEXT_SECONDARY, textAnchor='middle'))
    return d


def create_bar_chart(data, labels, width=400, height=200):
    d = Drawing(width, height)
    chart = VerticalBarChart()
    chart.x, chart.y = 60, 30
    chart.height, chart.width = height - 60, width - 80
    chart.data = [data]
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.fontName = 'Helvetica'
    chart.valueAxis.valueMin, chart.valueAxis.valueMax, chart.valueAxis.valueStep = 0, 100, 20
    chart.valueAxis.labels.fontSize = 8
    for i, score in enumerate(data):
        chart.bars[0].fillColor = get_score_color(score)
    chart.bars[0].strokeColor = None
    d.add(chart)
    return d


def create_platform_chart(platforms, width=450, height=180):
    d = Drawing(width, height)
    bar_height, bar_max_width = 22, 280
    start_y = height - 30
    for i, (name, score) in enumerate(platforms.items()):
        y = start_y - (i * (bar_height + 10))
        d.add(String(10, y + 5, name, fontSize=9, fontName='Helvetica',
                     fillColor=TEXT_PRIMARY, textAnchor='start'))
        bar_x = 130
        d.add(Rect(bar_x, y, bar_max_width, bar_height, fillColor=LIGHT_BG, strokeColor=None))
        bar_width = (score / 100) * bar_max_width
        d.add(Rect(bar_x, y, bar_width, bar_height, fillColor=get_score_color(score), strokeColor=None))
        d.add(String(bar_x + bar_max_width + 10, y + 6, f"{score}/100", fontSize=9,
                     fontName='Helvetica-Bold', fillColor=TEXT_PRIMARY, textAnchor='start'))
    return d


def build_styles():
    styles = getSampleStyleSheet()
    custom_styles = {
        'ReportTitle': ParagraphStyle('ReportTitle', fontName='Helvetica-Bold', fontSize=28,
                                       textColor=PRIMARY, spaceAfter=6),
        'ReportSubtitle': ParagraphStyle('ReportSubtitle', fontName='Helvetica', fontSize=14,
                                          textColor=TEXT_SECONDARY, spaceAfter=20),
        'SectionHeader': ParagraphStyle('SectionHeader', fontName='Helvetica-Bold', fontSize=18,
                                         textColor=PRIMARY, spaceBefore=20, spaceAfter=10),
        'SubHeader': ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=13,
                                     textColor=ACCENT, spaceBefore=14, spaceAfter=6),
        'BodyText_Custom': ParagraphStyle('BodyText_Custom', fontName='Helvetica', fontSize=10,
                                           textColor=TEXT_PRIMARY, spaceBefore=4, spaceAfter=4,
                                           leading=14, alignment=TA_JUSTIFY),
        'SmallText': ParagraphStyle('SmallText', fontName='Helvetica', fontSize=8,
                                     textColor=TEXT_SECONDARY, spaceBefore=2, spaceAfter=2),
        'Recommendation': ParagraphStyle('Recommendation', fontName='Helvetica', fontSize=10,
                                          textColor=TEXT_PRIMARY, leftIndent=15, spaceBefore=3,
                                          spaceAfter=3, bulletIndent=5, leading=14),
    }
    for name, style in custom_styles.items():
        styles.add(style)
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(50, letter[1] - 40, letter[0] - 50, letter[1] - 40)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TEXT_SECONDARY)
    canvas.drawString(50, letter[1] - 35, "GEO-SEO Analysis Report")
    canvas.setStrokeColor(lightgrey)
    canvas.setLineWidth(0.5)
    canvas.line(50, 40, letter[0] - 50, 40)
    canvas.drawString(50, 28, f"Generated {datetime.now().strftime('%B %d, %Y')}")
    canvas.drawRightString(letter[0] - 50, 28, f"Page {doc.page}")
    canvas.drawCentredString(letter[0] / 2, 28, "Confidential")
    canvas.restoreState()


def make_table_style(header_color=PRIMARY):
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])


def generate_report(data, output_path="GEO-REPORT.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=55, bottomMargin=55,
                            leftMargin=50, rightMargin=50)
    styles = build_styles()
    elements = []

    url = data.get("url", "https://example.com")
    brand_name = data.get("brand_name", url.replace("https://", "").replace("http://", "").split("/")[0])
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    geo_score = data.get("geo_score", 0)
    scores = data.get("scores", {})
    ai_citability = scores.get("ai_citability", 0)
    brand_authority = scores.get("brand_authority", 0)
    content_eeat = scores.get("content_eeat", 0)
    technical = scores.get("technical", 0)
    schema_score = scores.get("schema", 0)
    platform_optimization = scores.get("platform_optimization", 0)
    platforms = data.get("platforms", {"Google AI Overviews": 0, "ChatGPT": 0, "Perplexity": 0, "Gemini": 0, "Bing Copilot": 0})
    findings = data.get("findings", [])
    quick_wins = data.get("quick_wins", [])
    medium_term = data.get("medium_term", [])
    strategic = data.get("strategic", [])
    executive_summary = data.get("executive_summary", "")
    crawler_access = data.get("crawler_access", {})

    # Cover Page
    elements.append(Spacer(1, 100))
    elements.append(Paragraph("GEO Analysis Report", styles['ReportTitle']))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Generative Engine Optimization Audit for <b>{brand_name}</b>", styles['ReportSubtitle']))
    elements.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=20))

    details = Table([["Website", url], ["Analysis Date", date], ["GEO Score", f"{geo_score}/100 — {get_score_label(geo_score)}"]], colWidths=[120, 350])
    details.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), ACCENT), ('TEXTCOLOR', (1, 0), (1, -1), TEXT_PRIMARY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10), ('LINEBELOW', (0, 0), (-1, -2), 0.5, lightgrey),
    ]))
    elements.extend([details, Spacer(1, 30), create_score_gauge(geo_score, 200, 200), PageBreak()])

    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    summary_text = executive_summary or (
        f"This report presents the findings of a comprehensive GEO audit for <b>{brand_name}</b> ({url}). "
        f"The overall GEO Readiness Score is <b>{geo_score}/100</b> ({get_score_label(geo_score)}).")
    elements.extend([Paragraph(summary_text, styles['BodyText_Custom']), Spacer(1, 16)])

    # Score Breakdown — weights must match ScoringMethodology.md (canonical source)
    elements.append(Paragraph("GEO Score Breakdown", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    score_data = [
        ["Component", "Score", "Weight", "Weighted"],
        ["AI Citability & Visibility", f"{ai_citability}/100", "25%", f"{round(ai_citability * 0.25, 1)}"],
        ["Brand Authority Signals", f"{brand_authority}/100", "20%", f"{round(brand_authority * 0.20, 1)}"],
        ["Content Quality & E-E-A-T", f"{content_eeat}/100", "20%", f"{round(content_eeat * 0.20, 1)}"],
        ["Technical Foundations", f"{technical}/100", "15%", f"{round(technical * 0.15, 1)}"],
        ["Structured Data", f"{schema_score}/100", "10%", f"{round(schema_score * 0.10, 1)}"],
        ["Platform Optimization", f"{platform_optimization}/100", "10%", f"{round(platform_optimization * 0.10, 1)}"],
        ["OVERALL", f"{geo_score}/100", "100%", f"{geo_score}"],
    ]
    st = Table(score_data, colWidths=[200, 80, 60, 80])
    style = make_table_style()
    style.add('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
    style.add('BACKGROUND', (0, -1), (-1, -1), MEDIUM_BG)
    st.setStyle(style)
    elements.extend([st, Spacer(1, 16)])

    chart_scores = [ai_citability, brand_authority, content_eeat, technical, schema_score, platform_optimization]
    elements.extend([create_bar_chart(chart_scores, ["Citability", "Brand", "Content", "Technical", "Schema", "Platform"]), PageBreak()])

    # Platform Readiness
    elements.append(Paragraph("AI Platform Readiness", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    if platforms:
        elements.append(create_platform_chart(platforms))
    elements.append(PageBreak())

    # Crawler Access
    elements.append(Paragraph("AI Crawler Access Status", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    if crawler_access:
        cd = [["Crawler", "Platform", "Status", "Recommendation"]]
        for name, info in crawler_access.items():
            if isinstance(info, dict):
                cd.append([name, info.get("platform", ""), info.get("status", "Unknown"), info.get("recommendation", "")])
            else:
                cd.append([name, "", str(info), ""])
        ct = Table(cd, colWidths=[100, 100, 80, 180])
        ct.setStyle(make_table_style())
        elements.append(ct)
    elements.append(PageBreak())

    # Findings
    elements.append(Paragraph("Key Findings", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    for f in findings:
        sev = f.get("severity", "info").upper()
        sev_color = {
            "CRITICAL": DANGER, "HIGH": WARNING, "MEDIUM": INFO
        }.get(sev, TEXT_SECONDARY)
        elements.append(Paragraph(
            f'<font color="{sev_color.hexval()}">[{sev}]</font> <b>{f.get("title", "")}</b>',
            styles['BodyText_Custom']))
        if f.get("description"):
            elements.append(Paragraph(f["description"], styles['Recommendation']))
    elements.append(PageBreak())

    # Action Plan
    elements.append(Paragraph("Prioritized Action Plan", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    for section_name, items, desc in [
        ("Quick Wins (This Week)", quick_wins, "High impact, low effort."),
        ("Medium-Term (This Month)", medium_term, "Moderate effort, significant impact."),
        ("Strategic (This Quarter)", strategic, "Long-term competitive advantage."),
    ]:
        elements.append(Paragraph(section_name, styles['SubHeader']))
        elements.append(Paragraph(desc, styles['SmallText']))
        for i, action in enumerate(items, 1):
            text = f"<b>{i}.</b> {action.get('action', action) if isinstance(action, dict) else action}"
            elements.append(Paragraph(text, styles['Recommendation']))
        elements.append(Spacer(1, 12))

    # Methodology
    elements.append(PageBreak())
    elements.append(Paragraph("Appendix: Methodology", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    elements.append(Paragraph(
        f"GEO audit conducted on {date} analyzing {url}. Dimensions: AI Citability (25%), "
        "Brand Authority (20%), Content E-E-A-T (20%), Technical (15%), Schema (10%), Platform (10%).",
        styles['BodyText_Custom']))

    glossary = [
        ["Term", "Definition"],
        ["GEO", "Generative Engine Optimization — optimizing content for AI search citation"],
        ["AIO", "AI Overviews — Google's AI-generated answer boxes"],
        ["E-E-A-T", "Experience, Expertise, Authoritativeness, Trustworthiness"],
        ["SSR", "Server-Side Rendering — generating HTML on server for crawler access"],
        ["JSON-LD", "JavaScript Object Notation for Linked Data — preferred structured data format"],
        ["sameAs", "Schema.org property linking entity to profiles on other platforms"],
        ["llms.txt", "Proposed standard file for guiding AI systems about site content"],
        ["IndexNow", "Protocol for instantly notifying search engines of content changes"],
    ]
    gt = Table(glossary, colWidths=[80, 380])
    gt.setStyle(make_table_style())
    elements.extend([Spacer(1, 16), Paragraph("Glossary", styles['SubHeader']), gt])

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sample = {
            "url": "https://example.com", "brand_name": "Example Company",
            "date": datetime.now().strftime("%Y-%m-%d"), "geo_score": 58,
            "scores": {"ai_citability": 45, "brand_authority": 62, "content_eeat": 70,
                       "technical": 55, "schema": 30, "platform_optimization": 48},
            "platforms": {"Google AI Overviews": 65, "ChatGPT": 52, "Perplexity": 48, "Gemini": 60, "Bing Copilot": 45},
            "executive_summary": "Sample GEO audit report demonstrating PDF generation capabilities.",
            "findings": [
                {"severity": "critical", "title": "No Schema Markup", "description": "No JSON-LD structured data detected."},
                {"severity": "high", "title": "JS-Only Rendering", "description": "Content invisible to AI crawlers."},
            ],
            "quick_wins": ["Allow AI crawlers in robots.txt", "Add publication dates", "Create llms.txt"],
            "medium_term": ["Implement Organization schema", "Optimize content for citability"],
            "strategic": ["Build Wikipedia presence", "Develop YouTube content strategy"],
            "crawler_access": {
                "GPTBot": {"platform": "ChatGPT", "status": "Allowed", "recommendation": "Keep"},
                "ClaudeBot": {"platform": "Claude", "status": "Blocked", "recommendation": "Unblock"},
            },
        }
        print(f"Report generated: {generate_report(sample, 'GEO-REPORT-sample.pdf')}")
    else:
        input_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "GEO-REPORT.pdf"
        data = json.loads(sys.stdin.read()) if input_path == "-" else json.load(open(input_path))
        print(f"Report generated: {generate_report(data, output_file)}")
