# NeuroFlow - Setup Instructions

## 🚀 Quick Start Guide

Get your AI-powered study planner running in 5 minutes!

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google account (for API key)
- Internet connection

---

## 🔑 Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)

> 💡 **Note:** The Gemini API has a generous free tier (60 requests/minute)

---

## 💻 Step 2: Installation

### Option A: Local Installation

```bash
# 1. Clone or download the NeuroFlow files
cd neuroflow

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your API key
# On Windows:
set GOOGLE_API_KEY=your_api_key_here
# On macOS/Linux:
export GOOGLE_API_KEY=your_api_key_here

# 6. Run the application
python main.py
```

### Option B: Google Colab (Recommended for Beginners)

```python
# 1. Upload all NeuroFlow files to Colab

# 2. Install dependencies
!pip install -q gradio google-generativeai reportlab

# 3. Set your API key
import os
os.environ['GOOGLE_API_KEY'] = 'your_api_key_here'

# 4. Run the application
!python main.py
```

---

## 🌐 Step 3: Access the Web Interface

After running `main.py`, you'll see output like:

```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxx.gradio.live
```

- **Local access:** Open `http://127.0.0.1:7860` in your browser
- **Public access:** Use the Gradio link (works from any device)

---

## 📝 Usage Guide

### 1. Enter Your Information

| Field | Description | Example |
|-------|-------------|---------|
| **Subjects** | Your exam subjects | Mathematics, Physics, Chemistry |
| **Exam Dates** | When exams are scheduled | 2024-06-15, 2024-06-20 |
| **Difficulty** | How hard each subject is (1-5) | 5, 4, 3 |
| **Daily Hours** | How long you can study daily | 8 hours |
| **Energy Pattern** | When you're most alert | Morning High |
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

## 🔧 Troubleshooting

### Issue: "Module not found" error

```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: "API key invalid" error

```bash
# Solution: Check your API key
# 1. Verify key is copied correctly
# 2. Ensure key is set in environment
# 3. Try regenerating key at makersuite.google.com
```

### Issue: "Rate limit exceeded"

```bash
# Solution: Wait 1 minute and retry
# Free tier: 60 requests/minute limit
```

### Issue: PDF export fails

```bash
# Solution: Install reportlab
pip install reportlab
```

---

## 🎯 Tips for Best Results

1. **Be honest about stress/sleep** - The AI adjusts recommendations based on this
2. **Use realistic daily hours** - Overestimating leads to burnout
3. **Update regularly** - Regenerate as exam dates approach
4. **Follow the schedule** - Consistency beats intensity

---

## 📊 Understanding Your Results

### Productivity Score (0-100)
- **90-100:** Excellent - Optimal conditions
- **75-89:** Good - Solid study plan
- **60-74:** Average - Room for improvement
- **Below 60:** Needs adjustment

### Burnout Risk (%)
- **0-30%:** Low risk - Healthy pace
- **31-60%:** Medium - Monitor stress
- **61-85%:** High - Reduce load
- **86-100%:** Critical - Immediate action needed

### Cognitive Load (0-100)
- **0-50:** Manageable - Sustainable long-term
- **51-70:** Elevated - Take regular breaks
- **71-85:** High - Risk of fatigue
- **86-100:** Overload - Schedule too heavy

---

## 🆘 Getting Help

1. Check the [FAQ](#faq) below
2. Review error messages carefully
3. Try the CLI demo: `python main.py --demo`
4. Enable debug mode in the code

---

## ❓ FAQ

**Q: Is my data safe?**
A: Yes! All processing happens locally. Only schedule generation uses Google's API.

**Q: Can I use without API key?**
A: Yes! The app works in "fallback mode" with basic rule-based scheduling.

**Q: How accurate is the AI?**
A: The AI uses cognitive science principles. Results improve with accurate inputs.

**Q: Can I customize the schedule?**
A: Currently, regenerate with different inputs. Manual editing coming soon!

**Q: Does it work for all exam types?**
A: Yes! Works for school, college, competitive, and professional exams.

---

## 🎓 For Educators

NeuroFlow can be used for:
- Student counseling sessions
- Study skills workshops
- Academic coaching
- Mental health awareness

Contact us for institutional licenses.

---

## 📞 Support

- **Email:** support@neuroflow.ai
- **Website:** www.neuroflow.ai
- **Documentation:** docs.neuroflow.ai

---

**Ready to achieve 90%+ without burnout? Let's go! 🚀**
