import logging
import os

import streamlit as st
from dotenv import load_dotenv

from auth_storage import (
    clear_auth_from_session,
    is_authenticated,
    load_auth_from_session,
    save_auth_to_session,
)
from client import AgentClient, AgentClientError
from display_texts import dt, get_current_language
from multilanguage_css import apply_language_styles
from session_manager import init_session_state

load_dotenv()

logger = logging.getLogger(__name__)

NO_AUTH = os.getenv("NO_AUTH", "False").lower() in ("true", "1", "yes")
AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8080")


def login_ui():
    """
    Secure login UI using backend JWT authentication.
    """
    # Initialize session state
    init_session_state()

    # Apply language-specific CSS
    current_language = st.session_state.get("app_language", get_current_language())
    apply_language_styles(st, current_language)

    st.title(dt.LOGIN_WELCOME)

    if "login_success_message" in st.session_state:
        st.success(st.session_state["login_success_message"])
        del st.session_state["login_success_message"]

    if "login_error_message" in st.session_state:
        st.error(st.session_state["login_error_message"])
        del st.session_state["login_error_message"]

    # Create tabs for login and register
    login_tab = f"🔑 {dt.LOGIN_BUTTON}"
    register_tab = f"📝 {dt.CREATE_ACCOUNT_BUTTON}"
    tab1, tab2 = st.tabs([login_tab, register_tab])

    with tab1:
        st.subheader(dt.LOGIN_BUTTON)

        email = st.text_input(
            dt.LOGIN_EMAIL_PROMPT,
            key="login_email_input",
            value=st.session_state.get("email", ""),
        )
        password = st.text_input(
            dt.LOGIN_PASSWORD_PROMPT, type="password", key="login_password_input"
        )

        col1, col2 = st.columns(2)

        with col1:
            login_btn = f"🔓 {dt.LOGIN_BUTTON}"
            if st.button(login_btn, type="primary", use_container_width=True):
                if not email or not password:
                    st.error(dt.LOGIN_FAILED)
                else:
                    try:
                        # Create client and login
                        client = AgentClient(base_url=AGENT_URL, get_info=False)
                        login_data = client.login(email, password)

                        # Store authentication using the new storage helper
                        save_auth_to_session(
                            access_token=login_data["access_token"],
                            refresh_token=login_data["refresh_token"],
                            user_id=login_data["user_id"],
                            email=login_data["email"],
                        )

                        success_msg = f"✅ {email}"
                        st.session_state["login_success_message"] = success_msg
                        st.rerun()
                        return True
                    except AgentClientError as e:
                        st.error(f"❌ {dt.LOGIN_FAILED}")
                        logger.error(f"Login error: {e}")
                    except Exception as e:
                        st.error(f"❌ {dt.LOGIN_FAILED}")
                        logger.error(f"Unexpected login error: {e}")

        with col2:
            reset_btn = f"🔑 {dt.RESET_PASSWORD_BUTTON}"
            if st.button(reset_btn, use_container_width=True):
                st.info(dt.RESET_PASSWORD_BUTTON)

    with tab2:
        st.subheader(dt.CREATE_ACCOUNT_BUTTON)

        reg_email = st.text_input(dt.LOGIN_EMAIL_PROMPT, key="register_email_input")
        reg_password = st.text_input(
            dt.LOGIN_PASSWORD_PROMPT, type="password", key="register_password_input"
        )
        reg_password_confirm = st.text_input(
            dt.LOGIN_PASSWORD_PROMPT,
            type="password",
            key="register_password_confirm_input",
        )

        create_btn = f"📝 {dt.CREATE_ACCOUNT_BUTTON}"
        if st.button(create_btn, type="primary", use_container_width=True):
            if not reg_email or not reg_password or not reg_password_confirm:
                st.error(dt.ACCOUNT_CREATION_FAILED)
            elif reg_password != reg_password_confirm:
                st.error(dt.ACCOUNT_CREATION_FAILED)
            elif len(reg_password) < 8:
                st.error(dt.ACCOUNT_CREATION_FAILED)
            else:
                try:
                    # Create client and register
                    client = AgentClient(base_url=AGENT_URL, get_info=False)
                    register_data = client.register(reg_email, reg_password)

                    success_msg = dt.ACCOUNT_CREATED_SUCCESS.format(email=reg_email)
                    st.success(success_msg)
                    st.session_state["email"] = reg_email
                    default_msg = dt.ACCOUNT_CREATED_SUCCESS.format(email=reg_email)
                    st.session_state["login_success_message"] = register_data.get(
                        "message", default_msg
                    )
                    st.rerun()
                except AgentClientError as e:
                    st.error(dt.ACCOUNT_CREATION_FAILED)
                    logger.error(f"Registration error: {e}")
                except Exception as e:
                    st.error(dt.ACCOUNT_CREATION_FAILED)
                    logger.error(f"Unexpected registration error: {e}")

    st.divider()
    st.caption(dt.WARNING_MESSAGE)

    return False


def logout():
    """Logout and clear all authentication data."""
    # Clear authentication using the storage helper
    clear_auth_from_session()

    # Clear conversation-related data
    keys_to_clear = [
        "messages",
        "thread_id",
        "conversation_title",
        "pdf_to_view",
        "annotations",
        "graphs",
        "suggested_command",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Clear thread_id from query params but keep auth cleared
    if "thread_id" in st.query_params:
        del st.query_params["thread_id"]

    if "show_user_modal" in st.session_state:
        st.session_state["show_user_modal"] = False
    st.rerun()


def ensure_authenticated():
    """
    Ensure the user is authenticated. If not, show login UI.
    Returns True if authenticated, False otherwise.
    """
    if NO_AUTH:
        default_id = "00000000-0000-0000-0000-000000000001"
        st.session_state.current_user_id = st.session_state.get("current_user_id", default_id)
        st.session_state.current_user_email = st.session_state.get(
            "current_user_email", "admin@admin"
        )
        return True

    # Fast path: already in memory
    if is_authenticated():
        return True

    # First-time hydration from cookies after a hard reload
    # Do this only once to avoid flicker/loops
    if not st.session_state.get("_auth_cookie_checked", False):
        st.session_state["_auth_cookie_checked"] = True
        if load_auth_from_session():
            # Cookies were found; rerun to ensure all downstream
            # code sees hydrated state
            st.rerun()
            return True

    # Not authenticated, show login UI
    if not login_ui():
        st.stop()
    else:
        return True
