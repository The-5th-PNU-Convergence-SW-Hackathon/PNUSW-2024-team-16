from contextlib import contextmanager
import streamlit as st
import streamlit.components.v1 as components

st.write("text outside the container")
with st.container():
    st.write("text inside the container")

st.write("More text outside the container")


st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div[style*="flex-direction: column;"] div[data-testid="stVerticalBlock"] {
        border: 1px solid red;
    }
</style>
""",
    unsafe_allow_html=True,
)
