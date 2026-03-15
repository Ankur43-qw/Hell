"""
NeuroFlow - Main Entry Point
============================
AI-Powered Adaptive Study Planner

This is the main entry point for the NeuroFlow application.
Run this file to start the web interface.

Usage:
    python main.py
    
Or in Google Colab:
    !python main.py
"""

import os
import sys
import argparse
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import NeuroFlow modules
from config import APP_NAME, APP_VERSION, APP_DESCRIPTION, GOOGLE_API_KEY
from ui import launch_app, NeuroFlowUI


def print_banner() -> None:
    """Print application banner."""
    banner = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🧠 {APP_NAME:<52} ║
    ║   {APP_TAGLINE:<54} ║
    ║   Version {APP_VERSION:<47} ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies() -> bool:
    """
    Check if all required dependencies are installed.
    
    Returns:
        True if all dependencies are available, False otherwise.
    """
    required_packages = [
        "gradio",
        "google-generativeai",
        "reportlab",
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            if package == "google-generativeai":
                __import__("google.generativeai")
            elif package == "reportlab":
                __import__("reportlab")
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with: pip install -r requirements.txt")
        return False
    
    return True


def check_api_key() -> bool:
    """
    Check if Google API key is configured.
    
    Returns:
        True if API key is set, False otherwise.
    """
    if not GOOGLE_API_KEY:
        print("\n⚠️  Warning: GOOGLE_API_KEY not found in environment variables.")
        print("   The app will run in fallback mode (basic features only).")
        print("   For full AI features, set your API key:")
        print("   export GOOGLE_API_KEY='your_api_key_here'")
        print("   Get your key from: https://makersuite.google.com/app/apikey\n")
        return False
    
    print("✅ Google API Key configured")
    return True


def run_cli_demo() -> None:
    """Run a command-line demo of the study planner."""
    print("\n🎯 Running CLI Demo...\n")
    
    from study_planner import StudyPlannerEngine
    from cognitive_analyzer import CognitiveAnalyzer
    
    # Sample data
    subjects = ["Mathematics", "Physics", "Chemistry", "English"]
    difficulties = [5, 4, 3, 2]
    exam_dates = ["2024-06-15", "2024-06-20", "2024-06-25", "2024-06-18"]
    
    # Create schedule
    engine = StudyPlannerEngine()
    schedule = engine.create_schedule(
        subjects=subjects,
        difficulty_levels=difficulties,
        exam_dates=exam_dates,
        daily_hours=8,
        energy_pattern="morning_high",
        break_structure="Deep Focus (50-10)",
        stress_level=5,
        sleep_hours=7
    )
    
    # Analyze
    analyzer = CognitiveAnalyzer()
    analysis = analyzer.analyze(
        schedule=schedule,
        stress_level=5,
        sleep_hours=7,
        daily_hours=8,
        energy_pattern="morning_high"
    )
    
    # Display results
    print("=" * 60)
    print("📅 SAMPLE STUDY SCHEDULE")
    print("=" * 60)
    
    print("\n🕐 Daily Timetable:")
    for slot in schedule.get("daily_schedule", [])[:6]:
        print(f"   {slot['time']}: {slot['subject']} ({slot['activity']})")
    print("   ...")
    
    print("\n📊 Metrics:")
    print(f"   Cognitive Load: {analysis['cognitive_load_score']:.1f}/100")
    print(f"   Burnout Risk: {analysis['burnout_risk_percentage']:.1f}%")
    print(f"   Efficiency: {analysis['efficiency_prediction']:.1f}%")
    
    print("\n💡 Recommendations:")
    for rec in analysis.get("recommendations", [])[:3]:
        print(f"   • {rec}")
    
    print("\n✅ Demo completed successfully!")


def main() -> None:
    """Main entry point."""
    global APP_TAGLINE
    APP_TAGLINE = "AI-Powered Adaptive Study Planner"
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} - {APP_TAGLINE}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch web UI
  python main.py --demo             # Run CLI demo
  python main.py --port 7860        # Launch on specific port
  python main.py --no-share         # Don't create public link
        """
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run CLI demo instead of web UI"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Server port (default: auto)"
    )
    
    parser.add_argument(
        "--no-share",
        action="store_true",
        help="Don't create public shareable link"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run demo or web UI
    if args.demo:
        run_cli_demo()
    else:
        # Check API key (optional)
        check_api_key()
        
        # Launch web UI
        print(f"\n🚀 Starting {APP_NAME} web interface...\n")
        
        try:
            launch_app(
                share=not args.no_share,
                server_port=args.port
            )
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error starting application: {e}")
            print(f"\n❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
