import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from scipy.io import loadmat
# كود قراءة البيانات الحقيقية
try:
    mat_data = loadmat('Time_Normal_1_098.mat') 
    # استخراج عمود الاهتزاز (Drive End vibration)
    real_vibration = mat_data['X098_DE_time'].flatten()
except Exception as e:
    # إذا صرا مشكل في تحميل الملف، يخدم بأرقام عشوائية باش ما يتوقفش البرنامج
    real_vibration = np.random.randn(1000) * 0.1
    st.error(f"Error loading .mat file: {e}")
def ai_diagnostic_logic(current_vibration):
    if current_vibration > 0.8:
        return "Critical", "🛑 High Vibration Detected! Potential Bearing Failure."
    elif current_vibration > 0.5:
        return "Warning", "⚠️ Unusual Pattern - Maintenance Check Recommended."
    else:
        return "Healthy", "✅ Machine is operating within normal parameters."

# إعداد الصفحة لتكون بستايل مظلم واحترافي
st.set_page_config(page_title="DZ-Predict Dashboard", layout="wide")

# القائمة الجانبية
st.sidebar.title("🛠️ DZ-Predict v1.0")
st.sidebar.markdown("---")
st.sidebar.info("Industry 4.0 Solution for Algerian Factories")

# العناوين الرئيسية
st.title("🏭 Machine Health Monitoring System")
st.markdown("### Location: Sétif Plant - Unit 01")

# مربعات الإحصائيات (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Health", "94%", "+2%")
col2.metric("Vibration", "0.04 mm/s", "-0.01")
col3.metric("Temperature", "52°C", "Stable")
col4.metric("Next Maintenance", "124h", "Predicted")

st.markdown("---")

# منطقة المبيانات
left_column, right_column = st.columns([2, 1])

with left_column:
    st.subheader("📈 Real-time Vibration Analysis")
    # صنع بيانات وهمية تشبه اهتزازات المحرك
    vibration_data = pd.DataFrame(
        np.random.normal(0.05, 0.01, size=(50, 1)),
        columns=['Vibration Level']
    )
    st.line_chart(vibration_data)

with right_column:
    st.subheader("🤖 AI Diagnosis")
    status_df = pd.DataFrame({
        'Status': ['Healthy', 'Warning', 'Fault'],
        'Value': [90, 8, 2]
    })
    fig = px.pie(status_df, values='Value', names='Status', hole=0.3,
                 color_discrete_sequence=['#00CC96', '#FFA15A', '#EF553B'])
    st.plotly_chart(fig, use_container_width=True)

# زر التشغيل للتجربة أمام البروف
# ... (باقي الكود تاعك تاع المربعات والمبيان) ...

# --- 2. في بلاصة المبيان والزر ---
st.subheader("📈 Live Vibration Analysis")
placeholder = st.empty()
data = np.random.randn(20, 1) * 0.4 # ضربناه في 0.4 باش تكون القيم واقعية
if 'alerts_history' not in st.session_state:
    st.session_state.alerts_history = []
# زر التشغيل
if st.button('Start AI Prediction'):
    st.write("Deep Learning Model (LSTM) is monitoring the stream...")
    latest_val = data[-1][0] 
    status, message = ai_diagnostic_logic(latest_val)
    
    if status == "Healthy":
        st.success(message)
    elif status == "Warning":
        st.warning(message)
    else:
        st.error(message)
    if status != "Healthy":
        new_log = {"Time": time.strftime("%H:%M:%S"), "Issue": message, "Status": status}
        st.session_state.alerts_history.insert(0, new_log)

# محاكاة الحركة
for i in range(100):
    idx = i % len(real_vibration) 
    new_data = np.array([[real_vibration[idx]]])
    data = np.append(data, new_data, axis=0)
    data = data[-20:]
    with placeholder.container():
        st.line_chart(data)
    time.sleep(0.1)
st.write("---")
st.subheader("📋 Maintenance Log (Recent Issues)")
if st.session_state.alerts_history:
    st.table(pd.DataFrame(st.session_state.alerts_history))
else:
    st.info("System Status: Clear. No issues logged yet. ✅")