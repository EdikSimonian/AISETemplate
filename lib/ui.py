import streamlit as st


def hide_chrome() -> None:
    """Hide Streamlit's default menu, footer, and header bar."""
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )
