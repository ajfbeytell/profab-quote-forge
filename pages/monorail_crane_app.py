import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monorail Crane Designer", layout="wide")
st.title("🛠️ Monorail Crane Preliminary Designer (SANS 10162)")
st.markdown("**South Africa Local Sections Only**")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
total_length = st.sidebar.number_input("Total Runway Length [m]", min_value=6.0, max_value=60.0, value=18.0, step=1.0)
bay_spacing = st.sidebar.number_input("Bay Spacing (Column spacing) [m]", min_value=4.0, max_value=12.0, value=6.0, step=0.5)
height = st.sidebar.number_input("Height to Runway Beam [m]", min_value=3.0, max_value=12.0, value=6.0)

columns_per_side = st.sidebar.number_input("Columns per side", min_value=2, max_value=10, value=4)
has_overhang = st.sidebar.selectbox("Has Overhang?", ["Yes", "No"], index=0)
overhang = st.sidebar.number_input("Overhang each end [m]", min_value=0.0, max_value=3.0, value=1.0, step=0.5) if has_overhang == "Yes" else 0.0

design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0, 5.0], index=3)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)

if st.sidebar.button("Generate Prelim Design", type="primary"):
    g = 9.81
    design_load_kn = swl * daf * design_factor * g
    effective_span = bay_spacing
    max_moment = (design_load_kn * effective_span) / 4
    total_beam_length = total_length + (2 * overhang)

    # ====================== MAIN RESULTS ======================
    data = []

    data.append({
        "Member": "Main Crane Beam (Runway)",
        "Section": "457x191x67 UB S355",
        "Length (m)": round(total_beam_length, 2),
        "Est. Mass (kg)": round(67 * total_beam_length),
        "Notes": "Primary runway beam"
    })

    data.append({
        "Member": "Columns",
        "Section": "254x254x73 UC S355",
        "Qty": columns_per_side * 2,
        "Est. Mass (kg)": round(73 * height * columns_per_side * 2),
        "Notes": "Main vertical supports"
    })

    # Base Plate Sizing (approximate but practical)
    base_plate_size = "400x400x20" if swl <= 5 else "500x500x25" if swl <= 10 else "600x600x30"

    data.append({
        "Member": "Base Plates",
        "Section": f"{base_plate_size} S355",
        "Qty": columns_per_side * 2,
        "Est. Mass (kg)": round(45 * columns_per_side * 2),
        "Notes": "Anchor bolt base plate"
    })

    data.append({
        "Member": "Cross Beams (Ties)",
        "Section": "203x133x25 UB S355",
        "Qty": columns_per_side - 1,
        "Est. Mass (kg)": round(25 * bay_spacing * (columns_per_side - 1)),
        "Notes": "Transverse beams"
    })

    data.append({
        "Member": "Bracing",
        "Section": "100x100x10 Equal Angle S355",
        "Qty": "As required",
        "Est. Mass (kg)": round(18 * height * (columns_per_side - 1) * 2),
        "Notes": "Diagonal bracing"
    })

    st.success(f"✅ {swl}t Monorail Crane — Total Runway {total_beam_length:.1f}m")

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ====================== DETAILED BOM ======================
    st.subheader("Bill of Materials (BOM)")
    bom = pd.DataFrame({
        "Item": ["Main Crane Beam (Runway)", "Columns", "Base Plates", "Cross Beams (Ties)", "Bracing (Angle)", "Anchor Bolts & Holding Down Bolts"],
        "Section / Description": ["457x191x67 UB S355", "254x254x73 UC S355", f"{base_plate_size} S355 Plate", 
                                 "203x133x25 UB S355", "100x100x10 Equal Angle S355", "M20 / M24 HD Bolts"],
        "Qty": [1, columns_per_side*2, columns_per_side*2, columns_per_side-1, "As required", "4 per column"],
        "Est. Mass (kg)": [round(67 * total_beam_length), round(73 * height * columns_per_side * 2),
                          round(45 * columns_per_side * 2), round(25 * bay_spacing * (columns_per_side - 1)), 
                          round(18 * height * (columns_per_side - 1) * 2), 0]
    })
    st.dataframe(bom, use_container_width=True)

    total_mass = bom["Est. Mass (kg)"].sum()
    st.info(f"**Total Estimated Steel Mass: {total_mass:.0f} kg**")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill all inputs on the left sidebar and click **Generate Prelim Design**")