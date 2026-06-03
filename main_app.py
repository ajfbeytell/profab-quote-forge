import streamlit as st

st.set_page_config(page_title="QuoteForge", page_icon="🔥", layout="wide")

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
        if st.button("Login", use_container_width=True):
            st.info("🔐 Login coming soon...")
    with col_r:
        if st.button("Register", type="primary", use_container_width=True):
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

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏗️ Cranes & Lifting")
    st.write("Spreader beams, lifting beams, jib cranes, monorail, portal, overhead & underslung cranes")
    
    st.page_link("pages/spreader_beam_app.py", label="Design Spreader Beam", icon="🔧", use_container_width=True)
    st.page_link("pages/lifting_beam_app.py", label="Design Lifting Beam", icon="🔧", use_container_width=True)
    st.page_link("pages/jib_crane_app.py", label="Design Jib Crane", icon="🔧", use_container_width=True)
    st.page_link("pages/monorail_crane_app.py", label="Design Monorail Crane", icon="🔧", use_container_width=True)
    st.page_link("pages/portal_frame_crane_app.py", label="Design Portal Frame Crane", icon="🔧", use_container_width=True)
    st.page_link("pages/underslung_crane_app.py", label="Design Underslung Crane", icon="🔧", use_container_width=True)
    st.page_link("pages/overhead_crane_app.py", label="Design Overhead Crane", icon="🔧", use_container_width=True)

st.caption("© QuoteForge • Preliminary designs only • Must be checked by registered ECSA Engineer")