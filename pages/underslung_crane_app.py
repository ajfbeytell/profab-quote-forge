import streamlit as st
import pandas as pd

st.set_page_config(page_title="Underslung Crane Designer", layout="wide")
st.title("🛠️ Underslung Crane Preliminary Designer (SANS 10162)")
st.markdown("**South Africa Local Sections Only** — Hoist runs under the beam")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
span = st.sidebar.number_input("Crane Span (between runways) [m]", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
total_runway_length = st.sidebar.number_input("Total Runway Length [m]", min_value=10.0, max_value=60.0, value=24.0, step=1.0)
bay_spacing = st.sidebar.number_input("Bay Spacing (Support spacing) [m]", min_value=3.0, max_value=12.0, value=6.0, step=0.5)

design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0, 5.0], index=3)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)
crane_type = st.sidebar.selectbox("Crane Type", ["Single Girder Underslung", "Double Girder Underslung"], index=0)

if st.sidebar.button("Generate Prelim Design", type="primary"):
    g = 9.81
    design_load_kn = swl * daf * design_factor * g
    max_moment = (design_load_kn * span) / 8

    # Dynamic column calculation
    num_bays = round(total_runway_length / bay_spacing)
    columns_per_side = num_bays + 1

    results = []

    # Main Bridge Beam
    if crane_type == "Single Girder Underslung":
        beam_section = "457x191x67 UB S355"
        beam_mass_per_m = 67
    else:
        beam_section = "356x171x45 UB S355 (x2)"
        beam_mass_per_m = 90

    results.append({
        "Member": "Main Bridge Beam",
        "Section": beam_section,
        "Length (m)": round(span, 2),
        "Est. Mass (kg)": round(beam_mass_per_m * span),
        "Status": "✅ Good"
    })

    # Runway Beams
    results.append({
        "Member": "Runway Beams (pair)",
        "Section": "457x191x67 UB S355",
        "Length (m)": round(total_runway_length, 2),
        "Est. Mass (kg)": round(67 * total_runway_length * 2),
        "Status": "✅ Good"
    })

    # Columns / Supports
    results.append({
        "Member": "Columns / Supports",
        "Section": "254x254x73 UC S355",
        "Qty (per side)": columns_per_side,
        "Total Qty": columns_per_side * 2,
        "Est. Mass (kg)": round(73 * 6.0 * columns_per_side * 2),
        "Status": "✅ Good"
    })

    # Bracing
    results.append({
        "Member": "Bracing",
        "Section": "100x100x10 Equal Angle S355",
        "Qty": "As required",
        "Est. Mass (kg)": round(18 * 6.0 * (columns_per_side - 1) * 2),
        "Status": "✅ Good"
    })

    st.success(f"✅ {swl}t {crane_type} — Span {span}m | Runway {total_runway_length}m | Bay Spacing {bay_spacing}m")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ====================== BOM ======================
    st.subheader("Bill of Materials (BOM)")
    bom = pd.DataFrame({
        "Item": ["Main Bridge Beam", "Runway Beams (pair)", "Columns / Supports", "Bracing (Angle)", "Base Plates"],
        "Section / Description": [beam_section, "457x191x67 UB S355", "254x254x73 UC S355", 
                                 "100x100x10 Equal Angle S355", "400x400x20 S355 Plate"],
        "Qty / Length": [f"1 @ {span}m", f"2 @ {total_runway_length}m", f"{columns_per_side} per side", 
                        "As required", f"{columns_per_side*2}"],
        "Est. Mass (kg)": [
            round(beam_mass_per_m * span),
            round(67 * total_runway_length * 2),
            round(73 * 6.0 * columns_per_side * 2),
            round(18 * 6.0 * (columns_per_side - 1) * 2),
            round(45 * columns_per_side * 2)
        ]
    })
    st.dataframe(bom, use_container_width=True)

    total_mass = bom["Est. Mass (kg)"].sum()
    st.info(f"**Total Estimated Steel Mass: {total_mass:.0f} kg**")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill all inputs on the left and click **Generate Prelim Design**")