"""
NeuroFlow - Configuration Module
================================
Centralized configuration for the AI Study Planner application.
Contains constants, API settings, and default values.
"""

import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

# =============================================================================
# API CONFIGURATION
# =============================================================================

# Get API key from environment variable or use placeholder
# Users should set: export GOOGLE_API_KEY="your_api_key_here"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Gemini Model Configuration
GEMINI_MODEL = "gemini-1.5-flash"  # Fast and cost-effective
GEMINI_TEMPERATURE = 0.3  # Lower for more consistent outputs
GEMINI_MAX_TOKENS = 4096
GEMINI_TOP_P = 0.9
GEMINI_TOP_K = 40

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

APP_NAME = "NeuroFlow"
APP_TAGLINE = "AI-Powered Adaptive Study Planner"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = """
NeuroFlow creates optimized daily study schedules based on your energy cycles, 
academic goals, subject difficulty, and exam timelines. Achieve 90%+ scores without burnout.
"""

# =============================================================================
# STUDY PLANNING CONSTANTS
# =============================================================================

# Break structure templates (work_minutes, break_minutes)
BREAK_STRUCTURES = {
    "Pomodoro (25-5)": (25, 5),
    "Deep Focus (50-10)": (50, 10),
    "Ultra Deep (90-20)": (90, 20),
    "Micro Learning (15-3)": (15, 3),
}

# Energy patterns with optimal subject placement
ENERGY_PATTERNS = {
    "morning_high": {
        "name": "Morning High (Early Bird)",
        "peak_hours": [6, 7, 8, 9, 10, 11],
        "dip_hours": [14, 15, 16],
        "optimal_subjects": "difficult",
        "description": "Peak cognitive performance in morning hours"
    },
    "afternoon_high": {
        "name": "Afternoon High",
        "peak_hours": [12, 13, 14, 15, 16, 17],
        "dip_hours": [9, 10, 11],
        "optimal_subjects": "moderate",
        "description": "Best performance during midday hours"
    },
    "night_high": {
        "name": "Night Owl",
        "peak_hours": [20, 21, 22, 23, 0, 1],
        "dip_hours": [14, 15, 16],
        "optimal_subjects": "difficult",
        "description": "Peak focus during late night hours"
    },
    "bimodal": {
        "name": "Bimodal (Morning + Evening)",
        "peak_hours": [7, 8, 9, 19, 20, 21, 22],
        "dip_hours": [13, 14, 15],
        "optimal_subjects": "mixed",
        "description": "Two peak periods with afternoon dip"
    },
    "consistent": {
        "name": "Consistent Energy",
        "peak_hours": [9, 10, 11, 14, 15, 16, 20],
        "dip_hours": [13, 19],
        "optimal_subjects": "any",
        "description": "Steady energy throughout the day"
    }
}

# Subject difficulty mapping
DIFFICULTY_LEVELS = {
    1: {"label": "Very Easy", "cognitive_load": 0.6, "color": "#4CAF50"},
    2: {"label": "Easy", "cognitive_load": 0.7, "color": "#8BC34A"},
    3: {"label": "Moderate", "cognitive_load": 0.8, "color": "#FFC107"},
    4: {"label": "Hard", "cognitive_load": 0.9, "color": "#FF9800"},
    5: {"label": "Very Hard", "cognitive_load": 1.0, "color": "#F44336"},
}

# Stress level impact on productivity
STRESS_IMPACT = {
    range(1, 4): {"factor": 1.1, "label": "Optimal", "color": "#4CAF50"},
    range(4, 7): {"factor": 1.0, "label": "Normal", "color": "#8BC34A"},
    range(7, 9): {"factor": 0.8, "label": "Elevated", "color": "#FF9800"},
    range(9, 11): {"factor": 0.6, "label": "High", "color": "#F44336"},
}

# Sleep quality impact
SLEEP_IMPACT = {
    range(0, 5): {"factor": 0.6, "label": "Severe Deprivation", "risk": "High"},
    range(5, 6): {"factor": 0.75, "label": "Insufficient", "risk": "Medium-High"},
    range(6, 7): {"factor": 0.85, "label": "Below Optimal", "risk": "Medium"},
    range(7, 9): {"factor": 1.0, "label": "Optimal", "risk": "Low"},
    range(9, 13): {"factor": 0.9, "label": "Excessive", "risk": "Low"},
}

# Burnout risk thresholds
BURNOUT_THRESHOLDS = {
    "low": {"max": 30, "color": "#4CAF50", "message": "Healthy study load"},
    "medium": {"max": 60, "color": "#FF9800", "message": "Monitor stress levels"},
    "high": {"max": 85, "color": "#F44336", "message": "Risk of burnout - reduce load"},
    "critical": {"max": 100, "color": "#9C27B0", "message": "Immediate intervention needed"},
}

# Productivity score ranges
PRODUCTIVITY_RANGES = {
    "excellent": {"min": 90, "color": "#4CAF50", "label": "Excellent"},
    "good": {"min": 75, "color": "#8BC34A", "label": "Good"},
    "average": {"min": 60, "color": "#FFC107", "label": "Average"},
    "below_average": {"min": 40, "color": "#FF9800", "label": "Below Average"},
    "poor": {"min": 0, "color": "#F44336", "label": "Poor"},
}

# =============================================================================
# UI CONFIGURATION
# =============================================================================

# Theme colors
THEME_COLORS = {
    "primary": "#6366F1",      # Indigo
    "secondary": "#8B5CF6",    # Violet
    "accent": "#EC4899",       # Pink
    "success": "#10B981",      # Emerald
    "warning": "#F59E0B",      # Amber
    "danger": "#EF4444",       # Red
    "info": "#3B82F6",         # Blue
    "dark": "#1F2937",         # Gray 800
    "light": "#F3F4F6",        # Gray 100
}

# CSS Customization for Gradio
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-color: #6366F1;
    --secondary-color: #8B5CF6;
    --accent-color: #EC4899;
    --success-color: #10B981;
    --warning-color: #F59E0B;
    --danger-color: #EF4444;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.header-section {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
}

.header-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

.input-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--dark);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.metric-card {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid #e2e8f0;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

.metric-label {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.25rem;
}

.timetable-container {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.timetable-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 1rem;
    font-weight: 600;
}

.timetable-row {
    display: grid;
    grid-template-columns: 100px 1fr 120px;
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
    align-items: center;
}

.timetable-row:hover {
    background: #f8fafc;
}

.time-slot {
    font-weight: 600;
    color: var(--primary-color);
}

.subject-tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

.difficulty-1 { background: #dcfce7; color: #166534; }
.difficulty-2 { background: #d1fae5; color: #065f46; }
.difficulty-3 { background: #fef3c7; color: #92400e; }
.difficulty-4 { background: #ffedd5; color: #9a3412; }
.difficulty-5 { background: #fee2e2; color: #991b1b; }

.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #e2e8f0;
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.alert {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.alert-success { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
.alert-warning { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
.alert-danger { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }

.btn-primary {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.recommendation-card {
    background: #f0fdf4;
    border-left: 4px solid var(--success-color);
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.75rem;
}

.warning-card {
    background: #fffbeb;
    border-left: 4px solid var(--warning-color);
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.75rem;
}
"""

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

STUDY_PLAN_PROMPT = """
You are NeuroFlow, an expert AI study planner with deep knowledge of cognitive science, 
learning psychology, and exam preparation strategies.

Create a personalized study schedule based on the following inputs:

USER PROFILE:
- Subjects: {subjects}
- Exam Dates: {exam_dates}
- Difficulty Levels: {difficulty_levels}
- Daily Available Hours: {daily_hours}
- Energy Pattern: {energy_pattern}
- Stress Level: {stress_level}/10
- Sleep Hours: {sleep_hours}
- Preferred Break Structure: {break_structure}

REQUIREMENTS:
1. Create a detailed daily timetable with specific time slots
2. Place difficult subjects during peak energy hours
3. Include appropriate breaks based on the selected structure
4. Add subject rotation to prevent mental fatigue
5. Include weekly revision slots
6. Calculate realistic daily study capacity

OUTPUT FORMAT (JSON):
{{
    "daily_schedule": [
        {{
            "time": "HH:MM - HH:MM",
            "subject": "Subject Name",
            "activity": "Study/Review/Practice",
            "duration_minutes": int,
            "intensity": "high/medium/low"
        }}
    ],
    "deep_work_blocks": [
        {{
            "start_time": "HH:MM",
            "duration_hours": float,
            "subject": "Subject Name",
            "focus_technique": "description"
        }}
    ],
    "break_structure": {{
        "type": "Pomodoro/50-10/etc",
        "work_duration": int,
        "break_duration": int,
        "long_break_every": int
    }},
    "subject_rotation": [
        {{
            "day": "Monday/etc",
            "morning_subject": "Subject",
            "afternoon_subject": "Subject",
            "evening_subject": "Subject"
        }}
    ],
    "weekly_revision": {{
        "day": "Sunday/etc",
        "duration_hours": float,
        "subjects_to_review": ["Subject1", "Subject2"]
    }},
    "optimization_notes": ["string"]
}}

Ensure the schedule is realistic, balanced, and optimized for the user's energy pattern.
"""

COGNITIVE_ANALYSIS_PROMPT = """
Analyze the following study schedule for cognitive load and burnout risk:

SCHEDULE DETAILS:
{schedule_details}

USER CONTEXT:
- Stress Level: {stress_level}/10
- Sleep: {sleep_hours} hours
- Daily Hours: {daily_hours}
- Energy Pattern: {energy_pattern}

Provide analysis in this JSON format:
{{
    "cognitive_load_score": float (0-100),
    "burnout_risk_percentage": float (0-100),
    "efficiency_prediction": float (0-100),
    "risk_factors": ["string"],
    "recommendations": ["string"],
    "redistribution_suggestions": [
        {{
            "from": "time/subject",
            "to": "time/subject",
            "reason": "explanation"
        }}
    ],
    "schedule_health": "excellent/good/fair/poor/critical"
}}

Be thorough and specific in your analysis.
"""

PRODUCTIVITY_SCORE_PROMPT = """
Calculate a comprehensive productivity score (0-100) based on:

INPUTS:
- Schedule Quality: {schedule_quality}
- Energy Alignment: {energy_alignment}
- Break Structure: {break_structure}
- Stress Level: {stress_level}/10
- Sleep Quality: {sleep_hours} hours
- Subject Difficulty Balance: {difficulty_balance}

Also provide:
1. Breakdown of score components
2. Specific improvement suggestions
3. Expected outcomes if followed

Output as JSON with detailed reasoning.
"""

# =============================================================================
# ERROR MESSAGES
# =============================================================================

ERROR_MESSAGES = {
    "api_key_missing": "⚠️ GOOGLE_API_KEY not found. Please set your API key in environment variables.",
    "api_error": "🚨 Error communicating with AI service. Please try again.",
    "invalid_input": "❌ Please check your inputs and try again.",
    "schedule_generation_failed": "❌ Failed to generate study schedule. Please try with different inputs.",
    "pdf_generation_failed": "❌ Failed to generate PDF. Please try again.",
    "rate_limit": "⏳ Rate limit exceeded. Please wait a moment and try again.",
    "network_error": "🌐 Network error. Please check your connection.",
}

SUCCESS_MESSAGES = {
    "schedule_generated": "✅ Study schedule generated successfully!",
    "pdf_exported": "📄 PDF exported successfully!",
    "analysis_complete": "📊 Cognitive analysis complete!",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_stress_impact(stress_level: int) -> Dict:
    """Get productivity factor based on stress level."""
    for stress_range, impact in STRESS_IMPACT.items():
        if stress_level in stress_range:
            return impact
    return STRESS_IMPACT[range(4, 7)]  # Default to normal

def get_sleep_impact(sleep_hours: int) -> Dict:
    """Get productivity factor based on sleep hours."""
    for sleep_range, impact in SLEEP_IMPACT.items():
        if sleep_hours in sleep_range:
            return impact
    return SLEEP_IMPACT[range(7, 9)]  # Default to optimal

def get_burnout_risk_level(risk_percentage: float) -> str:
    """Determine burnout risk level from percentage."""
    if risk_percentage <= 30:
        return "low"
    elif risk_percentage <= 60:
        return "medium"
    elif risk_percentage <= 85:
        return "high"
    else:
        return "critical"

def get_productivity_label(score: float) -> str:
    """Get productivity label from score."""
    for key, value in PRODUCTIVITY_RANGES.items():
        if score >= value["min"]:
            return value["label"]
    return "Poor"

def validate_inputs(subjects: List[str], exam_dates: List[str], 
                   daily_hours: float, stress_level: int, 
                   sleep_hours: int) -> Tuple[bool, str]:
    """Validate user inputs."""
    if not subjects or len(subjects) == 0:
        return False, "Please enter at least one subject."
    
    if not exam_dates or len(exam_dates) != len(subjects):
        return False, "Please provide exam dates for all subjects."
    
    if daily_hours < 1 or daily_hours > 16:
        return False, "Daily hours must be between 1 and 16."
    
    if stress_level < 1 or stress_level > 10:
        return False, "Stress level must be between 1 and 10."
    
    if sleep_hours < 3 or sleep_hours > 12:
        return False, "Sleep hours must be between 3 and 12."
    
    return True, ""
