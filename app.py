import streamlit as st

from lib.auth import confirm_email, get_current_user, logout

st.set_page_config(
    page_title="Workshop App",
    page_icon="🚀",
    layout="centered",
)

# Handle email confirmation link (?token_hash=...&type=signup)
if "token_hash" in st.query_params and not st.session_state.get("user"):
    user, error = confirm_email(
        st.query_params["token_hash"],
        st.query_params.get("type", "signup"),
    )
    if user:
        st.query_params.clear()
        st.rerun()
    else:
        st.error(f"Confirmation failed: {error}")
        st.stop()

user = get_current_user()

if user:
    pg = st.navigation(
        [
            st.Page("pages/home.py", title="Home", icon=":material/home:"),
            st.Page("pages/settings.py", title="Settings", icon=":material/settings:"),
        ]
    )
    with st.sidebar:
        st.divider()
        if st.button("Log out", use_container_width=True):
            logout()
            st.rerun()
else:
    pg = st.navigation(
        [
            st.Page("pages/1_Login.py", title="Log in"),
            st.Page("pages/2_Signup.py", title="Sign up"),
        ]
    )

pg.run()
