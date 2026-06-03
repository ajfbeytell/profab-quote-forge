import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="QuoteForge", page_icon="🔥", layout="wide")

# ====================== QUOTEFORGE HEADER ======================
col_logo, col_title, col_auth = st.columns([1, 4, 2])

with col_logo:
    st.image("images/quoteforge_logo.png", width=160)

with col_title:
    st.markdown("# QuoteForge")
    st.markdown("**Engineering Precision. Forged Fast.**")

with col_auth:
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("Login", use_container_width=True, key="jib_login"):
            st.info("🔐 Login coming soon...")
    with col_r:
        if st.button("Register", type="primary", use_container_width=True, key="jib_register"):
            st.info("📝 Registration coming soon...")

st.markdown("---")

# Back to Home button
if st.button("← Back to Home", use_container_width=True, key="jib_back"):
    st.switch_page("main_app.py")

st.markdown("---")

# ====================== INPUTS ======================
st.sidebar.header("Jib Crane Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=20.0, value=5.0)
jib_length = st.sidebar.number_input("Jib Arm Length [m]", min_value=2.0, max_value=12.0, value=6.0, step=0.5)
column_height = st.sidebar.number_input("Column Height to Under Beam [m]", min_value=3.0, max_value=10.0, value=5.0, step=0.5)

knee_brace = st.sidebar.selectbox("Knee Brace", ["Yes", "No"], index=0)
slewing = st.sidebar.selectbox("Slewing Range", ["None", "180°", "270°", "360°"], index=0)

design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0], index=2)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)

if st.sidebar.button("Generate Prelim Designs", type="primary"):
    g = 9.81
    design_load_kn = swl * daf * design_factor * g

    max_moment_knm = design_load_kn * jib_length * 1.5
    column_axial_kn = design_load_kn * 1.2

    height_factor = (column_height / 4.0) ** 2.5
    load_factor = swl ** 1.8
    knee_reduction = 0.65 if knee_brace == "Yes" else 1.0

    # ====================== FULL UB RANGE FOR JIB ARM ======================
    arm_db = [
        {"name": "203x133x25.1 UB S355", "mass": 25.1, "capacity_knm": 850},
        {"name": "203x133x30 UB S355", "mass": 30, "capacity_knm": 980},
        {"name": "254x146x31 UB S355", "mass": 31, "capacity_knm": 1150},
        {"name": "254x146x37 UB S355", "mass": 37, "capacity_knm": 1380},
        {"name": "254x146x43 UB S355", "mass": 43, "capacity_knm": 1600},
        {"name": "305x102x24.8 UB S355", "mass": 24.8, "capacity_knm": 920},
        {"name": "305x102x28.2 UB S355", "mass": 28.2, "capacity_knm": 1050},
        {"name": "305x102x32.8 UB S355", "mass": 32.8, "capacity_knm": 1180},
        {"name": "305x165x40.3 UB S355", "mass": 40.3, "capacity_knm": 1480},
        {"name": "305x165x46.1 UB S355", "mass": 46.1, "capacity_knm": 1700},
        {"name": "305x165x54 UB S355", "mass": 54, "capacity_knm": 1950},
        {"name": "356x171x45 UB S355", "mass": 45, "capacity_knm": 1750},
        {"name": "356x171x51 UB S355", "mass": 51, "capacity_knm": 1980},
        {"name": "356x171x67.1 UB S355", "mass": 67.1, "capacity_knm": 2450},
        {"name": "406x140x39 UB S355", "mass": 39, "capacity_knm": 1550},
        {"name": "406x140x46 UB S355", "mass": 46, "capacity_knm": 1800},
        {"name": "406x178x54.1 UB S355", "mass": 54.1, "capacity_knm": 2100},
        {"name": "406x178x60.1 UB S355", "mass": 60.1, "capacity_knm": 2350},
        {"name": "406x178x67.1 UB S355", "mass": 67.1, "capacity_knm": 2600},
        {"name": "457x191x67.1 UB S355", "mass": 67.1, "capacity_knm": 2550},
        {"name": "457x191x89.3 UB S355", "mass": 89.3, "capacity_knm": 3200},
        {"name": "457x191x98.3 UB S355", "mass": 98.3, "capacity_knm": 3500},
        {"name": "533x210x82.2 UB S355", "mass": 82.2, "capacity_knm": 2950},
        {"name": "533x210x92.1 UB S355", "mass": 92.1, "capacity_knm": 3300},
        {"name": "533x210x101 UB S355", "mass": 101, "capacity_knm": 3600},
    ]

    # ====================== REALISTIC LARGE CHS COLUMNS (based on real manufacturers) ======================
    column_db = [
        {"name": "323.9x12.5 CHS S355", "mass": 95, "capacity_kn": 2980},
        {"name": "406.4x12.5 CHS S355", "mass": 121, "capacity_kn": 3800},
        {"name": "457x12.5 CHS S355", "mass": 137, "capacity_kn": 4500},
        {"name": "508x12.5 CHS S355", "mass": 153, "capacity_kn": 5200},
        {"name": "560x12.5 CHS S355", "mass": 169, "capacity_kn": 5800},
        {"name": "610x12.5 CHS S355", "mass": 185, "capacity_kn": 6500},
        {"name": "660x12.5 CHS S355", "mass": 200, "capacity_kn": 7200},
        {"name": "711x12.5 CHS S355", "mass": 215, "capacity_kn": 7900},
        {"name": "762x12.5 CHS S355", "mass": 230, "capacity_kn": 8600},
        {"name": "610x16 CHS S355", "mass": 235, "capacity_kn": 8200},
        {"name": "660x16 CHS S355", "mass": 255, "capacity_kn": 9000},
    ]

    # Arm results - ONLY "✅ Good" members
    arm_results = []
    for arm in arm_db:
        util = (max_moment_knm / arm["capacity_knm"]) * 100
        est_mass = arm["mass"] * jib_length * 1.1
        if util < 70:
            arm_results.append({
                "Section": arm["name"],
                "Type": "UB",
                "Est. Mass (kg)": round(est_mass),
                "Utilisation %": f"{round(util, 1)}%",
                "Status": "✅ Good"
            })

    # Column results
    col_results = []
    for col in column_db:
        effective_capacity = col["capacity_kn"] / (height_factor * load_factor * knee_reduction)
        util = (column_axial_kn / effective_capacity) * 100
        est_mass = col["mass"] * column_height * 1.1
        if util < 90:
            col_results.append({
                "Section": col["name"],
                "Type": "CHS",
                "Est. Mass (kg)": round(est_mass),
                "Utilisation %": f"{round(util, 1)}%",
                "Status": "✅ Good" if util < 70 else "⚠️ Review"
            })

    st.success(f"✅ {swl}t Jib Crane — Arm {jib_length}m, Column {column_height}m (Real cantilever design – supported on column side only)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recommended Jib Arm (UB) – Only Good")
        if arm_results:
            df_arm = pd.DataFrame(arm_results)
            st.dataframe(df_arm, use_container_width=True, hide_index=True)
            st.success(f"**Best Arm: {arm_results[0]['Section']}**")
        else:
            st.warning("No Good arm section found – try lower SWL.")

    with col2:
        st.subheader("Recommended Column (CHS)")
        if col_results:
            df_col = pd.DataFrame(col_results)
            st.dataframe(df_col, use_container_width=True, hide_index=True)
            st.success(f"**Best Column: {col_results[0]['Section']}**")
        else:
            st.warning("No suitable column found – try different inputs.")

    # BOM
    st.markdown("---")
    st.subheader("Bill of Materials - Recommended")
    best_arm = arm_results[0] if arm_results else None
    best_col = col_results[0] if col_results else None

    baseplate_size = "700x700x30 mm" if column_height > 6 else "600x600x25 mm"

    bom = pd.DataFrame({
        "Item": ["Jib Arm", "Column", "Base Plate", "Knee Brace", "Slewing Shaft"],
        "Description": [
            best_arm["Section"] if best_arm else "-",
            best_col["Section"] if best_col else "-",
            baseplate_size,
            "100 x 100 x 10 L Angle" if knee_brace == "Yes" else "-",
            f"EN8 Shaft Ø{80 if swl <= 5 else 100 if swl <= 10 else 120} mm" if slewing != "None" else "-"
        ],
        "Qty": [1, 1, 1, 1 if knee_brace == "Yes" else 0, 1 if slewing != "None" else 0],
        "Est Mass (kg)": [
            best_arm["Est. Mass (kg)"]*0.6 if best_arm else 0,
            best_col["Est. Mass (kg)"]*0.4 if best_col else 0,
            180 if column_height > 6 else 140, 45, 30
        ]
    })
    st.dataframe(bom, use_container_width=True)
    st.info(f"**Total Estimated Mass: {bom['Est Mass (kg)'].sum():.0f} kg**")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill inputs on the left and click **Generate Prelim Designs**")