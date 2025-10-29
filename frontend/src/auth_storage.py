"""
Authentication storage helper to persist tokens across page interactions and reloads.

This module stores auth in both Streamlit session_state (for fast access) and
browser cookies via streamlit-cookies-controller (to survive full page reloads
and new Streamlit sessions in the same browser tab).
"""

import streamlit as st

try:
    # The package is declared in pyproject and should be available
    from streamlit_cookies_controller import CookieController  # type: ignore
except Exception:  # pragma: no cover - optional dependency safeguards
    CookieController = None  # type: ignore


COOKIE_KEYS = {
    "access_token": "polyrag_access_token",
    "refresh_token": "polyrag_refresh_token",
    "current_user_id": "polyrag_user_id",
    "current_user_email": "polyrag_user_email",
    "authenticated": "polyrag_authenticated",
}


def _get_cookie_controller():
    """Return a CookieController instance or None if unavailable."""
    if CookieController is None:
        return None
    # Keep a single controller in session_state to avoid multiple instances
    if "_cookie_controller" not in st.session_state:
        st.session_state._cookie_controller = CookieController()
    return st.session_state._cookie_controller


def _write_cookies(access_token: str, refresh_token: str, user_id: str, email: str) -> None:
    controller = _get_cookie_controller()
    if not controller:
        return
    # Session cookies (expire when browser/tab closes). Avoid secure/httponly here since
    # the controller reads cookies client-side; secure cookies would be inaccessible in JS.
    controller.set(COOKIE_KEYS["access_token"], access_token)
    controller.set(COOKIE_KEYS["refresh_token"], refresh_token)
    controller.set(COOKIE_KEYS["current_user_id"], user_id)
    controller.set(COOKIE_KEYS["current_user_email"], email)
    controller.set(COOKIE_KEYS["authenticated"], "1")


def _read_cookies_into_session() -> bool:
    controller = _get_cookie_controller()
    if not controller:
        return False
    cookies = controller.getAll() or {}
    access_token = cookies.get(COOKIE_KEYS["access_token"]) or None
    user_id = cookies.get(COOKIE_KEYS["current_user_id"]) or None
    if not access_token or not user_id:
        return False

    # Hydrate session_state from cookies
    st.session_state.access_token = access_token
    st.session_state.refresh_token = cookies.get(COOKIE_KEYS["refresh_token"]) or None
    st.session_state.current_user_id = user_id
    st.session_state.current_user_email = cookies.get(COOKIE_KEYS["current_user_email"]) or None
    st.session_state.authenticated = True
    return True


def _clear_cookies() -> None:
    controller = _get_cookie_controller()
    if not controller:
        return
    for key in COOKIE_KEYS.values():
        try:
            controller.remove(key)
        except Exception:
            # Ignore cookie removal errors to avoid blocking logout
            pass


def save_auth_to_session(access_token: str, refresh_token: str, user_id: str, email: str) -> None:
    """
    Save authentication data to session state and cookies.

    Args:
        access_token: JWT access token
        refresh_token: JWT refresh token
        user_id: User ID
        email: User email
    """
    # Save to session_state
    st.session_state.access_token = access_token
    st.session_state.refresh_token = refresh_token
    st.session_state.current_user_id = user_id
    st.session_state.current_user_email = email
    st.session_state.authenticated = True

    # Persist to cookies to survive reloads
    _write_cookies(access_token, refresh_token, user_id, email)


def load_auth_from_session() -> bool:
    """
    Ensure authentication data is loaded into session_state.
    First checks session_state, then attempts to hydrate from cookies.

    Returns:
        True if auth data exists/loaded, False otherwise
    """
    in_session = (
        st.session_state.get("authenticated")
        and st.session_state.get("access_token")
        and st.session_state.get("current_user_id")
    )
    if in_session:
        return True
    # Try cookies fallback
    return _read_cookies_into_session()


def clear_auth_from_session() -> None:
    """
    Clear all authentication data from session state and cookies.
    """
    keys_to_clear = [
        "access_token",
        "refresh_token",
        "current_user_id",
        "current_user_email",
        "authenticated",
        "agent_client",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Also clear cookies so reload won't auto-login
    _clear_cookies()


def is_authenticated() -> bool:
    """
    Check if user is authenticated, hydrating from cookies if needed.

    Returns:
        True if user is authenticated, False otherwise
    """
    return load_auth_from_session()


def get_access_token() -> str | None:
    """
    Get the current access token from session state, hydrating from cookies if needed.

    Returns:
        Access token if available, None otherwise
    """
    if not st.session_state.get("access_token"):
        load_auth_from_session()
    return st.session_state.get("access_token")


def get_user_id() -> str | None:
    """
    Get the current user ID from session state, hydrating from cookies if needed.

    Returns:
        User ID if available, None otherwise
    """
    if not st.session_state.get("current_user_id"):
        load_auth_from_session()
    return st.session_state.get("current_user_id")
