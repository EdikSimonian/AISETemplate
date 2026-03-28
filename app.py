import streamlit as st

from lib.auth import get_current_user

st.set_page_config(
    page_title="Workshop App",
    page_icon="🚀",
    layout="centered",
)

user = get_current_user()

if user:
    pg = st.navigation(
        [
            st.Page("pages/home.py", title="Home", icon="🏠"),
        ]
    )
else:
    pg = st.navigation(
        [
            st.Page("pages/1_Login.py", title="Log in"),
            st.Page("pages/2_Signup.py", title="Sign up"),
        ]
    )

pg.run()
