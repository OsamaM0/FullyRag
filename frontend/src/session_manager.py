"""
Session management for authentication persistence.
This module handles session state initialization and persistence.
"""

import hashlib
import time

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def init_session_state():
    """Initialize session state variables if they don't exist."""
    # Initialize app language from .env if not already set
    if "app_language" not in st.session_state:
        from display_texts import get_current_language

        st.session_state.app_language = get_current_language()

    # Authentication state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "refresh_token" not in st.session_state:
        st.session_state.refresh_token = None

    if "current_user_id" not in st.session_state:
        st.session_state.current_user_id = None

    if "current_user_email" not in st.session_state:
        st.session_state.current_user_email = None

    # Conversation state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    if "conversation_title" not in st.session_state:
        st.session_state.conversation_title = None

    # Agent client state
    if "agent_client" not in st.session_state:
        st.session_state.agent_client = None

    # Session tracking - used to detect new sessions
    if "session_id" not in st.session_state:
        # Create a unique session ID based on timestamp and random value
        st.session_state.session_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()
        st.session_state.session_start_time = time.time()


def check_session_timeout(timeout_seconds: int = 3600) -> bool:
    """
    Check if the session has timed out.

    Args:
        timeout_seconds: Timeout duration in seconds (default: 1 hour)

    Returns:
        True if session has timed out, False otherwise
    """
    if "session_start_time" not in st.session_state:
        return True

    elapsed_time = time.time() - st.session_state.session_start_time
    return elapsed_time > timeout_seconds


def update_session_activity():
    """Update the last activity time for the session."""
    st.session_state.session_start_time = time.time()
