import streamlit as st

st.set_page_config(page_title="QuoteForge", page_icon="🔥", layout="wide")

# === HIDE SIDEBAR COMPLETELY ===
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        section[data-testid="stSidebarNav"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
col_logo, col_title, col_auth = st.columns([1, 4, 2])

with col_logo:
    st.image("images/quoteforge_logo.png", width=160)

with col_title:
    st.markdown("# QuoteForge")
    st.markdown("**Engineering Precision. Forged Fast.**")

with col_auth:
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("Login", use_container_width=True, key="main_login"):
            st.info("🔐 Login coming soon...")
    with col_r:
        if st.button("Register", type="primary", use_container_width=True, key="main_register"):
            st.info("📝 Registration coming soon...")

st.markdown("---")

# ====================== HERO ======================
st.markdown("""
<div style="text-align: center;">
    <h2 style="color: #1E3A8A;">Fast, Accurate Preliminary Designs for Quoting</h2>
    <p style="font-size: 1.3rem;">AI-powered tools for cranes, lifting equipment and more.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ====================== CATEGORIES ======================
st.subheader("Choose Design Category")

cat1, cat2, cat3 = st.columns(3)

with cat1:
    st.markdown("### 🏗️ Cranes & Lifting")
    st.write("Spreader beams, lifting beams, jib cranes, monorail, portal, overhead & underslung cranes")
    if st.button("Enter Cranes & Lifting →", type="primary", use_container_width=True, key="enter_cranes"):
        st.session_state.page = "cranes"

with cat2:
    st.markdown("### 🏠 Structural Buildings")
    st.write("Portal frames, industrial sheds, warehouses")
    st.button("Coming Soon", disabled=True, use_container_width=True, key="coming_soon_buildings")

with cat3:
    st.markdown("### 🛢️ Tanks & Silos")
    st.write("Storage tanks, pressure vessels, silos")
    st.button("Coming Soon", disabled=True, use_container_width=True, key="coming_soon_tanks")

st.markdown("---")

# ====================== CRANES & LIFTING SECTION ======================
if st.session_state.get("page") == "cranes":
    st.subheader("Cranes & Lifting Equipment Designer")
    st.write("Select the equipment you want to design:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("images/spreader_beam.png", width=230)
        st.subheader("Spreader Beam")
        if st.button("Design Spreader Beam", key="spreader_btn", use_container_width=True):
            st.switch_page("pages/spreader_beam_app.py")

    with col2:
        st.image("images/lifting_beam.png", width=230)
        st.subheader("Lifting Beam")
        if st.button("Design Lifting Beam", key="lifting_btn", use_container_width=True):
            st.switch_page("pages/lifting_beam_app.py")

    with col3:
        st.image("images/jib_crane.png", width=230)
        st.subheader("Jib Crane")
        if st.button("Design Jib Crane", key="jib_btn", use_container_width=True):
            st.switch_page("pages/jib_crane_app.py")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.image("images/monorail_crane.png", width=230)
        st.subheader("Monorail Crane")
        if st.button("Design Monorail Crane", key="monorail_btn", use_container_width=True):
            st.switch_page("pages/monorail_crane_app.py")

    with col5:
        st.image("images/portal_crane.png", width=230)
        st.subheader("Portal Frame Crane")
        if st.button("Design Portal Frame Crane", key="portal_btn", use_container_width=True):
            st.switch_page("pages/portal_frame_crane_app.py")

    with col6:
        st.image("images/underslung_crane.png", width=230)
        st.subheader("Underslung Crane")
        if st.button("Design Underslung Crane", key="underslung_btn", use_container_width=True):
            st.switch_page("pages/underslung_crane_app.py")

    col7, _, _ = st.columns(3)
    with col7:
        st.image("images/overhead_crane.png", width=230)
        st.subheader("Overhead Crane")
        if st.button("Design Overhead Crane", key="overhead_btn", use_container_width=True):
            st.switch_page("pages/overhead_crane_app.py")

    if st.button("← Back to Home", key="back_home_btn", use_container_width=True):
        st.session_state.page = None
        st.rerun()

else:
    st.info("👆 Click **Enter Cranes & Lifting →** above to start designing")

# ====================== FOOTER ======================
st.markdown("---")
st.caption("© QuoteForge • Preliminary designs only • Final designs must be checked and signed off by a registered Professional Engineer (ECSA)")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = None