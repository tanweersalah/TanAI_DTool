import streamlit as st
from streamlit_router import StreamlitRouter 




# Access specific parameters
containerid = st.query_params.get("containerid", ["1"])[0]  

st.write(f"Current page: {containerid}")

    