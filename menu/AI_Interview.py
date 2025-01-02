import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("AI Interview")
    components.iframe(
        src="https://yumelearn.streamlit.app/Sensei_Talk?embed=true",
        height=600,
    )

if __name__ == "__main__":
    main()