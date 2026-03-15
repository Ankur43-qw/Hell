import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyDYw22EodIk_pzkV6MG0YYZ_9DECN1OeXo"

import gradio as gr

# Energy patterns
ENERGY_PATTERNS = {
    "morning_high": {"name": "Morning High", "peak": [6, 7, 8, 9, 10, 11]},
    "afternoon_high": {"name": "Afternoon High", "peak": [12, 13, 14, 15, 16, 17]},
    "night_high": {"name": "Night Owl", "peak": [20, 21, 22, 23, 0, 1]},
    "bimodal": {"name": "Bimodal", "peak": [7, 8, 9, 19, 20, 21]},
}

def generate_schedule(subjects, exam_date, daily_hours, energy_pattern):
    subjects_list = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subjects_list:
        subjects_list = ["Study"]
    
    energy = ENERGY_PATTERNS.get(energy_pattern, ENERGY_PATTERNS["morning_high"])
    peak_hours = energy["peak"][:3]
    
    schedule = []
    deep_work = []
    
    start_hour = 8 if energy_pattern == "morning_high" else 12 if energy_pattern == "afternoon_high" else 20 if energy_pattern == "night_high" else 9
    current_hour = start_hour
    total_minutes = int(daily_hours * 60)
    elapsed = 0
    session_num = 0
    
    while elapsed < total_minutes:
        work_duration = 90 if current_hour in peak_hours else 50
        if elapsed + work_duration > total_minutes:
            work_duration = total_minutes - elapsed
        
        subject = subjects_list[session_num % len(subjects_list)]
        end_hour = current_hour + work_duration // 60
        end_min = work_duration % 60
        time_str = f"{current_hour:02d}:00-{end_hour:02d}:{end_min:02d}"
        
        schedule.append({"time": time_str, "subject": subject, "type": "deep_work" if current_hour in peak_hours else "study", "duration": work_duration})
        
        if current_hour in peak_hours:
            deep_work.append({"time": time_str, "subject": subject, "technique": "Deep Focus"})
        
        elapsed += work_duration
        current_hour = end_hour
        session_num += 1
        
        if elapsed < total_minutes:
            break_duration = 15 if session_num % 4 == 0 else 10
            if elapsed + break_duration > total_minutes:
                break_duration = total_minutes - elapsed
            end_hour = current_hour + break_duration // 60
            end_min = break_duration % 60
            schedule.append({"time": f"{current_hour:02d}:00-{end_hour:02d}:{end_min:02d}", "subject": "Break", "type": "break", "duration": break_duration})
            elapsed += break_duration
            current_hour = end_hour
    
    burnout = min(100, int((daily_hours / 10) * 40 + len(subjects_list) * 5))
    productivity = max(40, min(95, int(100 - burnout * 0.5 + daily_hours * 2)))
    
    html = f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #f3f4f6, #e5e7eb); padding: 20px; border-radius: 12px; text-align: center;">
            <div style="font-size: 2.5rem; font-weight: bold; color: {'#10b981' if productivity >= 75 else '#f59e0b' if productivity >= 60 else '#ef4444'};">{productivity}</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Productivity Score</div>
        </div>
        <div style="background: linear-gradient(135deg, #f3f4f6, #e5e7eb); padding: 20px; border-radius: 12px; text-align: center;">
            <div style="font-size: 2.5rem; font-weight: bold; color: {'#10b981' if burnout < 40 else '#f59e0b' if burnout < 70 else '#ef4444'};">{burnout}%</div>
            <div style="color: #6b7280; font-size: 0.875rem;">Burnout Risk</div>
        </div>
    </div>
    <div style="border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
    """
    
    for item in schedule:
        bg = "#f3f4f6" if item["type"] == "break" else "#fef3c7" if item["type"] == "deep_work" else "#ffffff"
        border = "#d1d5db" if item["type"] == "break" else "#f59e0b" if item["type"] == "deep_work" else "#4f46e5"
        emoji = "☕" if item["type"] == "break" else "🎯" if item["type"] == "deep_work" else "📖"
        html += f"""<div style="display: flex; padding: 12px; background: {bg}; border-left: 4px solid {border}; border-bottom: 1px solid #e5e7eb;">
            <div style="width: 100px; font-weight: 600; color: #4f46e5;">{item['time']}</div>
            <div style="flex: 1;"><span style="font-weight: 500;">{emoji} {item['subject']}</span> <span style="color: #6b7280; font-size: 0.875rem;">({item['duration']} min)</span></div>
        </div>"""
    
    html += "</div>"
    
    if deep_work:
        html += """<div style="margin-top: 20px;"><h4 style="color: #4f46e5;">🎯 Deep Work Blocks</h4><div style="background: #fef3c7; padding: 16px; border-radius: 8px;">"""
        for block in deep_work:
            html += f"""<div style="margin-bottom: 8px; padding: 8px; background: white; border-radius: 4px;"><strong>{block['time']}</strong> - {block['subject']}</div>"""
        html += "</div></div>"
    
    return html

with gr.Blocks(title="NeuroFlow - AI Study Planner") as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border-radius: 16px; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">🧠 NeuroFlow</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">AI-Powered Adaptive Study Planner</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Your Information")
            subjects = gr.Textbox(label="Subjects", placeholder="Math, Physics, Chemistry")
            exam_date = gr.Textbox(label="Exam Date", placeholder="2024-06-15")
            daily_hours = gr.Slider(label="Daily Hours", minimum=1, maximum=12, value=6, step=0.5)
            energy = gr.Dropdown(label="Energy Pattern", choices=list(ENERGY_PATTERNS.keys()), value="morning_high")
            btn = gr.Button("🚀 Generate Plan", variant="primary")
        
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Your Plan")
            output = gr.HTML()
    
    btn.click(fn=generate_schedule, inputs=[subjects, exam_date, daily_hours, energy], outputs=output)

if __name__ == "__main__":
    demo.launch()
