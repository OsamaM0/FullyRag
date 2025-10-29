# Language and RTL Support

Covers default language initialization, session integration, and styling for RTL.

## Flow

- Read LANGUAGE from `.env`
- Map to code (`english→en`, `arabic→ar`)
- Load appropriate display_texts JSON
- Initialize `st.session_state.app_language`
- Apply CSS (LTR/RTL)
- Render pages using `dt` texts
- User can switch; session updates and triggers rerun

## Key files

- frontend/src/display_texts.py
- frontend/src/multilanguage_css.py
- frontend/src/session_manager.py
- frontend/src/streamlit-app.py

## RTL specifics

- Direction and fonts set via CSS for `[dir="rtl"]` or `[lang="ar"]`

## Configuration precedence

User selection → session state → `.env` LANGUAGE → default `en`
