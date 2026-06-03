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
        if st.button("Login", use_container_width=True, key="lifting_login"):
            st.info("🔐 Login coming soon...")
    with col_r:
        if st.button("Register", type="primary", use_container_width=True, key="lifting_register"):
            st.info("📝 Registration coming soon...")

st.markdown("---")

# Back to Home button
if st.button("← Back to Home", use_container_width=True, key="lifting_back"):
    st.switch_page("main_app.py")

st.markdown("---")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=500.0, value=20.0)
span = st.sidebar.number_input("Span [m]", min_value=1.0, max_value=30.0, value=9.0, step=0.5)
lug_offset = st.sidebar.number_input("Lifting Lug Distance from Center [m]", 
                                     min_value=0.5, max_value=span/2 - 0.5, 
                                     value=span*0.25, step=0.5)
design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0], index=2)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)
deflection_limit = st.sidebar.selectbox("Deflection Limit", ["L/300", "L/360", "L/600"], index=0)

if st.sidebar.button("Generate Prelim Designs", type="primary"):
    g = 9.81
    design_load_kn = swl * daf * design_factor * g
    E = 210000  # MPa

    limit_ratio = int(deflection_limit.split('/')[1])
    max_allowable_defl = (span * 1000) / limit_ratio

    # Full realistic database including expanded UC
    sections_db = [
        {"type": "SHS", "name": "250x250x10 SHS S355", "mass": 75, "capacity_knm": 210, "Ixx": 14500},
        {"type": "SHS", "name": "300x300x12.5 SHS S355", "mass": 111, "capacity_knm": 320, "Ixx": 18500},
        {"type": "RHS", "name": "300x200x12.5 RHS S355", "mass": 98, "capacity_knm": 280, "Ixx": 24500},
        {"type": "CHS", "name": "323.9x12.5 CHS S355", "mass": 95, "capacity_knm": 298, "Ixx": 15200},
        # UB
        {"type": "UB", "name": "305x165x40.3 UB S355", "mass": 40.3, "capacity_knm": 280, "Ixx": 11200},
        {"type": "UB", "name": "356x171x45 UB S355", "mass": 45, "capacity_knm": 350, "Ixx": 16000},
        {"type": "UB", "name": "406x178x54.1 UB S355", "mass": 54.1, "capacity_knm": 420, "Ixx": 21000},
        {"type": "UB", "name": "457x191x67.1 UB S355", "mass": 67.1, "capacity_knm": 520, "Ixx": 28500},
        {"type": "UB", "name": "533x210x82.2 UB S355", "mass": 82.2, "capacity_knm": 650, "Ixx": 47500},
        {"type": "UB", "name": "533x210x92.1 UB S355", "mass": 92.1, "capacity_knm": 720, "Ixx": 53000},
        {"type": "UB", "name": "610x229x101 UB S355", "mass": 101, "capacity_knm": 850, "Ixx": 76000},
        # UC (full range added)
        {"type": "UC", "name": "203x203x46 UC S355", "mass": 46, "capacity_knm": 245, "Ixx": 15600},
        {"type": "UC", "name": "203x203x60 UC S355", "mass": 60, "capacity_knm": 310, "Ixx": 20000},
        {"type": "UC", "name": "254x254x73 UC S355", "mass": 73, "capacity_knm": 410, "Ixx": 34000},
        {"type": "UC", "name": "305x305x97 UC S355", "mass": 97, "capacity_knm": 550, "Ixx": 62000},
    ]

    results = []
    for sec in sections_db:
        # Updated moment calculation with lug offset
        # Effective max moment = (W/4) * (span - 2*lug_offset) + (W/2)*lug_offset
        moment_knm = (design_load_kn * (span - 2 * lug_offset)) / 4 + (design_load_kn / 2) * lug_offset
        
        util = (moment_knm / sec["capacity_knm"]) * 100

        Ixx_mm4 = sec["Ixx"] * 10000
        deflection_mm = (5 * design_load_kn * 1000 * (span * 1000)**3) / (384 * E * Ixx_mm4) * 0.8

        est_mass = sec["mass"] * (span + 0.8)

        if util < 95 and deflection_mm < max_allowable_defl:
            status = "✅ Good" if util < 75 else "⚠️ Review"
            results.append({
                "Section": sec["name"],
                "Est. Mass (kg)": round(est_mass),
                "Max Moment (kNm)": round(moment_knm, 1),
                "Utilisation %": f"{round(util, 1)}%",
                "Deflection (mm)": round(deflection_mm, 2),
                "Allowable (mm)": round(max_allowable_defl, 2),
                "Status": status
            })

    results = sorted(results, key=lambda x: x["Est. Mass (kg)"])

    st.success(f"✅ {swl}t × {span}m Lifting Beam — Lug offset {lug_offset}m")

    if results:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Recommended Sections (Lightest First)")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)

            best = results[0]
            st.success(f"**Best Option: {best['Section']}**")

        st.subheader("Bill of Materials - Best Option")
        best_sec = best["Section"]
        bom = pd.DataFrame({
            "Item": ["Main Beam", "End Plates", "Top Padeye", "Bottom Padeye / Hook", "Stiffeners"],
            "Description": [best_sec, "25mm S355 Plate", "Central lifting padeye", "Hook attachment", "Web stiffeners"],
            "Qty": [1, 2, 1, 1, 4],
            "Est Mass (kg)": [best["Est. Mass (kg)"], 80, 45, 35, 60]
        })
        st.dataframe(bom, use_container_width=True)
        st.info(f"**Total Estimated Mass: {bom['Est Mass (kg)'].sum():.0f} kg**")

        # 3 Next-Step Buttons
        st.markdown("---")
        st.subheader("Next Steps")
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            if st.button("📄 Generate Report with Calcs", type="primary", use_container_width=True):
                with st.expander("📋 Full Engineering Report", expanded=True):
                    st.markdown("### QuoteForge Preliminary Design Report - Lifting Beam")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success("Report ready for printing or PDF export.")

        with btn2:
            if st.button("🛠️ Get Fabrication Drawings Made", use_container_width=True):
                st.info("Fabrication drawings request sent.")

        with btn3:
            if st.button("👷 Let Engineer Sign Off Design", use_container_width=True):
                st.info("Engineer sign-off request received.")

    else:
        st.warning("⚠️ No suitable section found with current inputs.")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill inputs on the left and click **Generate Prelim Designs**")