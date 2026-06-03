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
        if st.button("Login", use_container_width=True, key="sub_login"):
            st.info("🔐 Login coming soon...")
    with col_r:
        if st.button("Register", type="primary", use_container_width=True, key="sub_register"):
            st.info("📝 Registration coming soon...")

st.markdown("---")

# Back to Home button
if st.button("← Back to Home", use_container_width=True, key="back_to_main"):
    st.switch_page("main_app.py")

st.markdown("---")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=500.0, value=20.0)
span = st.sidebar.number_input("Span [m]", min_value=1.0, max_value=30.0, value=6.0, step=0.5)
angle = st.sidebar.slider("Sling Angle to Vertical [°]", 30, 60, 45)
bottom_points = st.sidebar.selectbox("Number of Bottom Lift Points", [2, 4], index=0)

design_factor = st.sidebar.selectbox("Design / Safety Factor", 
                                     [1.25, 1.67, 2.0, 4.0], index=2)

daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)
deflection_limit = st.sidebar.selectbox("Deflection Limit", ["L/300", "L/360", "L/600"], index=0)

if st.sidebar.button("Generate Prelim Designs", type="primary"):
    g = 9.81
    design_load_kn = swl * daf * design_factor * g
    theta_rad = math.radians(angle)
    sin_theta = math.sin(theta_rad)
    comp_force_kn = (design_load_kn / 2) / sin_theta if sin_theta > 0 else design_load_kn / 2

    bending_factor = 1.0 if bottom_points == 2 else 1.25
    E = 210000  # MPa

    limit_ratio = int(deflection_limit.split('/')[1])
    max_allowable_defl = (span * 1000) / limit_ratio

    # Full South African sections database
    sections_db = [
        {"type": "SHS", "name": "200x200x8 SHS S355",   "mass": 48,  "capacity_kn": 1450, "Ixx": 7800},
        {"type": "SHS", "name": "250x250x10 SHS S355",  "mass": 75,  "capacity_kn": 2100, "Ixx": 14500},
        {"type": "SHS", "name": "300x300x12.5 SHS S355","mass": 111, "capacity_kn": 2680, "Ixx": 18500},
        {"type": "RHS", "name": "250x150x10 RHS S355",  "mass": 65,  "capacity_kn": 1950, "Ixx": 13800},
        {"type": "RHS", "name": "300x200x12.5 RHS S355","mass": 98,  "capacity_kn": 2800, "Ixx": 24500},
        {"type": "CHS", "name": "323.9x12.5 CHS S355",  "mass": 95,  "capacity_kn": 2980, "Ixx": 15200},
        {"type": "UB", "name": "203x133x25.1 UB S355", "mass": 25.1, "capacity_kn": 850,  "Ixx": 4500},
        {"type": "UB", "name": "254x146x31 UB S355",   "mass": 31,   "capacity_kn": 1150, "Ixx": 7200},
        {"type": "UB", "name": "305x165x40.3 UB S355", "mass": 40.3, "capacity_kn": 1480, "Ixx": 11200},
        {"type": "UB", "name": "356x171x45 UB S355",   "mass": 45,   "capacity_kn": 1750, "Ixx": 16000},
        {"type": "UB", "name": "406x178x54.1 UB S355", "mass": 54.1, "capacity_kn": 2100, "Ixx": 21000},
        {"type": "UB", "name": "457x191x67.1 UB S355", "mass": 67.1, "capacity_kn": 2550, "Ixx": 28500},
        {"type": "UB", "name": "533x210x82.2 UB S355", "mass": 82.2, "capacity_kn": 2950, "Ixx": 47500},
        {"type": "UB", "name": "533x210x92.1 UB S355", "mass": 92.1, "capacity_kn": 3300, "Ixx": 53000},
        {"type": "UB", "name": "610x229x101 UB S355",  "mass": 101,  "capacity_kn": 3600, "Ixx": 76000},
        {"type": "UC", "name": "203x203x46 UC S355",   "mass": 46,   "capacity_kn": 2450, "Ixx": 15600},
        {"type": "UC", "name": "203x203x60 UC S355",   "mass": 60,   "capacity_kn": 3100, "Ixx": 20000},
        {"type": "UC", "name": "254x254x73 UC S355",   "mass": 73,   "capacity_kn": 4100, "Ixx": 34000},
        {"type": "UC", "name": "305x305x97 UC S355",   "mass": 97,   "capacity_kn": 5500, "Ixx": 62000},
    ]

    results = []
    for sec in sections_db:
        adjusted_capacity = sec["capacity_kn"] / bending_factor
        util = (comp_force_kn / adjusted_capacity) * 100
        Ixx_mm4 = sec["Ixx"] * 10000
        deflection_mm = (5 * design_load_kn * 1000 * (span * 1000)**3) / (384 * E * Ixx_mm4) * 0.7
        est_mass = sec["mass"] * (span + 0.6)
        
        if util < 95 and deflection_mm < max_allowable_defl:
            status = "✅ Good" if (util < 75) else "⚠️ Review"
            results.append({
                "Section": sec["name"],
                "Est. Mass (kg)": round(est_mass),
                "Comp Force (kN)": round(comp_force_kn, 1),
                "Utilisation %": f"{round(util, 1)}%",
                "Deflection (mm)": round(deflection_mm, 2),
                "Allowable (mm)": round(max_allowable_defl, 2),
                "Status": status
            })

    results = sorted(results, key=lambda x: x["Est. Mass (kg)"])

    st.success(f"✅ {swl}t × {span}m Spreader Beam @ {angle}° — {bottom_points} bottom points")

    if results:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Recommended Sections (Lightest First)")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)

            best = results[0]
            st.success(f"**Best Option: {best['Section']}**")

        # BOM
        st.subheader("Bill of Materials - Best Option")
        best_sec = best["Section"]
        bom = pd.DataFrame({
            "Item": ["Main Beam", "End Plates", "Top Padeyes", "Bottom Padeyes / Lugs", "Shackles"],
            "Description": [best_sec, "25mm S355 Plate", "Top angled padeyes", "Welded lugs", f"SWL {swl*1.5:.0f}t"],
            "Qty": [1, 2, 2, 2*bottom_points, 2 + bottom_points],
            "Est Mass (kg)": [best["Est. Mass (kg)"], 60, 40, 25*bottom_points, 20*(2+bottom_points)]
        })
        st.dataframe(bom, use_container_width=True)
        st.info(f"**Total Estimated Mass: {bom['Est Mass (kg)'].sum():.0f} kg**")

        # ====================== NEW 3 BUTTONS ======================
        st.markdown("---")
        st.subheader("Next Steps")
        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            if st.button("📄 Generate Report with Calcs", type="primary", use_container_width=True):
                with st.expander("📋 Full Engineering Report", expanded=True):
                    st.markdown("### QuoteForge Preliminary Design Report")
                    st.write(f"**Project:** Spreader Beam {swl}t × {span}m")
                    st.write(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}")
                    st.markdown("---")
                    st.write("**Inputs**")
                    st.write(f"- SWL: {swl} t | Span: {span} m | Sling Angle: {angle}°")
                    st.write(f"- Bottom Lift Points: {bottom_points} | Safety Factor: {design_factor}")
                    st.write(f"- DAF: {daf} | Deflection Limit: {deflection_limit}")
                    st.markdown("---")
                    st.write("**Key Calculations**")
                    st.write(f"Design Load = {swl} × {daf} × {design_factor} × 9.81 = **{design_load_kn:.1f} kN**")
                    st.write(f"Compression Force per Sling = **{comp_force_kn:.1f} kN**")
                    st.write(f"Max Allowable Deflection = **{max_allowable_defl:.1f} mm**")
                    st.markdown("---")
                    st.write("**Recommended Section**")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.write("**Bill of Materials**")
                    st.dataframe(bom, use_container_width=True, hide_index=True)
                    st.success("Report ready for printing or PDF export.")

        with btn2:
            if st.button("🛠️ Get Fabrication Drawings Made", use_container_width=True):
                st.info("**Fabrication Drawings Request**\n\n"
                        "Your preliminary design is ready. Would you like us to arrange professional fabrication drawings?\n\n"
                        "Click below to send request to our drafting team.")
                if st.button("Request Fabrication Drawings →", type="primary"):
                    st.success("✅ Request sent! Our team will contact you shortly.")

        with btn3:
            if st.button("👷 Let Engineer Sign Off Design", use_container_width=True):
                st.info("**Professional Engineer Sign-Off**\n\n"
                        "Would you like a registered ECSA engineer to review and stamp this design?\n\n"
                        "This is the recommended next step before fabrication.")
                if st.button("Request Engineer Sign-Off →", type="primary"):
                    st.success("✅ Request received! We will connect you with an available engineer shortly.")

    else:
        st.warning("⚠️ No suitable section found with current inputs.")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill inputs on the left and click **Generate Prelim Designs**")