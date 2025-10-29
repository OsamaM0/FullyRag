import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from auth_helpers import login_ui
from display_texts import dt, get_current_language, set_language

# Apply language-specific CSS at the app level
from multilanguage_css import apply_language_styles
from session_manager import init_session_state

load_dotenv()

# Initialize session state at startup
init_session_state()


current_language = st.session_state.get("app_language", get_current_language())
apply_language_styles(st, current_language)

# Ensure language is set globally
if current_language != get_current_language():
    set_language(current_language)

if dt.LOGO:
    if dt.BIG_LOGO:
        custom_css = """
        <style>
            div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
                height: 3rem;
                width: auto;
            }
            div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
            div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
                display: flex;
                align-items: center;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

    # Resolve logo path relative to the frontend directory
    logo_path = Path(dt.LOGO)
    if not logo_path.is_absolute():
        # If running from root, prepend 'frontend/' to the path
        frontend_logo = Path(__file__).parent.parent / dt.LOGO
        if frontend_logo.exists():
            logo_path = frontend_logo
        else:
            logo_path = Path(dt.LOGO)

    st.logo(image=str(logo_path), size="large")

NO_AUTH = os.getenv("NO_AUTH", False)
NO_AUTH = False
if NO_AUTH:
    st.session_state.current_user_id = st.session_state.get(
        "current_user_id", "00000000-0000-0000-0000-000000000001"
    )
    st.session_state.current_user_email = st.session_state.get("current_user_email", "admin@admin")

chatbot = st.Page("frontend/chat.py", title=dt.ASSISTANT, icon=":material/chat:", default=True)
logout_page = st.Page("frontend/user.py", title=dt.LOGOUT, icon=":material/logout:")
comments = st.Page("frontend/feedback.py", title=dt.FEEDBACK, icon=":material/feedback:")

if "current_user_id" in st.session_state:
    pg = st.navigation(
        {
            "": [chatbot],
            "User": [logout_page, comments],
        },
    )
else:

    pg = st.navigation(pages=[st.Page(login_ui, title="Log in", icon=":material/login:")])

pg.run()
