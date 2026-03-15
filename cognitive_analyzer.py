"""
NeuroFlow - Cognitive Analyzer Module
=====================================
Analyzes cognitive load, burnout risk, and schedule efficiency.
Uses scientific principles from cognitive psychology.
"""

import math
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from config import (
    DIFFICULTY_LEVELS, BURNOUT_THRESHOLDS, PRODUCTIVITY_RANGES,
    get_stress_impact, get_sleep_impact, get_burnout_risk_level
)


@dataclass
class CognitiveMetrics:
    """Cognitive metrics for analysis."""
    total_study_hours: float = 0.0
    consecutive_hours: float = 0.0
    difficult_subject_hours: float = 0.0
    break_ratio: float = 0.0
    peak_utilization: float = 0.0
    variety_index: float = 0.0


@dataclass
class BurnoutIndicators:
    """Burnout risk indicators."""
    high_intensity_ratio: float = 0.0
    insufficient_breaks: bool = False
    sleep_deprivation: bool = False
    chronic_stress: bool = False
    lack_of_variety: bool = False
    unrealistic_load: bool = False


class CognitiveAnalyzer:
    """
    Analyzes study schedules for cognitive load and burnout risk.
    Based on cognitive load theory and attention restoration theory.
    """
    
    # Cognitive load thresholds
    MAX_DAILY_HOURS = 10  # Beyond this, diminishing returns
    MAX_CONSECUTIVE_HOURS = 3  # Before long break needed
    OPTIMAL_BREAK_RATIO = 0.15  # 15% of time should be breaks
    MIN_VARIETY_SUBJECTS = 3  # Minimum subjects per day
    
    def __init__(self):
        """Initialize cognitive analyzer."""
        self.metrics = CognitiveMetrics()
        self.indicators = BurnoutIndicators()
    
    def analyze(
        self,
        schedule: Dict[str, Any],
        stress_level: int,
        sleep_hours: int,
        daily_hours: float,
        energy_pattern: str
    ) -> Dict[str, Any]:
        """
        Perform comprehensive cognitive analysis.
        
        Args:
            schedule: Study schedule dictionary.
            stress_level: User's stress level (1-10).
            sleep_hours: User's sleep hours.
            daily_hours: Daily study hours.
            energy_pattern: User's energy pattern.
            
        Returns:
            Analysis results dictionary.
        """
        # Calculate metrics
        self._calculate_metrics(schedule, daily_hours)
        
        # Identify burnout indicators
        self._identify_burnout_indicators(stress_level, sleep_hours, daily_hours)
        
        # Calculate scores
        cognitive_load = self._calculate_cognitive_load(schedule)
        burnout_risk = self._calculate_burnout_risk(stress_level, sleep_hours)
        efficiency = self._predict_efficiency(stress_level, sleep_hours)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            cognitive_load, burnout_risk, stress_level, sleep_hours
        )
        
        # Generate redistribution suggestions
        redistribution = self._generate_redistribution_suggestions(
            schedule, cognitive_load
        )
        
        # Determine schedule health
        health = self._determine_schedule_health(cognitive_load, burnout_risk)
        
        return {
            "cognitive_load_score": round(cognitive_load, 1),
            "burnout_risk_percentage": round(burnout_risk, 1),
            "efficiency_prediction": round(efficiency, 1),
            "risk_factors": self._get_risk_factors(),
            "recommendations": recommendations,
            "redistribution_suggestions": redistribution,
            "schedule_health": health,
            "metrics": {
                "total_study_hours": round(self.metrics.total_study_hours, 1),
                "break_ratio": round(self.metrics.break_ratio, 2),
                "peak_utilization": round(self.metrics.peak_utilization, 1),
                "variety_index": round(self.metrics.variety_index, 1)
            }
        }
    
    def _calculate_metrics(self, schedule: Dict[str, Any], daily_hours: float) -> None:
        """Calculate cognitive metrics from schedule."""
        daily_schedule = schedule.get("daily_schedule", [])
        
        total_minutes = 0
        study_minutes = 0
        break_minutes = 0
        difficult_minutes = 0
        peak_minutes = 0
        subjects_seen = set()
        
        for slot in daily_schedule:
            duration = slot.get("duration_minutes", 0)
            total_minutes += duration
            
            activity = slot.get("activity", "").lower()
            intensity = slot.get("intensity", "medium")
            subject = slot.get("subject", "")
            
            if "break" not in activity:
                study_minutes += duration
                subjects_seen.add(subject)
                
                if intensity == "high":
                    difficult_minutes += duration
                    peak_minutes += duration
            else:
                break_minutes += duration
        
        self.metrics.total_study_hours = study_minutes / 60
        self.metrics.break_ratio = break_minutes / total_minutes if total_minutes > 0 else 0
        self.metrics.peak_utilization = peak_minutes / study_minutes * 100 if study_minutes > 0 else 0
        self.metrics.variety_index = len(subjects_seen)
    
    def _identify_burnout_indicators(
        self, 
        stress_level: int, 
        sleep_hours: int, 
        daily_hours: float
    ) -> None:
        """Identify potential burnout indicators."""
        self.indicators.high_intensity_ratio = (
            self.metrics.peak_utilization > 60
        )
        self.indicators.insufficient_breaks = (
            self.metrics.break_ratio < 0.1
        )
        self.indicators.sleep_deprivation = sleep_hours < 6
        self.indicators.chronic_stress = stress_level > 7
        self.indicators.lack_of_variety = self.metrics.variety_index < 2
        self.indicators.unrealistic_load = daily_hours > self.MAX_DAILY_HOURS
    
    def _calculate_cognitive_load(self, schedule: Dict[str, Any]) -> float:
        """
        Calculate cognitive load score (0-100).
        
        Based on:
        - Total study hours
        - Difficulty distribution
        - Break adequacy
        - Subject variety
        """
        load_score = 0.0
        
        # Hours factor (diminishing returns after 8 hours)
        hours = self.metrics.total_study_hours
        if hours <= 6:
            hours_factor = hours * 5  # 0-30
        elif hours <= 8:
            hours_factor = 30 + (hours - 6) * 10  # 30-50
        else:
            hours_factor = 50 + (hours - 8) * 8  # 50-100 (accelerating)
        
        load_score += min(hours_factor, 40)
        
        # Intensity factor
        intensity_factor = self.metrics.peak_utilization * 0.3
        load_score += min(intensity_factor, 25)
        
        # Break deficit factor
        optimal_break = self.OPTIMAL_BREAK_RATIO
        actual_break = self.metrics.break_ratio
        if actual_break < optimal_break:
            break_deficit = (optimal_break - actual_break) / optimal_break * 20
            load_score += break_deficit
        
        # Variety factor
        if self.metrics.variety_index < self.MIN_VARIETY_SUBJECTS:
            variety_penalty = (self.MIN_VARIETY_SUBJECTS - self.metrics.variety_index) * 5
            load_score += variety_penalty
        
        return min(load_score, 100)
    
    def _calculate_burnout_risk(
        self, 
        stress_level: int, 
        sleep_hours: int
    ) -> float:
        """
        Calculate burnout risk percentage (0-100).
        
        Based on multiple factors including stress, sleep, and schedule metrics.
        """
        risk_score = 0.0
        
        # Stress contribution (up to 30%)
        stress_factor = get_stress_impact(stress_level)
        if stress_level > 7:
            risk_score += (stress_level - 7) * 10  # 0-30
        
        # Sleep deprivation contribution (up to 25%)
        sleep_factor = get_sleep_impact(sleep_hours)
        if sleep_hours < 7:
            sleep_deficit = (7 - sleep_hours) * 8
            risk_score += sleep_deficit
        
        # Schedule load contribution (up to 30%)
        if self.metrics.total_study_hours > 8:
            overload = (self.metrics.total_study_hours - 8) * 5
            risk_score += min(overload, 30)
        
        # Break inadequacy (up to 15%)
        if self.metrics.break_ratio < 0.1:
            risk_score += 15
        
        return min(risk_score, 100)
    
    def _predict_efficiency(
        self, 
        stress_level: int, 
        sleep_hours: int
    ) -> float:
        """
        Predict study efficiency percentage (0-100).
        
        Based on stress, sleep, and schedule quality.
        """
        base_efficiency = 70.0
        
        # Sleep quality bonus/penalty
        sleep_factor = get_sleep_impact(sleep_hours)
        base_efficiency *= sleep_factor["factor"]
        
        # Stress impact
        stress_factor = get_stress_impact(stress_level)
        base_efficiency *= stress_factor["factor"]
        
        # Break structure bonus
        if self.metrics.break_ratio >= self.OPTIMAL_BREAK_RATIO:
            base_efficiency *= 1.1
        
        # Variety bonus
        if self.metrics.variety_index >= self.MIN_VARIETY_SUBJECTS:
            base_efficiency *= 1.05
        
        return min(base_efficiency, 100)
    
    def _get_risk_factors(self) -> List[str]:
        """Get list of identified risk factors."""
        factors = []
        
        if self.indicators.high_intensity_ratio:
            factors.append("High intensity study ratio (>60%)")
        if self.indicators.insufficient_breaks:
            factors.append("Insufficient break time (<10%)")
        if self.indicators.sleep_deprivation:
            factors.append("Sleep deprivation detected")
        if self.indicators.chronic_stress:
            factors.append("Elevated stress levels")
        if self.indicators.lack_of_variety:
            factors.append("Limited subject variety")
        if self.indicators.unrealistic_load:
            factors.append("Unrealistic daily study load")
        
        return factors if factors else ["No major risk factors identified"]
    
    def _generate_recommendations(
        self,
        cognitive_load: float,
        burnout_risk: float,
        stress_level: int,
        sleep_hours: int
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        # Load-based recommendations
        if cognitive_load > 75:
            recommendations.append(
                "🔴 High cognitive load detected: Reduce daily study hours by 1-2 hours "
                "or spread difficult subjects across more days."
            )
        elif cognitive_load > 60:
            recommendations.append(
                "🟡 Moderate cognitive load: Monitor energy levels and take breaks when needed."
            )
        
        # Burnout risk recommendations
        if burnout_risk > 70:
            recommendations.append(
                "⚠️ High burnout risk: Implement mandatory rest days and reduce study intensity. "
                "Consider speaking with a counselor."
            )
        elif burnout_risk > 50:
            recommendations.append(
                "⚡ Elevated burnout risk: Add more breaks and ensure adequate sleep."
            )
        
        # Sleep recommendations
        if sleep_hours < 6:
            recommendations.append(
                "💤 Critical: Increase sleep to at least 7 hours. Sleep deprivation "
                "severely impacts memory consolidation and cognitive function."
            )
        elif sleep_hours < 7:
            recommendations.append(
                "😴 Try to increase sleep by 30-60 minutes for better performance."
            )
        
        # Stress recommendations
        if stress_level > 8:
            recommendations.append(
                "🧘 High stress detected: Incorporate daily meditation (10-15 min) "
                "and light exercise to manage stress levels."
            )
        
        # Break recommendations
        if self.metrics.break_ratio < 0.15:
            recommendations.append(
                "⏸️ Increase break frequency: Aim for 15% of study time as breaks. "
                "Try the Pomodoro technique (25-5)."
            )
        
        # Variety recommendations
        if self.metrics.variety_index < 3:
            recommendations.append(
                "📚 Increase subject variety: Studying 3+ subjects per day improves "
                "retention and prevents mental fatigue."
            )
        
        if not recommendations:
            recommendations.append(
                "✅ Your schedule looks well-balanced! Maintain current habits."
            )
        
        return recommendations
    
    def _generate_redistribution_suggestions(
        self,
        schedule: Dict[str, Any],
        cognitive_load: float
    ) -> List[Dict[str, str]]:
        """Generate schedule redistribution suggestions."""
        suggestions = []
        
        daily_schedule = schedule.get("daily_schedule", [])
        
        # Find consecutive long sessions
        consecutive_hard = 0
        last_was_hard = False
        
        for slot in daily_schedule:
            intensity = slot.get("intensity", "medium")
            if intensity == "high":
                if last_was_hard:
                    consecutive_hard += 1
                last_was_hard = True
            else:
                last_was_hard = False
        
        if consecutive_hard > 2:
            suggestions.append({
                "from": "Consecutive hard subjects",
                "to": "Interleave with easier subjects",
                "reason": "Prevents cognitive overload and maintains focus"
            })
        
        # Check for long sessions without breaks
        long_sessions = [
            slot for slot in daily_schedule 
            if slot.get("duration_minutes", 0) > 90 and "break" not in slot.get("activity", "").lower()
        ]
        
        if long_sessions:
            suggestions.append({
                "from": f"{len(long_sessions)} sessions >90 minutes",
                "to": "Split into 50-60 minute blocks",
                "reason": "Shorter sessions with breaks improve retention"
            })
        
        # Suggest redistribution if load is uneven
        if cognitive_load > 70:
            suggestions.append({
                "from": "Heavy daily load",
                "to": "Spread across 6-7 days with lighter sessions",
                "reason": "Distributed practice is more effective than cramming"
            })
        
        return suggestions
    
    def _determine_schedule_health(
        self, 
        cognitive_load: float, 
        burnout_risk: float
    ) -> str:
        """Determine overall schedule health rating."""
        avg_score = (cognitive_load + burnout_risk) / 2
        
        if avg_score < 30:
            return "excellent"
        elif avg_score < 50:
            return "good"
        elif avg_score < 65:
            return "fair"
        elif avg_score < 80:
            return "poor"
        else:
            return "critical"


def quick_analyze(
    daily_hours: float,
    stress_level: int,
    sleep_hours: int,
    subjects_count: int = 4
) -> Dict[str, Any]:
    """
    Quick analysis without full schedule.
    
    Args:
        daily_hours: Daily study hours.
        stress_level: Stress level (1-10).
        sleep_hours: Sleep hours.
        subjects_count: Number of subjects.
        
    Returns:
        Quick analysis results.
    """
    analyzer = CognitiveAnalyzer()
    
    # Create minimal schedule for analysis
    minimal_schedule = {
        "daily_schedule": [
            {"duration_minutes": int(daily_hours * 60 * 0.85), "intensity": "medium", "activity": "study"},
            {"duration_minutes": int(daily_hours * 60 * 0.15), "intensity": "low", "activity": "break"}
        ]
    }
    
    return analyzer.analyze(
        schedule=minimal_schedule,
        stress_level=stress_level,
        sleep_hours=sleep_hours,
        daily_hours=daily_hours,
        energy_pattern="morning_high"
    )
