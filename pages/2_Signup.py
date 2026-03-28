import streamlit as st

from lib.auth import signup

st.set_page_config(page_title="Sign up", layout="centered")
st.title("Create an account")

with st.form("signup"):
    name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", help="Minimum 6 characters")
    submitted = st.form_submit_button("Create account", use_container_width=True)

if submitted:
    if not name or not email or not password:
        st.error("All fields are required.")
    elif len(password) < 6:
        st.error("Password must be at least 6 characters.")
    else:
        user = signup(email, password, name)
        if user:
            st.success(
                "Account created! Please check your email to confirm, then log in."
            )
            if st.button("Go to login"):
                st.switch_page("pages/1_Login.py")
        else:
            st.error("Could not create account. This email may already be registered.")

st.divider()
st.write("Already have an account?")
if st.button("Log in"):
    st.switch_page("pages/1_Login.py")
