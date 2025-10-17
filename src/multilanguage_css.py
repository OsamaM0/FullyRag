"""
Multi-language CSS enhancements for PolyRAG
Adds proper RTL (Right-to-Left) support for Arabic and other RTL languages
"""

# RTL Language Support CSS
RTL_CSS = """
<style>
    /* RTL Support for Arabic */
    [dir="rtl"] {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for Streamlit containers */
    [dir="rtl"] .stMarkdown,
    [dir="rtl"] .stText,
    [dir="rtl"] .stButton > button {
        text-align: right;
    }
    
    /* RTL for chat messages */
    [dir="rtl"] .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for input fields */
    [dir="rtl"] input,
    [dir="rtl"] textarea {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL for selectbox */
    [dir="rtl"] .stSelectbox {
        direction: rtl;
    }
    
    /* Flip icons for RTL */
    [dir="rtl"] .material-icons {
        transform: scaleX(-1);
    }
    
    /* RTL for sidebar */
    [dir="rtl"] section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    
    /* Preserve LTR for code blocks */
    [dir="rtl"] code,
    [dir="rtl"] pre {
        direction: ltr;
        text-align: left;
    }
    
    /* Language selector styling */
    .language-selector {
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
    }
    
    /* Smooth transitions for language switch */
    .stMarkdown,
    .stButton,
    .stTextInput,
    .stSelectbox {
        transition: all 0.3s ease;
    }
</style>
"""

# Language-specific font support
FONT_CSS = """
<style>
    /* Arabic font support */
    [lang="ar"] {
        font-family: 'Segoe UI', 'Dubai', 'Tahoma', 'Arial', sans-serif;
        font-size: 1.05em; /* Slightly larger for better Arabic readability */
    }
    
    /* English font */
    [lang="en"] {
        font-family: 'Source Sans Pro', 'Segoe UI', sans-serif;
    }
    
    /* Ensure proper font rendering for mixed content */
    .mixed-content {
        font-family: 'Segoe UI', 'Dubai', sans-serif;
    }
</style>
"""

# Complete CSS for multi-language support
COMPLETE_MULTILANG_CSS = RTL_CSS + FONT_CSS


def get_language_css(language_code: str) -> str:
    """
    Get CSS for specific language
    
    Args:
        language_code: Language code (e.g., 'en', 'ar')
        
    Returns:
        CSS string for the language
    """
    rtl_languages = ['ar', 'he', 'fa', 'ur']  # RTL languages
    
    if language_code in rtl_languages:
        return f"""
        <style>
            body {{
                direction: rtl;
            }}
            .stApp {{
                direction: rtl;
            }}
        </style>
        {COMPLETE_MULTILANG_CSS}
        """
    else:
        return f"""
        <style>
            body {{
                direction: ltr;
            }}
            .stApp {{
                direction: ltr;
            }}
        </style>
        {FONT_CSS}
        """


def apply_language_styles(st_module, language_code: str):
    """
    Apply language-specific styles to Streamlit app
    
    Args:
        st_module: Streamlit module
        language_code: Language code (e.g., 'en', 'ar')
    """
    css = get_language_css(language_code)
    st_module.markdown(css, unsafe_allow_html=True)


# Example usage in Streamlit app:
"""
import streamlit as st
from multilanguage_css import apply_language_styles

# In your main app
current_language = st.session_state.get('app_language', 'en')
apply_language_styles(st, current_language)
"""
