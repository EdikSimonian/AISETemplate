import streamlit as st

from lib.auth import login

st.set_page_config(page_title="Log in", layout="centered")
st.title("Log in")

with st.form("login"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Log in", use_container_width=True)

if submitted:
    if not email or not password:
        st.error("Email and password are required.")
    else:
        user = login(email, password)
        if user:
            st.success("Logged in!")
            st.switch_page("app.py")
        else:
            st.error("Invalid email or password.")

st.divider()
st.write("Don't have an account?")
if st.button("Sign up"):
    st.switch_page("pages/2_Signup.py")
