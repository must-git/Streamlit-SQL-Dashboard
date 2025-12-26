import streamlit as st
import pandas as pd
from db.connection import get_connection

st.title("SQL Playground")
st.markdown("---")

query = st.text_area("Write SQL query")

if st.button("Run"):
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    except Exception as e:
        st.error(e)
