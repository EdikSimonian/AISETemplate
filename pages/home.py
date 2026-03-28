import streamlit as st

from lib.auth import get_current_user

user = get_current_user()

st.title("Workshop App")
st.write(f"Welcome, **{user.user_metadata.get('name', user.email)}**!")

st.divider()
st.write("👈 Use the sidebar to navigate.")
