import streamlit as st

from lib.auth import get_current_user

user = get_current_user()

st.title("Settings")
st.write(f"**Email:** {user.email}")
