"""
NeuroFlow - Gradio UI Module
============================
Modern, responsive user interface using Gradio.
Clean design with loading animations and interactive elements.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

import gradio as gr

from config import (
    APP_NAME, APP_TAGLINE, APP_DESCRIPTION, APP_VERSION,
    ENERGY_PATTERNS, BREAK_STRUCTURES, DIFFICULTY_LEVELS,
    CUSTOM_CSS, ERROR_MESSAGES, SUCCESS_MESSAGES,
    validate_inputs, get_burnout_risk_level, get_productivity_label,
    THEME_COLORS
)
from ai_engine import create_ai_engine, GeminiAIEngine, FallbackAIEngine
from study_planner import StudyPlannerEngine
from cognitive_analyzer import CognitiveAnalyzer
from pdf_exporter import PDFExporter, PDFConfig


class NeuroFlowUI:
    """
    NeuroFlow User Interface.
    Provides an intuitive, modern interface for the study planner.
    """
    
    def __init__(self):
        """Initialize the UI."""
        self.ai_engine = None
        self.current_schedule = None
        self.current_analysis = None
        self.current_productivity_score = None
        self.user_inputs = None
    
    def _get_welcome_html(self) -> str:
        """Generate welcome section HTML."""
        return f"""
        <div class="header-section">
            <h1 class="header-title">{APP_NAME}</h1>
            <p class="header-subtitle">{APP_TAGLINE}</p>
            <p style="opacity: 0.8; margin-top: 10px;">{APP_DESCRIPTION}</p>
            <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 15px;">v{APP_VERSION}</p>
        </div>
        """
    
    def _get_loading_html(self) -> str:
        """Generate loading animation HTML."""
        return """
        <div class="loading-spinner">
            <div class="spinner"></div>
        </div>
        <p style="text-align: center; color: #6366F1; font-weight: 500;">
            AI is crafting your personalized study plan...
        </p>
        """
    
    def _format_schedule_html(self, schedule: Dict[str, Any]) -> str:
        """Format schedule as HTML table."""
        if not schedule or "daily_schedule" not in schedule:
            return "<p>No schedule generated yet.</p>"
        
        daily = schedule.get("daily_schedule", [])
        
        html = """
        <div class="timetable-container">
            <div class="timetable-header">
                <h3 style="margin: 0;">📅 Your Personalized Study Timetable</h3>
            </div>
        """
        
        for slot in daily:
            time_str = slot.get("time", "")
            subject = slot.get("subject", "")
            activity = slot.get("activity", "")
            duration = slot.get("duration_minutes", 0)
            intensity = slot.get("intensity", "medium")
            
            # Determine styling based on activity
            if "break" in activity.lower():
                bg_color = "#f3f4f6"
                border_left = "4px solid #9ca3af"
            elif intensity == "high":
                bg_color = "#fef3c7"
                border_left = "4px solid #f59e0b"
            else:
                bg_color = "#ffffff"
                border_left = "4px solid #6366f1"
            
            html += f"""
            <div class="timetable-row" style="background: {bg_color}; border-left: {border_left};">
                <div class="time-slot">{time_str}</div>
                <div>
                    <strong>{subject}</strong>
                    <span style="color: #6b7280; font-size: 0.875rem; margin-left: 8px;">
                        {activity}
                    </span>
                </div>
                <div style="text-align: right; color: #6b7280; font-size: 0.875rem;">
                    {duration} min
                </div>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _format_metrics_html(
        self, 
        productivity: float, 
        burnout: float, 
        cognitive: float,
        efficiency: float
    ) -> str:
        """Format metrics as HTML cards."""
        # Determine colors based on values
        prod_color = "#10b981" if productivity >= 75 else "#f59e0b" if productivity >= 60 else "#ef4444"
        burnout_color = "#10b981" if burnout <= 30 else "#f59e0b" if burnout <= 60 else "#ef4444"
        cognitive_color = "#10b981" if cognitive <= 50 else "#f59e0b" if cognitive <= 70 else "#ef4444"
        efficiency_color = "#10b981" if efficiency >= 75 else "#f59e0b" if efficiency >= 60 else "#ef4444"
        
        return f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0;">
            <div class="metric-card">
                <div class="metric-value" style="color: {prod_color};">{productivity:.0f}</div>
                <div class="metric-label">Productivity Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: {burnout_color};">{burnout:.0f}%</div>
                <div class="metric-label">Burnout Risk</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: {cognitive_color};">{cognitive:.0f}</div>
                <div class="metric-label">Cognitive Load</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: {efficiency_color};">{efficiency:.0f}%</div>
                <div class="metric-label">Efficiency</div>
            </div>
        </div>
        """
    
    def _format_analysis_html(self, analysis: Dict[str, Any]) -> str:
        """Format cognitive analysis as HTML."""
        if not analysis:
            return "<p>No analysis available.</p>"
        
        health = analysis.get("schedule_health", "fair")
        health_colors = {
            "excellent": "#10b981",
            "good": "#8b5cf6",
            "fair": "#f59e0b",
            "poor": "#f97316",
            "critical": "#ef4444"
        }
        health_color = health_colors.get(health, "#6b7280")
        
        html = f"""
        <div style="background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="color: #1f2937; margin-bottom: 16px;">🧠 Cognitive Analysis</h3>
            
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <span style="font-weight: 600;">Schedule Health:</span>
                <span style="background: {health_color}; color: white; padding: 4px 12px; 
                           border-radius: 9999px; font-size: 0.875rem; text-transform: uppercase;">
                    {health}
                </span>
            </div>
        """
        
        # Risk factors
        risk_factors = analysis.get("risk_factors", [])
        if risk_factors and risk_factors[0] != "No major risk factors identified":
            html += """
            <div style="margin-bottom: 16px;">
                <h4 style="color: #ef4444; margin-bottom: 8px;">⚠️ Risk Factors</h4>
                <ul style="margin: 0; padding-left: 20px;">
            """
            for factor in risk_factors:
                html += f"<li style='color: #374151; margin-bottom: 4px;'>{factor}</li>"
            html += "</ul></div>"
        
        # Recommendations
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            html += """
            <div>
                <h4 style="color: #10b981; margin-bottom: 8px;">💡 Recommendations</h4>
            """
            for rec in recommendations:
                html += f"""
                <div class="recommendation-card" style="margin-bottom: 8px;">
                    {rec}
                </div>
                """
            html += "</div>"
        
        # Redistribution suggestions
        redistribution = analysis.get("redistribution_suggestions", [])
        if redistribution:
            html += """
            <div style="margin-top: 16px;">
                <h4 style="color: #8b5cf6; margin-bottom: 8px;">🔄 Suggested Changes</h4>
            """
            for suggestion in redistribution:
                html += f"""
                <div class="warning-card" style="margin-bottom: 8px;">
                    <strong>From:</strong> {suggestion.get('from', '')}<br>
                    <strong>To:</strong> {suggestion.get('to', '')}<br>
                    <em style="color: #6b7280;">{suggestion.get('reason', '')}</em>
                </div>
                """
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _format_rotation_html(self, schedule: Dict[str, Any]) -> str:
        """Format subject rotation as HTML."""
        rotation = schedule.get("subject_rotation", [])
        if not rotation:
            return ""
        
        html = """
        <div style="background: white; border-radius: 12px; padding: 20px; margin: 20px 0; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="color: #1f2937; margin-bottom: 16px;">📊 Weekly Subject Rotation</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #ec4899, #8b5cf6); color: white;">
                        <th style="padding: 12px; text-align: left;">Day</th>
                        <th style="padding: 12px; text-align: left;">Morning</th>
                        <th style="padding: 12px; text-align: left;">Afternoon</th>
                        <th style="padding: 12px; text-align: left;">Evening</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for i, day in enumerate(rotation[:5]):  # Weekdays only
            bg = "#f9fafb" if i % 2 == 0 else "white"
            html += f"""
            <tr style="background: {bg};">
                <td style="padding: 12px; font-weight: 600;">{day.get('day', '')}</td>
                <td style="padding: 12px;">{day.get('morning_subject', '')}</td>
                <td style="padding: 12px;">{day.get('afternoon_subject', '')}</td>
                <td style="padding: 12px;">{day.get('evening_subject', '')}</td>
            </tr>
            """
        
        html += """
                </tbody>
            </table>
        """
        
        # Weekly revision
        revision = schedule.get("weekly_revision", {})
        if revision:
            html += f"""
            <div style="margin-top: 16px; padding: 16px; background: #f0fdf4; 
                        border-radius: 8px; border-left: 4px solid #10b981;">
                <strong>📚 Weekly Revision ({revision.get('day', 'Sunday')}):</strong>
                {revision.get('duration_hours', 2)} hours reviewing 
                {', '.join(revision.get('subjects_to_review', []))}
            </div>
            """
        
        html += "</div>"
        return html
    
    def generate_schedule(
        self,
        subjects_text: str,
        exam_dates_text: str,
        difficulty_levels: str,
        daily_hours: float,
        energy_pattern: str,
        stress_level: int,
        sleep_hours: int,
        break_structure: str,
        api_key: str
    ) -> Tuple[str, str, str, str, str, gr.update]:
        """
        Generate study schedule with all analyses.
        
        Args:
            subjects_text: Comma-separated subject names.
            exam_dates_text: Comma-separated exam dates (YYYY-MM-DD).
            difficulty_levels: Comma-separated difficulty levels (1-5).
            daily_hours: Daily available study hours.
            energy_pattern: Selected energy pattern.
            stress_level: Current stress level (1-10).
            sleep_hours: Average sleep hours.
            break_structure: Selected break structure.
            api_key: Google API key.
            
        Returns:
            Tuple of (loading_html, schedule_html, metrics_html, analysis_html, rotation_html, pdf_button)
        """
        # Parse inputs
        subjects = [s.strip() for s in subjects_text.split(",") if s.strip()]
        exam_dates = [d.strip() for d in exam_dates_text.split(",") if d.strip()]
        
        try:
            difficulties = [int(d.strip()) for d in difficulty_levels.split(",") if d.strip()]
        except ValueError:
            return (
                "",
                "<p style='color: red;'>❌ Invalid difficulty levels. Use numbers 1-5 separated by commas.</p>",
                "", "", "",
                gr.update(visible=False)
            )
        
        # Validate inputs
        valid, error_msg = validate_inputs(subjects, exam_dates, daily_hours, stress_level, sleep_hours)
        if not valid:
            return (
                "",
                f"<p style='color: red;'>{error_msg}</p>",
                "", "", "",
                gr.update(visible=False)
            )
        
        # Pad difficulties if needed
        while len(difficulties) < len(subjects):
            difficulties.append(3)
        difficulties = difficulties[:len(subjects)]
        
        # Store user inputs
        self.user_inputs = {
            "subjects": subjects,
            "exam_dates": exam_dates,
            "difficulty_levels": difficulties,
            "daily_hours": daily_hours,
            "energy_pattern": energy_pattern,
            "stress_level": stress_level,
            "sleep_hours": sleep_hours,
            "break_structure": break_structure
        }
        
        # Initialize AI engine
        if api_key.strip():
            self.ai_engine = create_ai_engine(api_key.strip())
        else:
            self.ai_engine = create_ai_engine(None)
        
        # Show loading
        loading_html = self._get_loading_html()
        
        try:
            # Generate schedule
            success, result = self.ai_engine.generate_study_schedule(
                subjects=subjects,
                exam_dates=exam_dates,
                difficulty_levels=difficulties,
                daily_hours=daily_hours,
                energy_pattern=energy_pattern,
                stress_level=stress_level,
                sleep_hours=sleep_hours,
                break_structure=break_structure
            )
            
            if not success:
                return (
                    "",
                    f"<p style='color: red;'>❌ {result}</p>",
                    "", "", "",
                    gr.update(visible=False)
                )
            
            # Convert to dict if needed
            if hasattr(result, '__dataclass_fields__'):
                self.current_schedule = {
                    "daily_schedule": result.daily_schedule,
                    "deep_work_blocks": result.deep_work_blocks,
                    "break_structure": result.break_structure,
                    "subject_rotation": result.subject_rotation,
                    "weekly_revision": result.weekly_revision,
                    "optimization_notes": result.optimization_notes
                }
            else:
                self.current_schedule = result
            
            # Analyze cognitive load
            analyzer = CognitiveAnalyzer()
            self.current_analysis = analyzer.analyze(
                schedule=self.current_schedule,
                stress_level=stress_level,
                sleep_hours=sleep_hours,
                daily_hours=daily_hours,
                energy_pattern=energy_pattern
            )
            
            # Calculate productivity score
            productivity_result = self._calculate_productivity_score()
            self.current_productivity_score = productivity_result
            
            # Generate HTML outputs
            schedule_html = self._format_schedule_html(self.current_schedule)
            
            metrics_html = self._format_metrics_html(
                productivity=productivity_result,
                burnout=self.current_analysis.get("burnout_risk_percentage", 0),
                cognitive=self.current_analysis.get("cognitive_load_score", 0),
                efficiency=self.current_analysis.get("efficiency_prediction", 0)
            )
            
            analysis_html = self._format_analysis_html(self.current_analysis)
            rotation_html = self._format_rotation_html(self.current_schedule)
            
            return (
                "",  # Clear loading
                schedule_html,
                metrics_html,
                analysis_html,
                rotation_html,
                gr.update(visible=True)  # Show PDF button
            )
            
        except Exception as e:
            return (
                "",
                f"<p style='color: red;'>❌ Error: {str(e)}</p>",
                "", "", "",
                gr.update(visible=False)
            )
    
    def _calculate_productivity_score(self) -> float:
        """Calculate overall productivity score."""
        if not self.current_schedule or not self.current_analysis:
            return 50.0
        
        # Base score
        base_score = 70.0
        
        # Adjust based on cognitive load (lower is better)
        cognitive_load = self.current_analysis.get("cognitive_load_score", 50)
        load_factor = 1 - (cognitive_load / 200)  # 0.75 at 50 load
        
        # Adjust based on burnout risk (lower is better)
        burnout_risk = self.current_analysis.get("burnout_risk_percentage", 50)
        burnout_factor = 1 - (burnout_risk / 150)  # 0.67 at 50 risk
        
        # Adjust based on efficiency prediction
        efficiency = self.current_analysis.get("efficiency_prediction", 70)
        efficiency_factor = efficiency / 100
        
        # Calculate final score
        score = base_score * load_factor * burnout_factor * efficiency_factor
        
        # Boost for good break structure
        break_structure = self.current_schedule.get("break_structure", {})
        if break_structure.get("work_duration", 60) <= 50:
            score *= 1.05
        
        return min(round(score, 1), 100)
    
    def export_pdf(self) -> Tuple[Optional[str], str]:
        """
        Export current schedule as PDF.
        
        Returns:
            Tuple of (file_path, status_message)
        """
        if not self.current_schedule or not self.current_analysis:
            return None, "❌ No schedule to export. Generate a schedule first."
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"neuroflow_schedule_{timestamp}.pdf"
            
            exporter = PDFExporter()
            filepath = exporter.export_schedule(
                schedule=self.current_schedule,
                analysis=self.current_analysis,
                productivity_score=self.current_productivity_score or 70,
                user_inputs=self.user_inputs or {},
                output_path=filename
            )
            
            return filepath, f"✅ PDF exported successfully: {filename}"
            
        except Exception as e:
            return None, f"❌ PDF export failed: {str(e)}"
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.
        
        Returns:
            Gradio Blocks interface.
        """
        with gr.Blocks(css=CUSTOM_CSS, title=f"{APP_NAME} - {APP_TAGLINE}") as demo:
            # Header
            gr.HTML(self._get_welcome_html())
            
            with gr.Row():
                # Input Section
                with gr.Column(scale=1):
                    gr.Markdown("## 📋 Your Information")
                    
                    with gr.Group():
                        api_key = gr.Textbox(
                            label="Google API Key (Optional)",
                            placeholder="Enter your Gemini API key or leave blank for basic mode",
                            type="password",
                            info="Get key from makersuite.google.com"
                        )
                        
                        subjects = gr.Textbox(
                            label="Subjects",
                            placeholder="e.g., Mathematics, Physics, Chemistry, English",
                            info="Enter subjects separated by commas"
                        )
                        
                        exam_dates = gr.Textbox(
                            label="Exam Dates",
                            placeholder="e.g., 2024-06-15, 2024-06-20, 2024-06-25, 2024-06-18",
                            info="Enter dates (YYYY-MM-DD) in same order as subjects"
                        )
                        
                        difficulty = gr.Textbox(
                            label="Difficulty Levels (1-5)",
                            placeholder="e.g., 5, 4, 3, 2",
                            info="1=Very Easy, 5=Very Hard. Same order as subjects"
                        )
                    
                    with gr.Group():
                        daily_hours = gr.Slider(
                            label="Daily Study Hours",
                            minimum=1,
                            maximum=16,
                            value=8,
                            step=0.5,
                            info="Total hours you can study per day"
                        )
                        
                        energy_pattern = gr.Dropdown(
                            label="Energy Pattern",
                            choices=list(ENERGY_PATTERNS.keys()),
                            value="morning_high",
                            info="When do you feel most alert?"
                        )
                        
                        break_structure = gr.Dropdown(
                            label="Break Structure",
                            choices=list(BREAK_STRUCTURES.keys()),
                            value="Deep Focus (50-10)",
                            info="Preferred work-break cycle"
                        )
                    
                    with gr.Group():
                        stress_level = gr.Slider(
                            label="Current Stress Level",
                            minimum=1,
                            maximum=10,
                            value=5,
                            step=1,
                            info="1=Very Relaxed, 10=Extremely Stressed"
                        )
                        
                        sleep_hours = gr.Slider(
                            label="Average Sleep Hours",
                            minimum=3,
                            maximum=12,
                            value=7,
                            step=0.5,
                            info="Hours of sleep per night"
                        )
                    
                    generate_btn = gr.Button(
                        "🚀 Generate My Study Plan",
                        variant="primary",
                        elem_classes=["btn-primary"]
                    )
                
                # Output Section
                with gr.Column(scale=2):
                    loading_output = gr.HTML()
                    
                    metrics_output = gr.HTML(
                        label="Performance Metrics"
                    )
                    
                    with gr.Tabs():
                        with gr.TabItem("📅 Daily Schedule"):
                            schedule_output = gr.HTML()
                        
                        with gr.TabItem("🧠 Cognitive Analysis"):
                            analysis_output = gr.HTML()
                        
                        with gr.TabItem("📊 Weekly Rotation"):
                            rotation_output = gr.HTML()
                    
                    pdf_btn = gr.Button(
                        "📄 Export as PDF",
                        visible=False
                    )
                    pdf_status = gr.Textbox(
                        label="",
                        interactive=False,
                        show_label=False
                    )
            
            # Event handlers
            generate_btn.click(
                fn=self.generate_schedule,
                inputs=[
                    subjects, exam_dates, difficulty,
                    daily_hours, energy_pattern, stress_level,
                    sleep_hours, break_structure, api_key
                ],
                outputs=[
                    loading_output, schedule_output, metrics_output,
                    analysis_output, rotation_output, pdf_btn
                ]
            )
            
            pdf_btn.click(
                fn=self.export_pdf,
                outputs=[gr.File(label="Download PDF"), pdf_status]
            )
            
            # Footer
            gr.Markdown("""
            ---
            <div style="text-align: center; color: #6b7280; padding: 20px;">
                <p>Made with ❤️ by NeuroFlow AI | Achieve 90%+ scores without burnout</p>
                <p style="font-size: 0.8rem;">Powered by Google Gemini & Gradio</p>
            </div>
            """)
        
        return demo


def launch_app(share: bool = True, server_port: Optional[int] = None) -> None:
    """
    Launch the NeuroFlow application.
    
    Args:
        share: Whether to create a public shareable link.
        server_port: Optional server port.
    """
    ui = NeuroFlowUI()
    demo = ui.create_interface()
    
    demo.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
        show_error=True
    )


if __name__ == "__main__":
    launch_app()
