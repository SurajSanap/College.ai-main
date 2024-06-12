import streamlit as st
import json

st.set_page_config(page_title="College.ai", page_icon='src/Logo College.png', layout='wide', initial_sidebar_state="expanded")

# Load CSS file
st.markdown('<style>' + open('./src/style.css').read() + '</style>', unsafe_allow_html=True)

from streamlit_lottie import st_lottie
from st_on_hover_tabs import on_hover_tabs

from menu.About import main as about_page
from menu.AI_Lens import main as ai_lens_page
from menu.Ask_To_PDF import main as ask_to_pdf_page
from menu.ATS import main as ats_page
from menu.Prompt_Examples import main as prompt_examples_page
from menu.Resume_Analyser import main as resume_analyser_page
from menu.User import main as user_page

# Initialize session state for theme
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "light"

themes = {
    "light": {
        "base": "light",
        "backgroundColor": "white",
        "primaryColor": "#c19ad9",
        "secondaryBackgroundColor": "#c98bdb",
        "textColor": "black"
    },
    "dark": {
        "base": "dark",
        "backgroundColor": "black",
        "primaryColor": "#c98bdb",
        "secondaryBackgroundColor": "#c98bdb",
        "textColor": "white"
    }
}

# Change theme function
def change_theme():
    current_theme = st.session_state.current_theme
    new_theme = "dark" if current_theme == "light" else "light"
    st.session_state.current_theme = new_theme
    apply_theme()

# Apply theme changes
def apply_theme():
    theme_settings = themes[st.session_state.current_theme]
    for key, value in theme_settings.items():
        st._config.set_option(f'theme.{key}', value)

# Home Page Function
def home():
    st.markdown("<h1 style='text-align: center;'>Welcome to College.ai!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>AI-powered System for Students</h4>", unsafe_allow_html=True)

    try:
        with open('src/Home_student.json', encoding='utf-8') as anim_source:
            animation_data = json.load(anim_source)
        st_lottie(animation_data, 1, True, True, "high", 350, -200)
    except FileNotFoundError:
        st.error("Animation file not found.")
    except UnicodeDecodeError as e:
        st.error(f"Error decoding JSON: {e}. Try specifying a different encoding.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("<a href='https://devpost.com/software/college-ai-m3o0bx' target='_blank'><button style='color: white; background-color: #4CAF50; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;'>Tutorial</button></a>", unsafe_allow_html=True)

# Main Function
def main():
    st.markdown("""
        <style>
            /* Reduce padding for the entire page */
            .css-1y0tads, .block-container, .css-1lcbmhc {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Display theme change button within the sidebar
        st.image('src/Logo College.png', width=70)
       
        btn_face = "🌞" if st.session_state.current_theme == "light" else "🌜"
        if st.button(btn_face):
            change_theme()
        apply_theme()
        tabs = on_hover_tabs(
            tabName=['Home', 'AI Lens', 'Ask To PDF', 'Resume Analyser', 'ATS', 'Prompt Examples', 'About', 'Account'], 
            iconName=['home', 'center_focus_weak', 'search', 'article', 'work', 'edit', 'info', 'account_circle'], 
            default_choice=0
        )

    menu = {
        'Home': home,
        'AI Lens': ai_lens_page,
        'Ask To PDF': ask_to_pdf_page,
        'Resume Analyser': resume_analyser_page,
        'ATS': ats_page,
        'Prompt Examples': prompt_examples_page,
        'About': about_page,
        'Account': user_page,
    }
    
    menu[tabs]()

if __name__ == "__main__":
    main()
