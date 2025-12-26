import streamlit as st

st.set_page_config(
    page_title="SQLite Dashboard",
    layout="wide",
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("SQLite Practice Dashboard")
st.markdown("---")