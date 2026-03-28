import streamlit as st


def hide_chrome() -> None:
    """Hide Streamlit's default menu, footer, header, and status widget.

    Uses body opacity trick to prevent flash-of-unstyled-content: the body
    starts invisible and fades in only after the hiding CSS has been applied.
    """
    st.markdown(
        """
        <style>
        /* Hide chrome immediately when this style block is parsed */
        #MainMenu,
        footer,
        header,
        [data-testid="stStatusWidget"],
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* Fade the body in to prevent flash of hidden elements */
        body {
            opacity: 0;
            animation: fadeIn 0.15s ease-in forwards;
        }
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
