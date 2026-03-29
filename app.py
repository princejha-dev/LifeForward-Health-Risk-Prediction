import streamlit as st
import requests

#i have used github copilot to create this UI according to my customization and need

st.set_page_config(page_title="NovaGen Health Predictor", page_icon="🏥", layout="centered")

# ── Custom CSS for a polished wizard look ──────────────────────────────────
st.markdown("""
<style>
    /* Progress bar colour override */
    .stProgress > div > div > div { background: linear-gradient(90deg, #00c6ff, #0072ff); }

    /* Step header badge */
    .step-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0072ff, #00c6ff);
        color: white;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }

    /* Navigation button row */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────
TOTAL_STEPS = 4

if "step" not in st.session_state:
    st.session_state.step = 1

# Initialise every input field so values survive page reruns
defaults = {
    "age": 30.0, "bmi": 22.0, "blood_pressure": 120.0, "cholesterol": 200.0,
    "glucose": 99.0, "heart_rate": 72.0, "blood_group": "A",
    "sleep": 7.0, "exercise": 1.0, "water": 3.0, "stress": 5.0,
    "smoking": 0, "alcohol": 0, "diet_type": "Standard",
    "diet_quality": 0, "mental_health": 0, "phys_activity": 0,
    "med_history": 0, "allergies": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helper: navigation ─────────────────────────────────────────────────────
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def go_to_step(n):
    st.session_state.step = n


# ── Header & progress bar ──────────────────────────────────────────────────
st.title("🏥 NovaGen Health Prediction")

step_labels = ["Physiological", "Lifestyle", "Medical History", "Results"]
progress = st.session_state.step / TOTAL_STEPS
st.progress(progress)

cols = st.columns(TOTAL_STEPS)
for i, label in enumerate(step_labels):
    with cols[i]:
        if i + 1 < st.session_state.step:
            st.markdown(f"✅ **{label}**")
        elif i + 1 == st.session_state.step:
            st.markdown(f"🔵 **{label}**")
        else:
            st.markdown(f"⚪ {label}")

st.divider()

# ══════════════════════════════════════════════════════════════════════════
#  STEP 1 – Physiological Metrics
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<span class="step-badge">Step 1 / 4 — Physiological Metrics</span>', unsafe_allow_html=True)
    st.write("Let's start with some basic health numbers.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.age = st.number_input("Age", min_value=0.0, max_value=120.0, value=st.session_state.age, key="inp_age")
        st.session_state.bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=st.session_state.bmi, key="inp_bmi")
        st.session_state.blood_pressure = st.number_input("Blood Pressure", min_value=60.0, max_value=250.0, value=st.session_state.blood_pressure, key="inp_bp")
        st.session_state.blood_group = st.selectbox("Blood Group", ["A", "B", "AB", "O"], index=["A", "B", "AB", "O"].index(st.session_state.blood_group), key="inp_bg")
    with col2:
        st.session_state.cholesterol = st.number_input("Cholesterol", min_value=100.0, max_value=400.0, value=st.session_state.cholesterol, key="inp_chol")
        st.session_state.glucose = st.number_input("Glucose Level", min_value=50.0, max_value=300.0, value=st.session_state.glucose, key="inp_glu")
        st.session_state.heart_rate = st.number_input("Heart Rate", min_value=40.0, max_value=200.0, value=st.session_state.heart_rate, key="inp_hr")

    st.write("")
    _, right = st.columns([4, 1])
    with right:
        st.button("Next →", on_click=next_step, use_container_width=True, type="primary")

# ══════════════════════════════════════════════════════════════════════════
#  STEP 2 – Lifestyle Metrics
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<span class="step-badge">Step 2 / 4 — Lifestyle Metrics</span>', unsafe_allow_html=True)
    st.write("Tell us about your daily habits.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=st.session_state.sleep, key="inp_sleep")
        st.session_state.exercise = st.number_input("Exercise Hours", min_value=0.0, max_value=24.0, value=st.session_state.exercise, key="inp_ex")
        st.session_state.water = st.number_input("Water Intake (L)", min_value=0.0, max_value=10.0, value=st.session_state.water, key="inp_water")
        st.session_state.stress = st.number_input("Stress Level (1‑10)", min_value=1.0, max_value=10.0, value=st.session_state.stress, key="inp_stress")
    with col2:
        st.session_state.smoking = st.selectbox("Smoking Status", [0, 1, 2], index=st.session_state.smoking,
                                                 format_func=lambda x: {0: "Never", 1: "Former", 2: "Current"}[x], key="inp_smoke")
        st.session_state.alcohol = st.selectbox("Alcohol Consumption", [0, 1, 2], index=st.session_state.alcohol,
                                                 format_func=lambda x: {0: "None", 1: "Occasional", 2: "Frequent"}[x], key="inp_alc")
        st.session_state.diet_type = st.selectbox("Diet Type", ["Standard", "Vegetarian", "Vegan"],
                                                   index=["Standard", "Vegetarian", "Vegan"].index(st.session_state.diet_type), key="inp_diet")

    st.write("")
    left, right = st.columns([1, 1])
    with left:
        st.button("← Back", on_click=prev_step, use_container_width=True)
    with right:
        st.button("Next →", on_click=next_step, use_container_width=True, type="primary")

# ══════════════════════════════════════════════════════════════════════════
#  STEP 3 – Medical History
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown('<span class="step-badge">Step 3 / 4 — Medical History</span>', unsafe_allow_html=True)
    st.write("A few more details about your medical background.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.diet_quality = st.selectbox("Diet Quality Score", [0, 1, 2], index=st.session_state.diet_quality, key="inp_dq")
        st.session_state.mental_health = st.selectbox("Mental Health Status", [0, 1, 2], index=st.session_state.mental_health, key="inp_mh")
        st.session_state.phys_activity = st.selectbox("Physical Activity Level", [0, 1, 2], index=st.session_state.phys_activity, key="inp_pa")
    with col2:
        st.session_state.med_history = st.selectbox("Family Medical History", [0, 1, 2], index=st.session_state.med_history, key="inp_fmh")
        st.session_state.allergies = st.selectbox("Allergies", [0, 1, 2], index=st.session_state.allergies, key="inp_allg")

    st.write("")
    left, right = st.columns([1, 1])
    with left:
        st.button("← Back", on_click=prev_step, use_container_width=True)
    with right:
        st.button("Get My Results →", on_click=next_step, use_container_width=True, type="primary")

# ══════════════════════════════════════════════════════════════════════════
#  STEP 4 – Summary & Prediction
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.markdown('<span class="step-badge">Step 4 / 4 — Your Results</span>', unsafe_allow_html=True)
    st.write("Review your inputs and get your health‑risk prediction.")

    # ── Quick summary table ────────────────────────────────────────────
    with st.expander("📋 Review Your Inputs", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Physiological**")
            st.write(f"Age: {st.session_state.age}")
            st.write(f"BMI: {st.session_state.bmi}")
            st.write(f"BP: {st.session_state.blood_pressure}")
            st.write(f"Cholesterol: {st.session_state.cholesterol}")
            st.write(f"Glucose: {st.session_state.glucose}")
            st.write(f"Heart Rate: {st.session_state.heart_rate}")
            st.write(f"Blood Group: {st.session_state.blood_group}")
        with c2:
            st.markdown("**Lifestyle**")
            st.write(f"Sleep: {st.session_state.sleep} hrs")
            st.write(f"Exercise: {st.session_state.exercise} hrs")
            st.write(f"Water: {st.session_state.water} L")
            st.write(f"Stress: {st.session_state.stress}")
            smoking_map = {0: "Never", 1: "Former", 2: "Current"}
            alcohol_map = {0: "None", 1: "Occasional", 2: "Frequent"}
            st.write(f"Smoking: {smoking_map[st.session_state.smoking]}")
            st.write(f"Alcohol: {alcohol_map[st.session_state.alcohol]}")
            st.write(f"Diet: {st.session_state.diet_type}")
        with c3:
            st.markdown("**Medical**")
            st.write(f"Diet Quality: {st.session_state.diet_quality}")
            st.write(f"Mental Health: {st.session_state.mental_health}")
            st.write(f"Physical Activity: {st.session_state.phys_activity}")
            st.write(f"Medical History: {st.session_state.med_history}")
            st.write(f"Allergies: {st.session_state.allergies}")

    # ── Build payload ──────────────────────────────────────────────────
    is_vegan = st.session_state.diet_type == "Vegan"
    is_veg   = st.session_state.diet_type == "Vegetarian"
    is_ab    = st.session_state.blood_group == "AB"
    is_b     = st.session_state.blood_group == "B"
    is_o     = st.session_state.blood_group == "O"

    payload = {
        "Age": st.session_state.age,
        "BMI": st.session_state.bmi,
        "Blood_Pressure": st.session_state.blood_pressure,
        "Cholesterol": st.session_state.cholesterol,
        "Glucose_Level": st.session_state.glucose,
        "Heart_Rate": st.session_state.heart_rate,
        "Sleep_Hours": st.session_state.sleep,
        "Exercise_Hours": st.session_state.exercise,
        "Water_Intake": st.session_state.water,
        "Stress_Level": st.session_state.stress,
        "Smoking": st.session_state.smoking,
        "Alcohol": st.session_state.alcohol,
        "Diet": st.session_state.diet_quality,
        "MentalHealth": st.session_state.mental_health,
        "PhysicalActivity": st.session_state.phys_activity,
        "MedicalHistory": st.session_state.med_history,
        "Allergies": st.session_state.allergies,
        "Diet_Type__Vegan": is_vegan,
        "Diet_Type__Vegetarian": is_veg,
        "Blood_Group_AB": is_ab,
        "Blood_Group_B": is_b,
        "Blood_Group_O": is_o,
    }

    # ── Predict button ─────────────────────────────────────────────────
    st.write("")
    if st.button("🔮 Predict Health Risk", type="primary", use_container_width=True):
        with st.spinner("Analysing your health data..."):
            try:
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                if response.status_code == 200:
                    prediction = response.json().get("prediction")
                    st.write("")
                    if "High Risk" in prediction:
                        st.error(f"⚠️ {prediction}")
                    else:
                        st.success(f"✅ {prediction}")
                else:
                    st.warning(f"API Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not reach the backend API. Make sure `uvicorn api:app` is running.")

    st.write("")
    left, _ = st.columns([1, 4])
    with left:
        st.button("← Back", on_click=prev_step, use_container_width=True)

    st.write("")
    st.button("🔄 Start Over", on_click=lambda: go_to_step(1), use_container_width=True)
