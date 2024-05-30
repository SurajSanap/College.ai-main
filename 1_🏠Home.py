import streamlit as st
from streamlit_lottie import st_lottie 
from st_on_hover_tabs import on_hover_tabs
import json

from menu.About import main as about_page
from menu.AI_Lens import main as ai_lens_page
from menu.Ask_To_PDF import main as ask_to_pdf_page
from menu.ATS import main as ats_page
from menu.Prompt_Examples import main as prompt_examples_page
from menu.Resume_Analyser import main as resume_analyser_page
from menu.User import main as user_page

#st.set_page_config("College.ai", page_icon='src/Logo College.png', layout='centered')
st.markdown('<style>' + open('./src/style.css').read() + '</style>', unsafe_allow_html=True)

def home():
    st.header(" Welcome to College.ai!")
    st.write("AI powered System for Students")

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

    st.link_button('Tutorial', "https://devpost.com/software/college-ai-m3o0bx")


def main():
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'AI Lens', 'Ask To PDF', 'Resume Analyser', 'ATS', 'Prompt Examples', 'About', 'Person'], 
                            iconName=['home', 'center_focus_weak', 'search', 'article', 'work', 'edit', 'info', 'account_circle'], 
                            default_choice=0)

    menu = {
        'Home': home,
        'AI Lens': ai_lens_page,
        'Ask To PDF': ask_to_pdf_page,
        'Resume Analyser': resume_analyser_page,
        'ATS': ats_page,
        'Prompt Examples': prompt_examples_page,
        'About': about_page,
        'Person': user_page
    }
    
    menu[tabs]()

if __name__ == "__main__":
    main()
