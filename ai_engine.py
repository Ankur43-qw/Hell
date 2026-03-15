"""
NeuroFlow - AI Engine Module
============================
Handles all interactions with Google's Gemini API.
Provides structured prompt generation and response parsing.
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

import google.generativeai as genai

from config import (
    GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS, GEMINI_TOP_P, GEMINI_TOP_K,
    STUDY_PLAN_PROMPT, COGNITIVE_ANALYSIS_PROMPT, PRODUCTIVITY_SCORE_PROMPT,
    ERROR_MESSAGES
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class StudySchedule:
    """Data class for study schedule."""
    daily_schedule: List[Dict[str, Any]]
    deep_work_blocks: List[Dict[str, Any]]
    break_structure: Dict[str, Any]
    subject_rotation: List[Dict[str, Any]]
    weekly_revision: Dict[str, Any]
    optimization_notes: List[str]


@dataclass
class CognitiveAnalysis:
    """Data class for cognitive analysis results."""
    cognitive_load_score: float
    burnout_risk_percentage: float
    efficiency_prediction: float
    risk_factors: List[str]
    recommendations: List[str]
    redistribution_suggestions: List[Dict[str, str]]
    schedule_health: str


@dataclass
class ProductivityScore:
    """Data class for productivity score."""
    overall_score: float
    components: Dict[str, float]
    improvement_suggestions: List[str]
    expected_outcomes: List[str]


class GeminiAIEngine:
    """
    AI Engine for NeuroFlow using Google's Gemini API.
    Handles all AI-powered features with robust error handling.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Engine.
        
        Args:
            api_key: Google API key. If None, uses environment variable.
        """
        self.api_key = api_key or GOOGLE_API_KEY
        self.model = None
        self._initialized = False
        
        if self.api_key:
            self._initialize_model()
    
    def _initialize_model(self) -> bool:
        """
        Initialize the Gemini model with configuration.
        
        Returns:
            bool: True if initialization successful, False otherwise.
        """
        try:
            genai.configure(api_key=self.api_key)
            
            generation_config = {
                "temperature": GEMINI_TEMPERATURE,
                "top_p": GEMINI_TOP_P,
                "top_k": GEMINI_TOP_K,
                "max_output_tokens": GEMINI_MAX_TOKENS,
            }
            
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config=generation_config
            )
            
            self._initialized = True
            logger.info("Gemini model initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            self._initialized = False
            return False
    
    def is_ready(self) -> bool:
        """Check if AI engine is ready for use."""
        return self._initialized and self.model is not None
    
    def _extract_json_from_response(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from AI response text.
        Handles various formatting scenarios.
        
        Args:
            text: Raw response text from AI.
            
        Returns:
            Parsed JSON dict or None if extraction fails.
        """
        # Try direct JSON parsing first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Look for JSON in code blocks
        json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(json_pattern, text)
        
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
        
        # Look for JSON between curly braces
        brace_pattern = r'\{[\s\S]*\}'
        match = re.search(brace_pattern, text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        
        logger.error(f"Could not extract JSON from response: {text[:200]}...")
        return None
    
    def _safe_api_call(self, prompt: str, max_retries: int = 2) -> Tuple[bool, Any]:
        """
        Make safe API call with retry logic.
        
        Args:
            prompt: The prompt to send to AI.
            max_retries: Maximum number of retry attempts.
            
        Returns:
            Tuple of (success: bool, result: Any)
        """
        if not self.is_ready():
            return False, ERROR_MESSAGES["api_key_missing"]
        
        for attempt in range(max_retries + 1):
            try:
                response = self.model.generate_content(prompt)
                
                if not response or not response.text:
                    if attempt < max_retries:
                        continue
                    return False, ERROR_MESSAGES["api_error"]
                
                return True, response.text
                
            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"API call error (attempt {attempt + 1}): {error_msg}")
                
                if "rate limit" in error_msg or "quota" in error_msg:
                    return False, ERROR_MESSAGES["rate_limit"]
                
                if attempt < max_retries:
                    continue
                
                return False, f"{ERROR_MESSAGES['api_error']} Details: {str(e)}"
        
        return False, ERROR_MESSAGES["api_error"]
    
    def generate_study_schedule(
        self,
        subjects: List[str],
        exam_dates: List[str],
        difficulty_levels: List[int],
        daily_hours: float,
        energy_pattern: str,
        stress_level: int,
        sleep_hours: int,
        break_structure: str
    ) -> Tuple[bool, Any]:
        """
        Generate personalized study schedule using AI.
        
        Args:
            subjects: List of subject names.
            exam_dates: List of exam dates (YYYY-MM-DD format).
            difficulty_levels: List of difficulty levels (1-5) for each subject.
            daily_hours: Daily available study hours.
            energy_pattern: User's energy pattern identifier.
            stress_level: Current stress level (1-10).
            sleep_hours: Average sleep hours per night.
            break_structure: Preferred break structure name.
            
        Returns:
            Tuple of (success: bool, result: StudySchedule or error message)
        """
        # Build prompt with user inputs
        prompt = STUDY_PLAN_PROMPT.format(
            subjects=subjects,
            exam_dates=exam_dates,
            difficulty_levels=difficulty_levels,
            daily_hours=daily_hours,
            energy_pattern=energy_pattern,
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            break_structure=break_structure
        )
        
        success, result = self._safe_api_call(prompt)
        
        if not success:
            return False, result
        
        # Extract and parse JSON
        schedule_data = self._extract_json_from_response(result)
        
        if not schedule_data:
            return False, ERROR_MESSAGES["schedule_generation_failed"]
        
        try:
            schedule = StudySchedule(
                daily_schedule=schedule_data.get("daily_schedule", []),
                deep_work_blocks=schedule_data.get("deep_work_blocks", []),
                break_structure=schedule_data.get("break_structure", {}),
                subject_rotation=schedule_data.get("subject_rotation", []),
                weekly_revision=schedule_data.get("weekly_revision", {}),
                optimization_notes=schedule_data.get("optimization_notes", [])
            )
            return True, schedule
            
        except Exception as e:
            logger.error(f"Error creating StudySchedule: {str(e)}")
            return False, ERROR_MESSAGES["schedule_generation_failed"]
    
    def analyze_cognitive_load(
        self,
        schedule_details: Dict[str, Any],
        stress_level: int,
        sleep_hours: int,
        daily_hours: float,
        energy_pattern: str
    ) -> Tuple[bool, Any]:
        """
        Analyze cognitive load and burnout risk.
        
        Args:
            schedule_details: Details of the generated schedule.
            stress_level: Current stress level (1-10).
            sleep_hours: Average sleep hours.
            daily_hours: Daily study hours.
            energy_pattern: User's energy pattern.
            
        Returns:
            Tuple of (success: bool, result: CognitiveAnalysis or error message)
        """
        prompt = COGNITIVE_ANALYSIS_PROMPT.format(
            schedule_details=json.dumps(schedule_details, indent=2),
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            daily_hours=daily_hours,
            energy_pattern=energy_pattern
        )
        
        success, result = self._safe_api_call(prompt)
        
        if not success:
            return False, result
        
        analysis_data = self._extract_json_from_response(result)
        
        if not analysis_data:
            return False, "Failed to parse cognitive analysis"
        
        try:
            analysis = CognitiveAnalysis(
                cognitive_load_score=analysis_data.get("cognitive_load_score", 50.0),
                burnout_risk_percentage=analysis_data.get("burnout_risk_percentage", 50.0),
                efficiency_prediction=analysis_data.get("efficiency_prediction", 50.0),
                risk_factors=analysis_data.get("risk_factors", []),
                recommendations=analysis_data.get("recommendations", []),
                redistribution_suggestions=analysis_data.get("redistribution_suggestions", []),
                schedule_health=analysis_data.get("schedule_health", "fair")
            )
            return True, analysis
            
        except Exception as e:
            logger.error(f"Error creating CognitiveAnalysis: {str(e)}")
            return False, "Failed to process cognitive analysis"
    
    def calculate_productivity_score(
        self,
        schedule_quality: float,
        energy_alignment: float,
        break_structure: float,
        stress_level: int,
        sleep_hours: int,
        difficulty_balance: float
    ) -> Tuple[bool, Any]:
        """
        Calculate comprehensive productivity score.
        
        Args:
            schedule_quality: Quality score of the schedule (0-100).
            energy_alignment: How well schedule matches energy pattern (0-100).
            break_structure: Quality of break structure (0-100).
            stress_level: Current stress level (1-10).
            sleep_hours: Average sleep hours.
            difficulty_balance: Balance of subject difficulties (0-100).
            
        Returns:
            Tuple of (success: bool, result: ProductivityScore or error message)
        """
        prompt = PRODUCTIVITY_SCORE_PROMPT.format(
            schedule_quality=schedule_quality,
            energy_alignment=energy_alignment,
            break_structure=break_structure,
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            difficulty_balance=difficulty_balance
        )
        
        success, result = self._safe_api_call(prompt)
        
        if not success:
            return False, result
        
        score_data = self._extract_json_from_response(result)
        
        if not score_data:
            return False, "Failed to parse productivity score"
        
        try:
            score = ProductivityScore(
                overall_score=score_data.get("overall_score", 50.0),
                components=score_data.get("components", {}),
                improvement_suggestions=score_data.get("improvement_suggestions", []),
                expected_outcomes=score_data.get("expected_outcomes", [])
            )
            return True, score
            
        except Exception as e:
            logger.error(f"Error creating ProductivityScore: {str(e)}")
            return False, "Failed to process productivity score"
    
    def get_optimization_suggestions(
        self,
        current_schedule: StudySchedule,
        cognitive_analysis: CognitiveAnalysis,
        user_constraints: Dict[str, Any]
    ) -> List[str]:
        """
        Get personalized optimization suggestions.
        
        Args:
            current_schedule: Current study schedule.
            cognitive_analysis: Cognitive analysis results.
            user_constraints: User's constraints and preferences.
            
        Returns:
            List of optimization suggestions.
        """
        suggestions = []
        
        # Add AI-generated recommendations
        suggestions.extend(cognitive_analysis.recommendations)
        
        # Add schedule-specific notes
        suggestions.extend(current_schedule.optimization_notes)
        
        # Add constraint-based suggestions
        if user_constraints.get("stress_level", 5) > 7:
            suggestions.append(
                "⚠️ High stress detected: Consider reducing daily study hours by 1-2 hours "
                "and adding more frequent breaks."
            )
        
        if user_constraints.get("sleep_hours", 7) < 6:
            suggestions.append(
                "💤 Sleep deprivation detected: Prioritize 7-8 hours of sleep for optimal "
                "cognitive performance and memory consolidation."
            )
        
        return suggestions


class FallbackAIEngine:
    """
    Fallback AI engine that uses rule-based algorithms when API is unavailable.
    Provides basic functionality without AI enhancement.
    """
    
    def __init__(self):
        """Initialize fallback engine."""
        logger.info("Using Fallback AI Engine (rule-based)")
    
    def generate_study_schedule(
        self,
        subjects: List[str],
        exam_dates: List[str],
        difficulty_levels: List[int],
        daily_hours: float,
        energy_pattern: str,
        stress_level: int,
        sleep_hours: int,
        break_structure: str
    ) -> Tuple[bool, Any]:
        """Generate basic schedule using rules."""
        from study_planner import StudyPlannerEngine
        
        engine = StudyPlannerEngine()
        schedule = engine.create_schedule(
            subjects=subjects,
            difficulty_levels=difficulty_levels,
            daily_hours=daily_hours,
            energy_pattern=energy_pattern,
            break_structure=break_structure
        )
        
        return True, schedule
    
    def analyze_cognitive_load(self, **kwargs) -> Tuple[bool, Any]:
        """Basic cognitive load analysis."""
        from cognitive_analyzer import CognitiveAnalyzer
        
        analyzer = CognitiveAnalyzer()
        analysis = analyzer.analyze(**kwargs)
        
        return True, analysis
    
    def calculate_productivity_score(self, **kwargs) -> Tuple[bool, Any]:
        """Basic productivity score calculation."""
        # Simple weighted average
        score = (
            kwargs.get("schedule_quality", 70) * 0.3 +
            kwargs.get("energy_alignment", 70) * 0.25 +
            kwargs.get("break_structure", 70) * 0.2 +
            (100 - kwargs.get("stress_level", 5) * 5) * 0.15 +
            min(kwargs.get("sleep_hours", 7) * 10, 100) * 0.1
        )
        
        return True, ProductivityScore(
            overall_score=round(score, 1),
            components={},
            improvement_suggestions=["AI enhancement unavailable - using basic scoring"],
            expected_outcomes=[]
        )


def create_ai_engine(api_key: Optional[str] = None) -> Any:
    """
    Factory function to create appropriate AI engine.
    
    Args:
        api_key: Optional API key.
        
    Returns:
        GeminiAIEngine if API key valid, else FallbackAIEngine.
    """
    engine = GeminiAIEngine(api_key)
    
    if engine.is_ready():
        return engine
    else:
        return FallbackAIEngine()
