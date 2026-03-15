# 🧠 NeuroFlow - AI-Powered Adaptive Study Planner

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/neuroflow)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> **Achieve 90%+ scores without burnout**

NeuroFlow is an AI-powered adaptive study planner that creates optimized daily study schedules based on your energy cycles, academic goals, subject difficulty, and exam timelines.

![NeuroFlow Demo](https://via.placeholder.com/800x400/6366F1/FFFFFF?text=NeuroFlow+AI+Study+Planner)

---

## ✨ Features

### 🎯 Core Features
- **Personalized Timetables** - AI-generated daily schedules
- **Deep Work Blocks** - Optimized focus sessions
- **Break Structures** - Pomodoro, 50-10, 90-20 options
- **Subject Rotation** - Weekly planning with variety
- **Weekly Revision** - Built-in review sessions

### 🧠 AI-Powered Analysis
- **Cognitive Load Analysis** - Detects schedule heaviness
- **Burnout Risk Prediction** - Prevents exhaustion
- **Productivity Score** - Measures effectiveness (0-100)
- **Efficiency Prediction** - Forecasts performance
- **Optimization Suggestions** - Personalized recommendations

### 📊 Advanced Features
- **Energy Pattern Matching** - Aligns with your chronotype
- **Stress Level Adjustment** - Adapts to your mental state
- **Sleep Quality Impact** - Factors in rest
- **Difficulty Balancing** - Distributes hard subjects optimally
- **PDF Export** - Download and print your schedule

---

## 🚀 Quick Start

### Option 1: Google Colab (Easiest)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/neuroflow/blob/main/NeuroFlow_Colab.ipynb)

1. Click the badge above
2. Add your Google API Key
3. Run all cells
4. Start planning!

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/neuroflow.git
cd neuroflow

# Install dependencies
pip install -r requirements.txt

# Set your Google API key
export GOOGLE_API_KEY="your_api_key_here"

# Run the application
python main.py
```

### Option 3: Docker (Coming Soon)

```bash
docker pull neuroflow/ai-study-planner
docker run -p 7860:7860 -e GOOGLE_API_KEY=your_key neuroflow/ai-study-planner
```

---

## 📖 Usage Guide

### 1. Enter Your Information

| Field | Description | Example |
|-------|-------------|---------|
| **Subjects** | Your exam subjects | Mathematics, Physics, Chemistry |
| **Exam Dates** | When exams are scheduled | 2024-06-15, 2024-06-20 |
| **Difficulty** | How hard each subject is (1-5) | 5, 4, 3 |
| **Daily Hours** | How long you can study daily | 8 hours |
| **Energy Pattern** | When you're most alert | Morning High |
| **Break Structure** | Preferred work-break cycle | Deep Focus (50-10) |
| **Stress Level** | Current stress (1-10) | 5 |
| **Sleep Hours** | Average sleep per night | 7 hours |

### 2. Generate Your Plan

Click **"🚀 Generate My Study Plan"** and wait 10-20 seconds for AI processing.

### 3. Review & Export

- View your personalized timetable
- Check cognitive analysis and burnout risk
- Review weekly rotation plan
- Export as PDF for printing

---

## 📊 Understanding Your Results

### Productivity Score (0-100)
| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | ⭐⭐⭐⭐⭐ Excellent | Optimal conditions |
| 75-89 | ⭐⭐⭐⭐ Good | Solid study plan |
| 60-74 | ⭐⭐⭐ Average | Room for improvement |
| 40-59 | ⭐⭐ Below Average | Needs adjustment |
| 0-39 | ⭐ Poor | Major changes needed |

### Burnout Risk (%)
| Risk | Color | Action |
|------|-------|--------|
| 0-30% | 🟢 Low | Healthy pace, maintain |
| 31-60% | 🟡 Medium | Monitor stress levels |
| 61-85% | 🟠 High | Reduce study load |
| 86-100% | 🔴 Critical | Immediate intervention |

### Cognitive Load (0-100)
| Load | Status | Recommendation |
|------|--------|----------------|
| 0-50 | 🟢 Manageable | Sustainable long-term |
| 51-70 | 🟡 Elevated | Take regular breaks |
| 71-85 | 🟠 High | Risk of fatigue |
| 86-100 | 🔴 Overload | Schedule too heavy |

---

## 🏗️ Architecture

```
NeuroFlow/
├── config.py              # Configuration & constants
├── ai_engine.py           # Gemini API integration
├── study_planner.py       # Core planning algorithms
├── cognitive_analyzer.py  # Cognitive load analysis
├── pdf_exporter.py        # PDF generation
├── ui.py                  # Gradio interface
├── main.py                # Entry point
├── requirements.txt       # Dependencies
├── SETUP_INSTRUCTIONS.md  # Detailed setup guide
├── MONETIZATION_GUIDE.md  # SaaS business guide
└── NeuroFlow_Colab.ipynb  # Colab notebook
```

### Tech Stack
- **Backend:** Python 3.8+
- **AI:** Google Gemini API
- **UI:** Gradio 4.0+
- **PDF:** ReportLab
- **Architecture:** Modular, scalable

---

## 🔑 Getting API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Set as environment variable: `export GOOGLE_API_KEY="your_key"`

> 💡 **Free Tier:** 60 requests/minute - plenty for personal use!

---

## 🛠️ Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black *.py
```

### Project Structure

```
neuroflow/
├── 📁 core/               # Core business logic
│   ├── study_planner.py
│   ├── cognitive_analyzer.py
│   └── ai_engine.py
├── 📁 ui/                 # User interface
│   └── gradio_interface.py
├── 📁 export/             # Export functionality
│   └── pdf_exporter.py
├── 📁 tests/              # Unit tests
├── 📁 docs/               # Documentation
└── 📁 examples/           # Example schedules
```

---

## 🌟 Roadmap

### Q1 2024 - MVP ✅
- [x] Basic schedule generation
- [x] Cognitive analysis
- [x] PDF export
- [x] Web interface

### Q2 2024 - Enhancement
- [ ] Mobile-responsive PWA
- [ ] Progress tracking dashboard
- [ ] Study reminders
- [ ] Subject material recommendations

### Q3 2024 - AI Features
- [ ] AI tutor chatbot
- [ ] Group study features
- [ ] Performance analytics
- [ ] Goal setting & tracking

### Q4 2024 - Scale
- [ ] Institution dashboard
- [ ] Parent portal
- [ ] Multi-language support
- [ ] API for developers

### 2025 - Expansion
- [ ] Native mobile apps (iOS/Android)
- [ ] Gamification features
- [ ] Tutor marketplace
- [ ] Enterprise features

---

## 💰 Monetization

NeuroFlow can be monetized as a SaaS product:

### Pricing Tiers
- **Free:** Basic scheduling (3 subjects)
- **Pro ($9.99/mo):** Unlimited subjects, full analysis
- **Premium ($19.99/mo):** AI tutor, group features

### Target Markets
- Individual students
- Coaching centers
- Schools & universities
- Corporate training

See [MONETIZATION_GUIDE.md](MONETIZATION_GUIDE.md) for detailed business plan.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Gradio team for the amazing UI framework
- Cognitive science research that informs our algorithms
- Our beta testers and early users

---

## 📞 Support

- **Documentation:** [docs.neuroflow.ai](https://docs.neuroflow.ai)
- **Email:** support@neuroflow.ai
- **Twitter:** [@NeuroFlowAI](https://twitter.com/NeuroFlowAI)
- **Discord:** [Join our community](https://discord.gg/neuroflow)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/neuroflow&type=Date)](https://star-history.com/#yourusername/neuroflow&Date)

---

**Made with ❤️ by NeuroFlow AI Team**

> *"Study smarter, not harder."*

[⬆ Back to Top](#-neuroflow--ai-powered-adaptive-study-planner)
