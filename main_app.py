import streamlit as st

st.set_page_config(page_title="QuoteForge", page_icon="🔥", layout="wide")

col_logo, col_title, col_auth = st.columns([1, 4, 2])

with col_logo:
    st.image("images/quoteforge_logo.png", width=160)

with col_title:
    st.markdown("# QuoteForge")
    st.markdown("**Engineering Precision. Forged Fast.**")

st.markdown("---")
st.markdown("### Fast, Accurate Preliminary Designs for Quoting")

st.subheader("Choose Design Category")

col1, _, _ = st.columns(3)

with col1:
    st.markdown("### 🏗️ Cranes & Lifting")
    st.page_link("pages/spreader_beam_app.py", label="Design Spreader Beam", icon="🔧", use_container_width=True)
    st.page_link("pages/lifting_beam_app.py", label="Design Lifting Beam", icon="🔧", use_container_width=True)
    st.page_link("pages/jib_crane_app.py", label="Design Jib Crane", icon="🔧", use_container_width=True)

st.caption("© QuoteForge • Preliminary designs only")
