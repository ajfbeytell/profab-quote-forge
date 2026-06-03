import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal Crane Designer", layout="wide")
st.title("🛠️ Portal Crane Preliminary Designer (SANS 10162)")
st.markdown("**South Africa Local Sections Only** — Free-standing Portal Crane with A-frame legs")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=50.0, value=10.0, step=1.0)
span = st.sidebar.number_input("Span (distance between A-frames) [m]", min_value=1.0, max_value=40.0, value=15.0, step=0.5)
runway_length = st.sidebar.number_input("Total Runway Length [m]", min_value=10.0, max_value=100.0, value=30.0, step=1.0)
height = st.sidebar.number_input("Clear Height to Underside of Girder [m]", min_value=4.0, max_value=15.0, value=6.0, step=0.5)

crane_type = st.sidebar.selectbox("Crane Girder Type", ["Single Girder", "Double Girder"], index=0)
has_knee_brace = st.sidebar.selectbox("Has Knee Braces on A-frames?", ["Yes", "No"], index=0)
environment = st.sidebar.selectbox("Environment", ["Indoor", "Outdoor"], index=0)
duty_class = st.sidebar.selectbox("Duty Class", ["Light", "Medium", "Heavy"], index=1)

overhang_type = st.sidebar.selectbox("Overhang", ["None", "One side only", "Both sides"], index=2)
overhang_length = st.sidebar.number_input("Overhang length each side [m]", min_value=0.0, max_value=5.0, value=1.0, step=0.5) if overhang_type != "None" else 0.0

design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0, 5.0], index=3)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)

if st.sidebar.button("Generate Prelim Design", type="primary"):
    # Duty Class and Environment affect the load
    duty_multiplier = {"Light": 1.0, "Medium": 1.25, "Heavy": 1.5}[duty_class]
    wind_factor = 1.15 if environment == "Outdoor" else 1.0
    effective_daf = daf * duty_multiplier

    g = 9.81
    design_load_kn = swl * effective_daf * design_factor * g

    # Overhang and Knee Brace affect moment
    overhang_factor = 1.0
    if overhang_type == "One side only":
        overhang_factor = 1.15
    elif overhang_type == "Both sides":
        overhang_factor = 1.25

    moment_reduction = 0.55 if has_knee_brace == "Yes" else 1.0
    effective_moment_knm = (design_load_kn * span / 8) * moment_reduction * overhang_factor * wind_factor

    # ====================== FULL UB RANGE ======================
    girder_db = [
        {"name": "203x133x25.1 UB S355", "mass": 25.1, "capacity_knm": 85},
        {"name": "203x133x30 UB S355", "mass": 30, "capacity_knm": 105},
        {"name": "254x146x31 UB S355", "mass": 31, "capacity_knm": 140},
        {"name": "254x146x37 UB S355", "mass": 37, "capacity_knm": 170},
        {"name": "254x146x43 UB S355", "mass": 43, "capacity_knm": 200},
        {"name": "305x102x24.8 UB S355", "mass": 24.8, "capacity_knm": 110},
        {"name": "305x102x28.2 UB S355", "mass": 28.2, "capacity_knm": 130},
        {"name": "305x102x32.8 UB S355", "mass": 32.8, "capacity_knm": 155},
        {"name": "305x165x40.3 UB S355", "mass": 40.3, "capacity_knm": 280},
        {"name": "305x165x46.1 UB S355", "mass": 46.1, "capacity_knm": 320},
        {"name": "305x165x54 UB S355", "mass": 54, "capacity_knm": 380},
        {"name": "356x171x45 UB S355", "mass": 45, "capacity_knm": 380},
        {"name": "356x171x51 UB S355", "mass": 51, "capacity_knm": 430},
        {"name": "356x171x67.1 UB S355", "mass": 67.1, "capacity_knm": 580},
        {"name": "406x140x39 UB S355", "mass": 39, "capacity_knm": 240},
        {"name": "406x140x46 UB S355", "mass": 46, "capacity_knm": 290},
        {"name": "406x178x54.1 UB S355", "mass": 54.1, "capacity_knm": 520},
        {"name": "406x178x60.1 UB S355", "mass": 60.1, "capacity_knm": 580},
        {"name": "406x178x67.1 UB S355", "mass": 67.1, "capacity_knm": 650},
        {"name": "406x178x74.3 UB S355", "mass": 74.3, "capacity_knm": 720},
        {"name": "457x191x67.1 UB S355", "mass": 67.1, "capacity_knm": 950},
        {"name": "457x191x89.3 UB S355", "mass": 89.3, "capacity_knm": 1250},
        {"name": "457x191x98.3 UB S355", "mass": 98.3, "capacity_knm": 1380},
        {"name": "533x210x82.2 UB S355", "mass": 82.2, "capacity_knm": 1380},
        {"name": "533x210x92.1 UB S355", "mass": 92.1, "capacity_knm": 1620},
        {"name": "533x210x101 UB S355", "mass": 101, "capacity_knm": 1800},
        {"name": "533x210x109 UB S355", "mass": 109, "capacity_knm": 1950},
        {"name": "533x210x122 UB S355", "mass": 122, "capacity_knm": 2200},
        {"name": "610x229x101 UB S355", "mass": 101, "capacity_knm": 1950},
        {"name": "610x229x113 UB S355", "mass": 113, "capacity_knm": 2250},
        {"name": "610x229x125 UB S355", "mass": 125, "capacity_knm": 2500},
    ]

    # Viable girders
    viable_girders = []
    for sec in girder_db:
        util = (effective_moment_knm / sec["capacity_knm"]) * 100
        est_mass = round(sec["mass"] * span)
        if util < 95:
            viable_girders.append({
                "Section": sec["name"],
                "Est. Mass (kg)": est_mass,
                "Utilisation %": round(util, 1),
                "Status": "✅ Good" if util < 75 else "⚠️ Acceptable"
            })

    viable_girders = sorted(viable_girders, key=lambda x: x["Est. Mass (kg)"])[:5]
    best_girder = viable_girders[0] if viable_girders else None

    # Runway Track
    if swl <= 8:
        runway_desc = "40x40 Square Bar"
    elif swl <= 12:
        runway_desc = "50x50 Square Bar"
    elif swl <= 20:
        runway_desc = "60x60 Square Bar"
    else:
        runway_desc = "Crane Rail (30-45 kg/m)"

    # Wheel Spacing & Size
    if swl <= 3:
        wheel_spacing = "1.2 m"
        wheel_od = "Ø125 mm (Wheel Block)"
    elif swl <= 5:
        wheel_spacing = "1.5 m"
        wheel_od = "Ø150 mm (Wheel Block)"
    elif swl <= 10:
        wheel_spacing = "1.8 m"
        wheel_od = "Ø200 mm"
    elif swl <= 20:
        wheel_spacing = "2.0 m"
        wheel_od = "Ø250 mm"
    else:
        wheel_spacing = "2.5 m"
        wheel_od = "Ø300 mm"

    st.success(f"✅ {swl}t {crane_type} Portal Crane — Span {span}m | Runway {runway_length}m | Duty: {duty_class} | {environment}")

    if best_girder:
        st.success(f"**BEST RECOMMENDED GIRDER: {best_girder['Section']}** | Utilisation: **{best_girder['Utilisation %']}%** | Mass: **{best_girder['Est. Mass (kg)']} kg**")

    st.subheader("Top 5 Viable Main Crane Girders")
    st.dataframe(pd.DataFrame(viable_girders), use_container_width=True, hide_index=True)

    st.success(f"**End Carriage Wheel Spacing (Gauge): {wheel_spacing}**")
    st.success(f"**Recommended Wheel Diameter (OD): {wheel_od}**")

    # ====================== BOM ======================
    girder_mass = best_girder["Est. Mass (kg)"] if best_girder else 0
    aframe_mass = round(97 * height * 2)
    knee_mass = round(31 * height * 2) if has_knee_brace == "Yes" else 0
    wheel_mass = 30

    total_mass = girder_mass + aframe_mass + knee_mass + wheel_mass

    st.subheader("Bill of Materials (BOM)")
    bom = pd.DataFrame({
        "Item": ["Main Crane Girder", "A-Frame Legs (sides)", "Runway Tracks (pair)", "Knee Braces", "End Carriage Wheels"],
        "Section / Description": [best_girder["Section"] if best_girder else "N/A", "305x305x97 UC S355", runway_desc,
                                 "254x146x31 UB S355" if has_knee_brace == "Yes" else "None", wheel_od],
        "Qty": [1, 2, 2, 4 if has_knee_brace == "Yes" else 0, 4],
        "Est. Mass (kg)": [girder_mass, aframe_mass, "Rail / Bar only", knee_mass, wheel_mass]
    })
    st.dataframe(bom, use_container_width=True, hide_index=True)

    st.success(f"**Total Estimated Mass: {total_mass} kg**")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill all inputs on the left and click **Generate Prelim Design**")