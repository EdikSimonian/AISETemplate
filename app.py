import streamlit as st

from lib.auth import get_current_user

st.set_page_config(
    page_title="Workshop App",
    page_icon="🚀",
    layout="centered",
)

# ------------------------------------------------------------------
# Auth gate — redirect to login if no active session
# ------------------------------------------------------------------
user = get_current_user()

if not user:
    st.title("Welcome")
    st.info("Please log in or sign up to continue.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log in", use_container_width=True):
            st.switch_page("pages/1_Login.py")
    with col2:
        if st.button("Sign up", use_container_width=True):
            st.switch_page("pages/2_Signup.py")
    st.stop()

# ------------------------------------------------------------------
# Main app — shown after login
# ------------------------------------------------------------------
st.title("Workshop App")
st.write(f"Welcome, **{user.user_metadata.get('name', user.email)}**!")

if st.button("Log out"):
    from lib.auth import logout
    logout()
    st.rerun()

st.divider()
st.write("👈 Use the sidebar to navigate.")
