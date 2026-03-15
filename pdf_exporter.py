"""
NeuroFlow - PDF Exporter Module
===============================
Exports study schedules and analysis reports as PDF documents.
Professional formatting with charts and visual elements.
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend


@dataclass
class PDFConfig:
    """Configuration for PDF export."""
    filename: str = "neuroflow_schedule.pdf"
    title: str = "NeuroFlow Study Plan"
    subtitle: str = "AI-Generated Personalized Schedule"
    author: str = "NeuroFlow AI"
    page_size: Any = A4


class PDFExporter:
    """
    Professional PDF exporter for NeuroFlow study plans.
    Creates beautifully formatted documents with tables and charts.
    """
    
    # Color scheme
    COLORS = {
        "primary": colors.Color(0.39, 0.40, 0.94),      # Indigo
        "secondary": colors.Color(0.55, 0.36, 0.96),    # Violet
        "accent": colors.Color(0.93, 0.28, 0.60),       # Pink
        "success": colors.Color(0.16, 0.73, 0.51),      # Emerald
        "warning": colors.Color(0.96, 0.62, 0.04),      # Amber
        "danger": colors.Color(0.94, 0.27, 0.27),       # Red
        "dark": colors.Color(0.12, 0.16, 0.22),         # Dark gray
        "light": colors.Color(0.95, 0.96, 0.98),        # Light gray
    }
    
    def __init__(self, config: Optional[PDFConfig] = None):
        """
        Initialize PDF exporter.
        
        Args:
            config: PDF configuration. Uses defaults if None.
        """
        self.config = config or PDFConfig()
        self.styles = self._create_styles()
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles."""
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name="CustomTitle",
            fontSize=28,
            leading=36,
            alignment=TA_CENTER,
            textColor=self.COLORS["primary"],
            fontName="Helvetica-Bold",
            spaceAfter=12
        ))
        
        # Subtitle style
        styles.add(ParagraphStyle(
            name="CustomSubtitle",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=self.COLORS["dark"],
            fontName="Helvetica",
            spaceAfter=24
        ))
        
        # Section header
        styles.add(ParagraphStyle(
            name="SectionHeader",
            fontSize=16,
            leading=20,
            alignment=TA_LEFT,
            textColor=self.COLORS["primary"],
            fontName="Helvetica-Bold",
            spaceBefore=20,
            spaceAfter=12
        ))
        
        # Metric label
        styles.add(ParagraphStyle(
            name="MetricLabel",
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            textColor=self.COLORS["dark"],
            fontName="Helvetica"
        ))
        
        # Metric value
        styles.add(ParagraphStyle(
            name="MetricValue",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=self.COLORS["primary"],
            fontName="Helvetica-Bold"
        ))
        
        # Body text
        styles.add(ParagraphStyle(
            name="BodyText",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            textColor=self.COLORS["dark"],
            fontName="Helvetica",
            spaceAfter=6
        ))
        
        # Recommendation
        styles.add(ParagraphStyle(
            name="Recommendation",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            textColor=self.COLORS["dark"],
            fontName="Helvetica",
            leftIndent=12,
            spaceAfter=4
        ))
        
        return styles
    
    def export_schedule(
        self,
        schedule: Dict[str, Any],
        analysis: Dict[str, Any],
        productivity_score: float,
        user_inputs: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        Export complete study schedule as PDF.
        
        Args:
            schedule: Study schedule dictionary.
            analysis: Cognitive analysis dictionary.
            productivity_score: Overall productivity score.
            user_inputs: User input parameters.
            output_path: Output file path. Uses config default if None.
            
        Returns:
            Path to generated PDF file.
        """
        if output_path is None:
            output_path = self.config.filename
        
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.config.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._create_header())
        
        # Metrics overview
        story.extend(self._create_metrics_overview(
            analysis, productivity_score
        ))
        
        # User profile
        story.extend(self._create_user_profile(user_inputs))
        
        # Daily schedule
        story.extend(self._create_daily_schedule(schedule))
        
        # Deep work blocks
        story.extend(self._create_deep_work_section(schedule))
        
        # Subject rotation
        story.extend(self._create_rotation_section(schedule))
        
        # Analysis and recommendations
        story.extend(self._create_analysis_section(analysis))
        
        # Footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_header(self) -> List[Any]:
        """Create document header."""
        return [
            Paragraph("NeuroFlow", self.styles["CustomTitle"]),
            Paragraph("AI-Generated Personalized Study Plan", self.styles["CustomSubtitle"]),
            HRFlowable(
                width="100%",
                thickness=2,
                color=self.COLORS["primary"],
                spaceBefore=12,
                spaceAfter=24
            ),
        ]
    
    def _create_metrics_overview(
        self, 
        analysis: Dict[str, Any],
        productivity_score: float
    ) -> List[Any]:
        """Create metrics overview section."""
        burnout_risk = analysis.get("burnout_risk_percentage", 0)
        cognitive_load = analysis.get("cognitive_load_score", 0)
        efficiency = analysis.get("efficiency_prediction", 0)
        
        # Create metrics table
        data = [
            [
                Paragraph(f"{productivity_score:.0f}", self.styles["MetricValue"]),
                Paragraph(f"{burnout_risk:.0f}%", self.styles["MetricValue"]),
                Paragraph(f"{cognitive_load:.0f}", self.styles["MetricValue"]),
                Paragraph(f"{efficiency:.0f}%", self.styles["MetricValue"]),
            ],
            [
                Paragraph("Productivity Score", self.styles["MetricLabel"]),
                Paragraph("Burnout Risk", self.styles["MetricLabel"]),
                Paragraph("Cognitive Load", self.styles["MetricLabel"]),
                Paragraph("Efficiency", self.styles["MetricLabel"]),
            ]
        ]
        
        table = Table(data, colWidths=[120, 120, 120, 120])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
        ]))
        
        return [
            Paragraph("Performance Metrics", self.styles["SectionHeader"]),
            table,
            Spacer(1, 20)
        ]
    
    def _create_user_profile(self, user_inputs: Dict[str, Any]) -> List[Any]:
        """Create user profile section."""
        subjects = user_inputs.get("subjects", [])
        daily_hours = user_inputs.get("daily_hours", 8)
        energy_pattern = user_inputs.get("energy_pattern", "")
        stress_level = user_inputs.get("stress_level", 5)
        sleep_hours = user_inputs.get("sleep_hours", 7)
        
        data = [
            ["Subjects", ", ".join(subjects)],
            ["Daily Study Hours", f"{daily_hours} hours"],
            ["Energy Pattern", energy_pattern],
            ["Stress Level", f"{stress_level}/10"],
            ["Sleep Hours", f"{sleep_hours} hours"],
        ]
        
        table = Table(data, colWidths=[150, 350])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.COLORS["light"]),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.COLORS["dark"]),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.COLORS["light"]]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [
            Paragraph("Your Profile", self.styles["SectionHeader"]),
            table,
            Spacer(1, 20)
        ]
    
    def _create_daily_schedule(self, schedule: Dict[str, Any]) -> List[Any]:
        """Create daily schedule table."""
        daily_schedule = schedule.get("daily_schedule", [])
        
        if not daily_schedule:
            return []
        
        # Table header
        data = [["Time", "Subject", "Activity", "Duration", "Intensity"]]
        
        # Table rows
        for slot in daily_schedule:
            time_str = slot.get("time", "")
            subject = slot.get("subject", "")
            activity = slot.get("activity", "")
            duration = f"{slot.get('duration_minutes', 0)} min"
            intensity = slot.get("intensity", "medium").title()
            
            data.append([time_str, subject, activity, duration, intensity])
        
        table = Table(data, colWidths=[100, 120, 100, 70, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS["light"]]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return [
            PageBreak(),
            Paragraph("Daily Study Schedule", self.styles["SectionHeader"]),
            table,
            Spacer(1, 20)
        ]
    
    def _create_deep_work_section(self, schedule: Dict[str, Any]) -> List[Any]:
        """Create deep work blocks section."""
        deep_work = schedule.get("deep_work_blocks", [])
        
        if not deep_work:
            return []
        
        data = [["Start Time", "Duration", "Subject", "Technique"]]
        
        for block in deep_work:
            data.append([
                block.get("start_time", ""),
                f"{block.get('duration_hours', 0):.1f}h",
                block.get("subject", ""),
                block.get("focus_technique", "")
            ])
        
        table = Table(data, colWidths=[100, 80, 150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS["secondary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS["light"]]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [
            Paragraph("Deep Work Blocks", self.styles["SectionHeader"]),
            Paragraph(
                "High-intensity focus sessions for your most challenging subjects.",
                self.styles["BodyText"]
            ),
            Spacer(1, 10),
            table,
            Spacer(1, 20)
        ]
    
    def _create_rotation_section(self, schedule: Dict[str, Any]) -> List[Any]:
        """Create subject rotation section."""
        rotation = schedule.get("subject_rotation", [])
        
        if not rotation:
            return []
        
        data = [["Day", "Morning", "Afternoon", "Evening"]]
        
        for day_plan in rotation[:5]:  # Show weekdays
            data.append([
                day_plan.get("day", ""),
                day_plan.get("morning_subject", ""),
                day_plan.get("afternoon_subject", ""),
                day_plan.get("evening_subject", "")
            ])
        
        table = Table(data, colWidths=[100, 130, 130, 130])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS["accent"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS["light"]]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        # Weekly revision
        revision = schedule.get("weekly_revision", {})
        revision_text = ""
        if revision:
            revision_text = (
                f"<b>Weekly Revision ({revision.get('day', 'Sunday')}):</b> "
                f"{revision.get('duration_hours', 2)} hours reviewing "
                f"{', '.join(revision.get('subjects_to_review', []))}"
            )
        
        return [
            Paragraph("Weekly Subject Rotation", self.styles["SectionHeader"]),
            table,
            Spacer(1, 10),
            Paragraph(revision_text, self.styles["BodyText"]),
            Spacer(1, 20)
        ]
    
    def _create_analysis_section(self, analysis: Dict[str, Any]) -> List[Any]:
        """Create cognitive analysis section."""
        recommendations = analysis.get("recommendations", [])
        risk_factors = analysis.get("risk_factors", [])
        
        elements = [
            PageBreak(),
            Paragraph("Cognitive Analysis & Recommendations", self.styles["SectionHeader"]),
            Spacer(1, 10),
        ]
        
        # Risk factors
        if risk_factors:
            elements.append(Paragraph("<b>Risk Factors:</b>", self.styles["BodyText"]))
            for factor in risk_factors:
                elements.append(Paragraph(f"• {factor}", self.styles["Recommendation"]))
            elements.append(Spacer(1, 10))
        
        # Recommendations
        if recommendations:
            elements.append(Paragraph("<b>Personalized Recommendations:</b>", self.styles["BodyText"]))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles["Recommendation"]))
        
        return elements
    
    def _create_footer(self) -> List[Any]:
        """Create document footer."""
        generated_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        return [
            Spacer(1, 40),
            HRFlowable(
                width="100%",
                thickness=1,
                color=colors.grey,
                spaceBefore=20,
                spaceAfter=10
            ),
            Paragraph(
                f"Generated by NeuroFlow AI on {generated_date}",
                ParagraphStyle(
                    name="Footer",
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.grey
                )
            ),
            Paragraph(
                "www.neuroflow.ai | Achieve 90%+ scores without burnout",
                ParagraphStyle(
                    name="Footer2",
                    fontSize=8,
                    alignment=TA_CENTER,
                    textColor=colors.grey
                )
            )
        ]
    
    def export_simple_schedule(
        self,
        schedule: Dict[str, Any],
        output_path: str = "schedule.pdf"
    ) -> str:
        """
        Export simple schedule without analysis.
        
        Args:
            schedule: Study schedule dictionary.
            output_path: Output file path.
            
        Returns:
            Path to generated PDF.
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        story.extend(self._create_header())
        story.extend(self._create_daily_schedule(schedule))
        story.extend(self._create_footer())
        
        doc.build(story)
        
        return output_path


def export_to_pdf(
    schedule: Dict[str, Any],
    analysis: Dict[str, Any],
    productivity_score: float,
    user_inputs: Dict[str, Any],
    output_path: Optional[str] = None
) -> str:
    """
    Convenience function to export to PDF.
    
    Args:
        schedule: Study schedule.
        analysis: Cognitive analysis.
        productivity_score: Productivity score.
        user_inputs: User inputs.
        output_path: Output path.
        
    Returns:
        Path to generated PDF.
    """
    exporter = PDFExporter()
    return exporter.export_schedule(
        schedule, analysis, productivity_score, user_inputs, output_path
    )
