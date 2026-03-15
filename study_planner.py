"""
NeuroFlow - Study Planner Engine
================================
Core study planning algorithms and schedule generation logic.
Works independently or with AI enhancement.
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

from config import (
    ENERGY_PATTERNS, DIFFICULTY_LEVELS, BREAK_STRUCTURES,
    get_stress_impact, get_sleep_impact
)


@dataclass
class TimeSlot:
    """Represents a time slot in the schedule."""
    start_time: str  # HH:MM format
    end_time: str
    duration_minutes: int
    subject: Optional[str] = None
    activity_type: str = "study"  # study, review, break, deep_work
    intensity: str = "medium"  # high, medium, low


@dataclass
class DailySchedule:
    """Represents a full day's schedule."""
    date: str
    slots: List[TimeSlot] = field(default_factory=list)
    total_study_minutes: int = 0
    total_break_minutes: int = 0
    deep_work_blocks: int = 0


@dataclass
class SubjectAllocation:
    """Tracks subject time allocation."""
    subject: str
    difficulty: int
    exam_date: Optional[str] = None
    allocated_hours: float = 0.0
    priority_score: float = 0.0


class StudyPlannerEngine:
    """
    Core study planning engine using cognitive science principles.
    Creates optimized schedules based on user inputs.
    """
    
    def __init__(self):
        """Initialize the study planner engine."""
        self.subjects: List[SubjectAllocation] = []
        self.energy_pattern: Dict[str, Any] = {}
        self.daily_hours: float = 8.0
        self.break_structure: Tuple[int, int] = (50, 10)
        self.stress_factor: float = 1.0
        self.sleep_factor: float = 1.0
    
    def setup(
        self,
        subjects: List[str],
        difficulty_levels: List[int],
        exam_dates: Optional[List[str]] = None,
        daily_hours: float = 8.0,
        energy_pattern_key: str = "morning_high",
        break_structure_name: str = "Deep Focus (50-10)",
        stress_level: int = 5,
        sleep_hours: int = 7
    ) -> None:
        """
        Setup the planner with user inputs.
        
        Args:
            subjects: List of subject names.
            difficulty_levels: Difficulty level (1-5) for each subject.
            exam_dates: Optional exam dates for each subject.
            daily_hours: Daily available study hours.
            energy_pattern_key: Key for energy pattern.
            break_structure_name: Name of break structure.
            stress_level: Stress level (1-10).
            sleep_hours: Sleep hours per night.
        """
        # Initialize subjects with priorities
        self.subjects = []
        for i, subject in enumerate(subjects):
            difficulty = difficulty_levels[i] if i < len(difficulty_levels) else 3
            exam_date = exam_dates[i] if exam_dates and i < len(exam_dates) else None
            
            # Calculate priority score based on difficulty and exam proximity
            priority = self._calculate_priority(difficulty, exam_date)
            
            self.subjects.append(SubjectAllocation(
                subject=subject,
                difficulty=difficulty,
                exam_date=exam_date,
                priority_score=priority
            ))
        
        # Sort by priority (highest first)
        self.subjects.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Set energy pattern
        self.energy_pattern = ENERGY_PATTERNS.get(
            energy_pattern_key, 
            ENERGY_PATTERNS["morning_high"]
        )
        
        # Set daily hours with stress/sleep adjustments
        self.daily_hours = daily_hours
        self.stress_factor = get_stress_impact(stress_level)["factor"]
        self.sleep_factor = get_sleep_impact(sleep_hours)["factor"]
        
        # Adjust effective hours based on stress and sleep
        self.effective_hours = daily_hours * self.stress_factor * self.sleep_factor
        
        # Set break structure
        self.break_structure = BREAK_STRUCTURES.get(
            break_structure_name,
            BREAK_STRUCTURES["Deep Focus (50-10)"]
        )
    
    def _calculate_priority(self, difficulty: int, exam_date: Optional[str]) -> float:
        """
        Calculate subject priority score.
        
        Args:
            difficulty: Subject difficulty (1-5).
            exam_date: Optional exam date string.
            
        Returns:
            Priority score (higher = more urgent).
        """
        base_priority = difficulty * 20  # 20-100 based on difficulty
        
        if exam_date:
            try:
                exam = datetime.strptime(exam_date, "%Y-%m-%d")
                today = datetime.now()
                days_until = (exam - today).days
                
                if days_until > 0:
                    # Urgency factor: closer exams get higher priority
                    urgency = max(0, (30 - days_until) * 2)
                    base_priority += urgency
            except ValueError:
                pass
        
        return base_priority
    
    def _get_peak_hours(self) -> List[int]:
        """Get peak energy hours based on pattern."""
        return self.energy_pattern.get("peak_hours", [9, 10, 11, 20, 21])
    
    def _get_dip_hours(self) -> List[int]:
        """Get low energy hours based on pattern."""
        return self.energy_pattern.get("dip_hours", [14, 15, 16])
    
    def _is_peak_hour(self, hour: int) -> bool:
        """Check if hour is during peak energy."""
        return hour in self._get_peak_hours()
    
    def _is_dip_hour(self, hour: int) -> bool:
        """Check if hour is during energy dip."""
        return hour in self._get_dip_hours()
    
    def _get_optimal_subject_for_hour(self, hour: int, 
                                       used_subjects: List[str]) -> Optional[SubjectAllocation]:
        """
        Get the best subject for a given hour based on energy and difficulty.
        
        Args:
            hour: Hour of day (0-23).
            used_subjects: Subjects already used today.
            
        Returns:
            Best subject allocation or None.
        """
        available = [s for s in self.subjects if s.subject not in used_subjects]
        
        if not available:
            available = self.subjects  # Reset if all used
        
        if self._is_peak_hour(hour):
            # Peak hours: hardest subjects
            return max(available, key=lambda x: x.difficulty)
        elif self._is_dip_hour(hour):
            # Dip hours: easier subjects or review
            easier = [s for s in available if s.difficulty <= 3]
            if easier:
                return random.choice(easier)
            return min(available, key=lambda x: x.difficulty)
        else:
            # Normal hours: balanced approach
            return available[0] if available else self.subjects[0]
    
    def _generate_time_slots(self, start_hour: int = 8) -> List[TimeSlot]:
        """
        Generate time slots for a day.
        
        Args:
            start_hour: Hour to start studying.
            
        Returns:
            List of time slots.
        """
        slots = []
        current_hour = start_hour
        used_subjects = []
        work_minutes, break_minutes = self.break_structure
        
        total_minutes = int(self.effective_hours * 60)
        elapsed_minutes = 0
        session_count = 0
        
        while elapsed_minutes < total_minutes:
            # Work session
            subject_alloc = self._get_optimal_subject_for_hour(current_hour, used_subjects)
            
            if subject_alloc:
                used_subjects.append(subject_alloc.subject)
                subject_alloc.allocated_hours += work_minutes / 60
            
            start_time = f"{current_hour:02d}:00"
            end_hour = current_hour + (work_minutes // 60)
            end_minute = work_minutes % 60
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            
            intensity = "high" if self._is_peak_hour(current_hour) else "medium"
            
            slots.append(TimeSlot(
                start_time=start_time,
                end_time=end_time,
                duration_minutes=work_minutes,
                subject=subject_alloc.subject if subject_alloc else "Review",
                activity_type="deep_work" if self._is_peak_hour(current_hour) else "study",
                intensity=intensity
            ))
            
            elapsed_minutes += work_minutes
            current_hour = end_hour
            session_count += 1
            
            # Add break if not last session
            if elapsed_minutes < total_minutes:
                break_start = end_time
                break_end_hour = current_hour + (break_minutes // 60)
                break_end_minute = break_minutes % 60
                break_end = f"{break_end_hour:02d}:{break_end_minute:02d}"
                
                slots.append(TimeSlot(
                    start_time=break_start,
                    end_time=break_end,
                    duration_minutes=break_minutes,
                    activity_type="break",
                    intensity="low"
                ))
                
                elapsed_minutes += break_minutes
                current_hour = break_end_hour
                
                # Long break every 4 sessions
                if session_count % 4 == 0:
                    long_break = 20
                    long_break_end_hour = current_hour + (long_break // 60)
                    long_break_end = f"{long_break_end_hour:02d}:00"
                    
                    slots.append(TimeSlot(
                        start_time=break_end,
                        end_time=long_break_end,
                        duration_minutes=long_break,
                        activity_type="break",
                        intensity="low"
                    ))
                    
                    elapsed_minutes += long_break
                    current_hour = long_break_end_hour
        
        return slots
    
    def create_daily_schedule(self, date: Optional[str] = None) -> DailySchedule:
        """
        Create a schedule for one day.
        
        Args:
            date: Date string (YYYY-MM-DD).
            
        Returns:
            DailySchedule object.
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        slots = self._generate_time_slots()
        
        study_minutes = sum(s.duration_minutes for s in slots if s.activity_type != "break")
        break_minutes = sum(s.duration_minutes for s in slots if s.activity_type == "break")
        deep_work = sum(1 for s in slots if s.activity_type == "deep_work")
        
        return DailySchedule(
            date=date,
            slots=slots,
            total_study_minutes=study_minutes,
            total_break_minutes=break_minutes,
            deep_work_blocks=deep_work
        )
    
    def create_weekly_schedule(self) -> List[DailySchedule]:
        """
        Create a schedule for the entire week.
        
        Returns:
            List of DailySchedule objects.
        """
        weekly_schedule = []
        today = datetime.now()
        
        for i in range(7):
            date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            daily = self.create_daily_schedule(date)
            weekly_schedule.append(daily)
        
        return weekly_schedule
    
    def get_subject_rotation(self) -> List[Dict[str, Any]]:
        """
        Generate subject rotation plan for the week.
        
        Returns:
            List of daily rotation plans.
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        rotation = []
        
        for i, day in enumerate(days):
            # Rotate subjects throughout the week
            rotated = self.subjects[i:] + self.subjects[:i]
            
            rotation.append({
                "day": day,
                "morning_subject": rotated[0].subject if len(rotated) > 0 else "Review",
                "afternoon_subject": rotated[1].subject if len(rotated) > 1 else "Practice",
                "evening_subject": rotated[2].subject if len(rotated) > 2 else "Light Review"
            })
        
        return rotation
    
    def get_weekly_revision_plan(self) -> Dict[str, Any]:
        """
        Generate weekly revision plan.
        
        Returns:
            Revision plan dictionary.
        """
        # Use Sunday for revision
        revision_subjects = [s.subject for s in self.subjects[:3]]
        
        return {
            "day": "Sunday",
            "duration_hours": min(3, self.daily_hours * 0.3),
            "subjects_to_review": revision_subjects,
            "focus_areas": ["Weak topics", "Previous mistakes", "Key concepts"]
        }
    
    def create_schedule(
        self,
        subjects: List[str],
        difficulty_levels: List[int],
        daily_hours: float,
        energy_pattern: str,
        break_structure: str,
        exam_dates: Optional[List[str]] = None,
        stress_level: int = 5,
        sleep_hours: int = 7
    ) -> Dict[str, Any]:
        """
        Main method to create complete study schedule.
        
        Args:
            subjects: List of subject names.
            difficulty_levels: Difficulty for each subject.
            daily_hours: Daily available hours.
            energy_pattern: Energy pattern key.
            break_structure: Break structure name.
            exam_dates: Optional exam dates.
            stress_level: Stress level (1-10).
            sleep_hours: Sleep hours.
            
        Returns:
            Complete schedule dictionary.
        """
        # Setup planner
        self.setup(
            subjects=subjects,
            difficulty_levels=difficulty_levels,
            exam_dates=exam_dates,
            daily_hours=daily_hours,
            energy_pattern_key=energy_pattern,
            break_structure_name=break_structure,
            stress_level=stress_level,
            sleep_hours=sleep_hours
        )
        
        # Generate daily schedule
        daily = self.create_daily_schedule()
        
        # Generate weekly rotation
        rotation = self.get_subject_rotation()
        
        # Generate revision plan
        revision = self.get_weekly_revision_plan()
        
        # Extract deep work blocks
        deep_work = [
            {
                "start_time": slot.start_time,
                "duration_hours": round(slot.duration_minutes / 60, 2),
                "subject": slot.subject,
                "focus_technique": "Pomodoro" if self.break_structure[0] <= 25 else "Deep Work"
            }
            for slot in daily.slots
            if slot.activity_type == "deep_work"
        ]
        
        # Generate optimization notes
        notes = self._generate_optimization_notes()
        
        return {
            "daily_schedule": [
                {
                    "time": f"{slot.start_time} - {slot.end_time}",
                    "subject": slot.subject or "Break",
                    "activity": slot.activity_type.replace("_", " ").title(),
                    "duration_minutes": slot.duration_minutes,
                    "intensity": slot.intensity
                }
                for slot in daily.slots
            ],
            "deep_work_blocks": deep_work,
            "break_structure": {
                "type": break_structure,
                "work_duration": self.break_structure[0],
                "break_duration": self.break_structure[1],
                "long_break_every": 4
            },
            "subject_rotation": rotation,
            "weekly_revision": revision,
            "optimization_notes": notes
        }
    
    def _generate_optimization_notes(self) -> List[str]:
        """Generate optimization notes based on schedule."""
        notes = []
        
        # Energy alignment note
        peak_hours = len(self._get_peak_hours())
        notes.append(
            f"📊 Schedule optimized for {self.energy_pattern['name']} "
            f"with {peak_hours} peak hours utilized"
        )
        
        # Difficulty distribution
        hard_subjects = [s for s in self.subjects if s.difficulty >= 4]
        if hard_subjects:
            notes.append(
                f"🎯 Difficult subjects ({', '.join(s.subject for s in hard_subjects[:2])}) "
                f"scheduled during peak energy hours"
            )
        
        # Break structure note
        work_min, break_min = self.break_structure
        notes.append(
            f"⏱️ Using {work_min}-{break_min} work-break cycle for optimal focus"
        )
        
        # Effective hours note
        if self.effective_hours < self.daily_hours:
            notes.append(
                f"⚠️ Effective study capacity: {self.effective_hours:.1f}h "
                f"(adjusted for stress/sleep factors)"
            )
        
        return notes


def create_sample_schedule() -> Dict[str, Any]:
    """Create a sample schedule for testing."""
    engine = StudyPlannerEngine()
    
    return engine.create_schedule(
        subjects=["Mathematics", "Physics", "Chemistry", "English"],
        difficulty_levels=[5, 4, 3, 2],
        daily_hours=8,
        energy_pattern="morning_high",
        break_structure="Deep Focus (50-10)",
        exam_dates=["2024-06-15", "2024-06-20", "2024-06-25", "2024-06-18"],
        stress_level=5,
        sleep_hours=7
    )
