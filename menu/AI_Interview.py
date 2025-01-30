import openai
import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from threading import Thread, Event
from dotenv import load_dotenv
import os
import time
import json
from streamlit_lottie import st_lottie
from tempfile import NamedTemporaryFile

# Global Flags
is_speaking = False
stop_event = Event()

# Load environment variables
load_dotenv()

# Function to Load and Display Animation
def load_animation():
    try:
        with open('src/Teacher1.json', encoding='utf-8') as anim_source:
            animation_data = json.load(anim_source)
            st_lottie(animation_data, height=200, key="animation")
    except FileNotFoundError:
        st.error("Animation file not found. Please check the file path.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to Recognize Speech
def recognize_speech():
    global is_speaking
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while is_speaking:
            time.sleep(0.1)
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            if stop_event.is_set():
                return "stop"
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand. Please try again."
        except sr.RequestError as e:
            return f"Speech recognition error: {str(e)}"

# Function to Generate Chatbot Response
def get_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[ 
                {"role": "system", "content": (
                    "You are an insightful and professional interviewer with a keen ability to engage guests in meaningful conversations. "
                    "Your goal is to ask thought-provoking, relevant, and well-structured questions that encourage deep discussion. "
                    "You adapt your tone and style based on the interviewee's background, ensuring a smooth and engaging dialogue. "
                    "Keep the conversation dynamic, ask thoughtful follow-ups, and maintain a professional yet personable approach."
                )},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message["content"]
    except openai.error.OpenAIError:
        st.error("You exceeded your current quota or faced an API issue. Please check your OpenAI account and billing details.")
        raise RuntimeError("Stopping the assistant due to API error.")
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to Speak the Response
def speak_response(response):
    global is_speaking

    def run_tts():
        global is_speaking
        is_speaking = True
        try:
            tts = gTTS(response, lang="en")
            audio_file = NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(audio_file.name)
            st.audio(audio_file.name, format="audio/mp3")
        except Exception as e:
            st.error(f"Error in text-to-speech: {e}")
        finally:
            is_speaking = False

    tts_thread = Thread(target=run_tts)
    tts_thread.start()

# Main Application
def main():
    # UI Setup
    st.title("AI Interview")
    st.write("<p style='text-align: center;'>Powered by OpenAI</p>", unsafe_allow_html=True)

    # Load animation
    load_animation()

    # API Key Input
    st.subheader("Setup")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

    if st.button("Set API Key"):
        if api_key:
            openai.api_key = api_key
            st.session_state["api_key"] = api_key
            st.success("API Key set successfully!")
        else:
            st.error("Please enter a valid API Key.")

    # Check API key before proceeding
    if "api_key" not in st.session_state:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

    # Start Voice Assistant
    if st.button("Start Voice Assistant"):
        st.write("Voice Assistant is active. Speak into your microphone.")
        stop_event.clear()
        try:
            while not stop_event.is_set():
                user_query = recognize_speech()
                if user_query.lower() == "stop":
                    st.write("Stopping the voice assistant.")
                    stop_event.set()
                    break

                st.write(f"**You said:** {user_query}")

                with st.spinner("Thinking..."):
                    chatbot_response = get_response(user_query)
                st.write(f"**Chatbot:** {chatbot_response}")

                # Speak the response
                speak_response(chatbot_response)
        except RuntimeError as stop_error:
            st.warning(str(stop_error))
            st.write("Voice Assistant stopped due to an error.")

if __name__ == "__main__":
    main()
