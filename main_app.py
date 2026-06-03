import streamlit as st

st.set_page_config(page_title="QuoteForge", page_icon="🔥", layout="wide")

st.title("QuoteForge")
st.markdown("**Engineering Precision. Forged Fast.**")

st.markdown("---")
st.subheader("Choose Design Category")

st.page_link("pages/spreader_beam_app.py", label="Design Spreader Beam", icon="🔧", use_container_width=True)
st.page_link("pages/lifting_beam_app.py", label="Design Lifting Beam", icon="🔧", use_container_width=True)
st.page_link("pages/jib_crane_app.py", label="Design Jib Crane", icon="🔧", use_container_width=True)
