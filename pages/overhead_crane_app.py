import streamlit as st
import pandas as pd

st.set_page_config(page_title="Overhead Crane Designer", layout="wide")
st.title("🛠️ Overhead Crane Preliminary Designer (SANS 10162)")
st.markdown("**South Africa Local Sections Only** — Fabricated Box Girder Bridge Crane")

# ====================== INPUTS ======================
st.sidebar.header("Design Inputs")

swl = st.sidebar.number_input("Safe Working Load (SWL) [tons]", min_value=1.0, max_value=50.0, value=10.0, step=1.0)
span = st.sidebar.number_input("Crane Span (between runway beams) [m]", min_value=1.0, max_value=40.0, value=15.0, step=0.5)
runway_length = st.sidebar.number_input("Total Runway Length [m]", min_value=10.0, max_value=100.0, value=30.0, step=1.0)
bay_spacing = st.sidebar.number_input("Bay / Column Spacing [m]", min_value=3.0, max_value=12.0, value=6.0, step=0.5)
height = st.sidebar.number_input("Clear Height to Underside of Runway Beam [m]", min_value=4.0, max_value=20.0, value=8.0, step=0.5)

crane_type = st.sidebar.selectbox("Girder Type", ["Single Box Girder", "Double Box Girder"], index=0)
has_haunches = st.sidebar.selectbox("Has Haunches on Columns?", ["Yes", "No"], index=0)
has_bracing = st.sidebar.selectbox("Has Bracing on Columns?", ["Yes", "No"], index=0)
environment = st.sidebar.selectbox("Environment", ["Indoor", "Outdoor"], index=0)
duty_class = st.sidebar.selectbox("Duty Class", ["Light", "Medium", "Heavy"], index=1)

design_factor = st.sidebar.selectbox("Design / Safety Factor", [1.25, 1.67, 2.0, 4.0, 5.0], index=3)
daf = st.sidebar.selectbox("Dynamic Amplification Factor (DAF)", [1.0, 1.25, 1.5, 2.0], index=1)

if st.sidebar.button("Generate Prelim Design", type="primary"):
    # All inputs affect the load
    duty_multiplier = {"Light": 1.0, "Medium": 1.25, "Heavy": 1.5}[duty_class]
    wind_factor = 1.15 if environment == "Outdoor" else 1.0
    effective_daf = daf * duty_multiplier

    g = 9.81
    design_load_kn = swl * effective_daf * design_factor * g

    # Moment on main girder
    moment_reduction = 0.75 if has_haunches == "Yes" else 1.0
    effective_moment_knm = (design_load_kn * span / 8) * moment_reduction * wind_factor

    # ====================== EXPANDED BOX GIRDER DATABASE (based on your Excel) ======================
    box_girder_db = [
        {"name": "Single Box 400x300x6/8", "capacity_knm": 350, "mass_per_m": 48, "top": "300x8 Plate", "bottom": "300x16 Plate", "web": "350x5 Plate (x2)", "angle": "40x5 Angle", "angle_qty": 2},
        {"name": "Single Box 500x350x8/10", "capacity_knm": 550, "mass_per_m": 68, "top": "350x10 Plate", "bottom": "350x16 Plate", "web": "400x5 Plate (x2)", "angle": "40x5 Angle", "angle_qty": 2},
        {"name": "Single Box 600x400x8/10", "capacity_knm": 850, "mass_per_m": 85, "top": "400x10 Plate", "bottom": "400x16 Plate", "web": "600x8 Plate (x2)", "angle": "50x5 Angle", "angle_qty": 4},
        {"name": "Single Box 700x450x10/12", "capacity_knm": 1250, "mass_per_m": 115, "top": "450x12 Plate", "bottom": "450x20 Plate", "web": "700x10 Plate (x2)", "angle": "50x5 Angle", "angle_qty": 4},
        {"name": "Single Box 800x500x10/12", "capacity_knm": 1650, "mass_per_m": 145, "top": "500x12 Plate", "bottom": "500x25 Plate", "web": "800x10 Plate (x2)", "angle": "60x6 Angle", "angle_qty": 4},
        {"name": "Single Box 900x550x12/14", "capacity_knm": 2100, "mass_per_m": 185, "top": "550x14 Plate", "bottom": "550x25 Plate", "web": "900x12 Plate (x2)", "angle": "60x6 Angle", "angle_qty": 4},
        {"name": "Single Box 1000x600x12/16", "capacity_knm": 2600, "mass_per_m": 230, "top": "600x16 Plate", "bottom": "600x25 Plate", "web": "1000x12 Plate (x2)", "angle": "60x6 Angle", "angle_qty": 4},
        {"name": "Double Box 600x400x8/10", "capacity_knm": 1700, "mass_per_m": 165, "top": "400x10 Plate (x2)", "bottom": "400x16 Plate (x2)", "web": "600x8 Plate (x4)", "angle": "50x5 Angle", "angle_qty": 8},
        {"name": "Double Box 700x450x10/12", "capacity_knm": 2450, "mass_per_m": 225, "top": "450x12 Plate (x2)", "bottom": "450x20 Plate (x2)", "web": "700x10 Plate (x4)", "angle": "60x6 Angle", "angle_qty": 8},
        {"name": "Double Box 800x500x10/12", "capacity_knm": 3250, "mass_per_m": 285, "top": "500x12 Plate (x2)", "bottom": "500x25 Plate (x2)", "web": "800x10 Plate (x4)", "angle": "60x6 Angle", "angle_qty": 8},
        {"name": "Double Box 900x550x12/14", "capacity_knm": 4100, "mass_per_m": 365, "top": "550x14 Plate (x2)", "bottom": "550x25 Plate (x2)", "web": "900x12 Plate (x4)", "angle": "60x6 Angle", "angle_qty": 8},
        {"name": "Double Box 1000x600x12/16", "capacity_knm": 5100, "mass_per_m": 455, "top": "600x16 Plate (x2)", "bottom": "600x25 Plate (x2)", "web": "1000x12 Plate (x4)", "angle": "60x6 Angle", "angle_qty": 8},
    ]

    # Find viable box girders
    viable_boxes = []
    for box in box_girder_db:
        util = (effective_moment_knm / box["capacity_knm"]) * 100
        est_mass = round(box["mass_per_m"] * span)
        if util < 95:
            viable_boxes.append({
                "Section": box["name"],
                "Est. Mass (kg)": est_mass,
                "Utilisation %": round(util, 1),
                "Status": "✅ Good" if util < 75 else "⚠️ Acceptable",
                "top": box["top"],
                "bottom": box["bottom"],
                "web": box["web"],
                "angle": box["angle"],
                "angle_qty": box["angle_qty"]
            })

    viable_boxes = sorted(viable_boxes, key=lambda x: x["Est. Mass (kg)"])[:5]
    best_box = viable_boxes[0] if viable_boxes else None

    st.success(f"✅ {swl}t {crane_type} Overhead Crane — Span {span}m | Duty: {duty_class} | {environment}")

    if best_box:
        st.success(f"**BEST RECOMMENDED BOX GIRDER: {best_box['Section']}** | Utilisation: **{best_box['Utilisation %']}%** | Mass: **{best_box['Est. Mass (kg)']} kg**")

    st.subheader("Top 5 Viable Box Girders")
    st.dataframe(pd.DataFrame(viable_boxes), use_container_width=True, hide_index=True)

    # Runway beams, track, wheels (same as before)
    runway_db = [
        {"name": "203x133x25.1 UB S355", "mass": 25.1, "capacity_knm": 85},
        {"name": "254x146x31 UB S355", "mass": 31, "capacity_knm": 140},
        {"name": "305x165x40.3 UB S355", "mass": 40.3, "capacity_knm": 280},
        {"name": "356x171x45 UB S355", "mass": 45, "capacity_knm": 380},
        {"name": "406x178x54.1 UB S355", "mass": 54.1, "capacity_knm": 520},
        {"name": "457x191x67.1 UB S355", "mass": 67.1, "capacity_knm": 950},
        {"name": "533x210x82.2 UB S355", "mass": 82.2, "capacity_knm": 1380},
        {"name": "533x210x92.1 UB S355", "mass": 92.1, "capacity_knm": 1620},
        {"name": "610x229x101 UB S355", "mass": 101, "capacity_knm": 1950},
    ]

    viable_runway = []
    for sec in runway_db:
        util = (effective_moment_knm / sec["capacity_knm"]) * 100
        est_mass = round(sec["mass"] * runway_length)
        if util < 95:
            viable_runway.append({
                "Section": sec["name"],
                "Est. Mass (kg)": est_mass,
                "Utilisation %": round(util, 1),
                "Status": "✅ Good" if util < 75 else "⚠️ Acceptable"
            })

    viable_runway = sorted(viable_runway, key=lambda x: x["Est. Mass (kg)"])[:5]

    st.subheader("Top 5 Viable Runway Beams (UB)")
    st.dataframe(pd.DataFrame(viable_runway), use_container_width=True, hide_index=True)

    # Runway Track & Wheels
    if swl <= 8:
        runway_desc = "40x40 Square Bar"
    elif swl <= 12:
        runway_desc = "50x50 Square Bar"
    elif swl <= 20:
        runway_desc = "60x60 Square Bar"
    else:
        runway_desc = "Crane Rail (30-45 kg/m)"

    if swl <= 3:
        wheel_spacing, wheel_od = "1.2 m", "Ø125 mm (Wheel Block)"
    elif swl <= 5:
        wheel_spacing, wheel_od = "1.5 m", "Ø150 mm (Wheel Block)"
    elif swl <= 10:
        wheel_spacing, wheel_od = "1.8 m", "Ø200 mm"
    elif swl <= 20:
        wheel_spacing, wheel_od = "2.0 m", "Ø250 mm"
    else:
        wheel_spacing, wheel_od = "2.5 m", "Ø300 mm"

    st.success(f"**End Carriage Wheel Spacing (Gauge): {wheel_spacing}**")
    st.success(f"**Recommended Wheel Diameter (OD): {wheel_od}**")

    # ====================== BOM with full box girder breakdown ======================
    num_columns = int(runway_length / bay_spacing) * 2 + 2
    column_mass = round(97 * height * num_columns) if has_bracing == "Yes" else round(73 * height * num_columns)

    st.subheader("Bill of Materials (BOM)")
    bom = pd.DataFrame({
        "Item": ["Top Plate", "Bottom Plate", "Web Plates", "Internal Angle Braces",
                 "Runway Beams (pair)", "Columns (UC/UB)", "Haunches", "Runway Track (pair)", "End Carriage Wheels"],
        "Section / Description": [best_box["top"], best_box["bottom"], best_box["web"], best_box["angle"],
                                  viable_runway[0]["Section"] if viable_runway else "N/A",
                                  "305x305x97 UC S355", "300x300x20 Plate" if has_haunches == "Yes" else "None",
                                  runway_desc, wheel_od],
        "Qty": [1, 1, 2 if "Single" in best_box["Section"] else 4, best_box["angle_qty"],
                2, num_columns, 8 if has_haunches == "Yes" else 0, 2, 4],
        "Est. Mass (kg)": [round(best_box["Est. Mass (kg)"] * 0.25), round(best_box["Est. Mass (kg)"] * 0.30),
                           round(best_box["Est. Mass (kg)"] * 0.35), round(best_box["Est. Mass (kg)"] * 0.10),
                           viable_runway[0]["Est. Mass (kg)"] * 2 if viable_runway else 0,
                           column_mass, 180 if has_haunches == "Yes" else 0, "Rail / Bar only", 120]
    })
    st.dataframe(bom, use_container_width=True, hide_index=True)

    total_mass = sum(row["Est. Mass (kg)"] for row in bom.to_dict('records') if isinstance(row["Est. Mass (kg)"], (int, float)))

    st.success(f"**Total Estimated Mass: {total_mass} kg**")

    st.error("⚠️ PRELIMINARY SIZING ONLY — For quoting. Must be checked & signed by registered ECSA Engineer.")

else:
    st.info("👈 Fill all inputs on the left and click **Generate Prelim Design**")