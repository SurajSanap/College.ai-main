import streamlit as st

st.set_page_config("College.ai", page_icon="src/Logo College.png", layout="centered")
st.markdown(
    "<style>" + open("./src/style.css").read() + "</style>", unsafe_allow_html=True
)

import json

from st_on_hover_tabs import on_hover_tabs
from streamlit_lottie import st_lottie

from menu.About import main as about_page
from menu.AI_Lens import main as ai_lens_page
from menu.Ask_To_PDF import main as ask_to_pdf_page
from menu.ATS import main as ats_page
from menu.Prompt_Examples import main as prompt_examples_page
from menu.Resume_Analyser import main as resume_analyser_page
from menu.User import main as user_page


def home():
    """
    The `home()` function in Python displays a welcome message, loads and displays an animation from a
    JSON file, and includes a link to a tutorial.
    """
    st.markdown(
        "<h1 style='text-align: center;'>Welcome to College.ai!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style='text-align: center;'>AI-powered System for Students</h4>",
        unsafe_allow_html=True,
    )

    try:
        with open("src/Home_student.json", encoding="utf-8") as anim_source:
            animation_data = json.load(anim_source)
        st_lottie(animation_data, 1, True, True, "high", 350, -200)
    except FileNotFoundError:
        st.error("Animation file not found.")
    except UnicodeDecodeError as e:
        st.error(f"Error decoding JSON: {e}. Try specifying a different encoding.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.markdown(
        "<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True
    )
    st.markdown(
        "<a href='https://devpost.com/software/college-ai-m3o0bx' target='_blank'><button style='color: white; background-color: #4CAF50; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;'>Tutorial</button></a>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """
    The `main` function in the provided Python code sets up a Streamlit app with a customized style and
    a sidebar containing tabs for different pages, each linked to a specific function.
    """

    st.markdown(
        """
        <style>
            /* Target the root container and reduce its padding */
            .css-1y0tads {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
            
            /* Further reduce padding within the main block container */
            .block-container {
                padding-top: 0px !important;
                margin-top: 0px !important;
                padding-bottom: 0px !important;
                margin-bottom: 0px !important;
            }

            /* Reduce space around the main area */
            .css-1lcbmhc {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }

            /* Adjust Streamlit markdown blocks to reduce top margin */
            .stMarkdown {
                margin-top: 0px !important;
            }
                
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.image("src/Logo College.png", width=70)
        tabs = on_hover_tabs(
            tabName=[
                "Home",
                "AI Lens",
                "Ask To PDF",
                "Resume Analyser",
                "ATS",
                "Prompt Examples",
                "About",
                "Account",
            ],
            iconName=[
                "home",
                "center_focus_weak",
                "search",
                "article",
                "work",
                "edit",
                "info",
                "account_circle",
            ],
            default_choice=0,
        )

    menu = {
        "Home": home,
        "AI Lens": ai_lens_page,
        "Ask To PDF": ask_to_pdf_page,
        "Resume Analyser": resume_analyser_page,
        "ATS": ats_page,
        "Prompt Examples": prompt_examples_page,
        "About": about_page,
        "Account": user_page,
    }

    menu[tabs]()


if __name__ == "__main__":
    main()
