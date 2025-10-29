import streamlit as st

from auth_helpers import ensure_authenticated, logout
from display_texts import dt, get_current_language
from multilanguage_css import apply_language_styles
from session_manager import init_session_state

# Initialize session state
init_session_state()

# Apply language-specific CSS
current_language = st.session_state.get("app_language", get_current_language())
apply_language_styles(st, current_language)

if not ensure_authenticated():
    st.stop()


if "current_user_email" in st.session_state:
    st.markdown(f":material/account_circle: {dt.LOGGED_AS}: {st.session_state.current_user_email}")
else:
    st.warning(dt.get("USER_PROFILE_NO_EMAIL_WARNING", "Warning: Email information not available."))

if st.button(dt.LOGOUT_BUTTON, key="logout_button_profile_page", type="primary"):
    logout()
