import streamlit as st

st.set_page_config(
    page_title="Crane & Lifting Designer",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Preliminary Crane & Lifting Equipment Designer")
st.markdown("### South Africa — SANS 10162 | Macsteel S355 Sections")

st.info("**Preliminary designs only** — All calculations are for quoting purposes. "
        "Final designs must be checked and signed off by a registered Professional Engineer (ECSA).")

st.markdown("---")
st.write("**Choose your equipment type below:**")

# 3-column layout - all images same size
col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/spreader_beam.png", width=230)
    st.subheader("Spreader Beam")
    if st.button("Design Spreader Beam", key="spreader", use_container_width=True):
        st.switch_page("spreader_beam_app.py")

with col2:
    st.image("images/lifting_beam.png", width=230)
    st.subheader("Lifting Beam")
    if st.button("Design Lifting Beam", key="lifting", use_container_width=True):
        st.switch_page("lifting_beam_app.py")

with col3:
    st.image("images/jib_crane.png", width=230)
    st.subheader("Jib Crane")
    if st.button("Design Jib Crane", key="jib", use_container_width=True):
        st.switch_page("jib_crane_app.py")

# Second row
col4, col5, col6 = st.columns(3)

with col4:
    st.image("images/monorail_crane.png", width=230)
    st.subheader("Monorail Crane")
    if st.button("Design Monorail Crane", key="monorail", use_container_width=True):
        st.switch_page("monorail_crane_app.py")

with col5:
    st.image("images/portal_crane.png", width=230)
    st.subheader("Portal Frame Crane")
    if st.button("Design Portal Frame Crane", key="portal", use_container_width=True):
        st.switch_page("portal_frame_crane_app.py")

with col6:
    st.image("images/underslung_crane.png", width=230)
    st.subheader("Underslung Crane")
    if st.button("Design Underslung Crane", key="underslung", use_container_width=True):
        st.switch_page("underslung_crane_app.py")

# Third row (last item)
col7, col8, col9 = st.columns(3)

with col7:
    st.image("images/overhead_crane.png", width=230)
    st.subheader("Overhead Crane")
    if st.button("Design Overhead Crane", key="overhead", use_container_width=True):
        st.switch_page("overhead_crane_app.py")

st.markdown("---")
st.caption("All designs use available South African sections. "
           "For commercial use, always have final drawings signed by a registered engineer.")