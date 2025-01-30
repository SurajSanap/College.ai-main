import openai
import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from threading import Thread, Event
from langdetect import detect
from googletrans import Translator
from dotenv import load_dotenv
import os
import time
import json
from streamlit_lottie import st_lottie
from tempfile import NamedTemporaryFile

# Initialize translator
translator = Translator()

# Global flags
is_speaking = False
stop_event = Event()

def main():
    # Animation Section
    try:
        with open('src/Teacher1.json', encoding='utf-8') as anim_source:
            animation_data = json.load(anim_source)
            st_lottie(animation_data, height=200, key="About")
    except FileNotFoundError:
        st.error("Animation file not found. Please check the file path.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    # Load environment variables
    load_dotenv()

    # Streamlit app setup
    st.title("AI Interview")
    st.write("<p style='text-align: center;'>Powered by OpenAi</p>", unsafe_allow_html=True)

    # API Key Setup moved from the sidebar to the main page
    st.subheader("Setup")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

    if st.button("Set API Key"):
        if api_key:
            openai.api_key = api_key
            st.session_state["api_key"] = api_key
            st.success("API Key set successfully!")
        else:
            st.error("Please enter a valid API Key.")

    # Check if API key is set before proceeding
    if "api_key" not in st.session_state:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

    # Function for Speech-to-Text
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
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand. Please try again."
            except sr.RequestError as e:
                return f"Speech recognition error: {str(e)}"

    # Function for Chatbot Response
    def get_response(question):
        try:
            # Detect language
            language = detect(question)
            if language == "ja":
                translated_question = translator.translate(question, src="ja", dest="en").text
            else:
                translated_question = question  # Assume it's in English

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[ 
                    {"role": "system", "content": (
                        "You are an insightful and professional interviewer with a keen ability to engage guests in meaningful conversations.
                        Your goal is to ask thought-provoking, relevant, and well-structured questions that encourage deep discussion. 
                        You adapt your tone and style based on the interviewee's background, ensuring a smooth and engaging dialogue. Keep the conversation dynamic, 
                        ask thoughtful follow-ups, and maintain a professional yet personable approach"
                    )},
                    {"role": "user", "content": translated_question},
                ]
            )

            raw_response = response.choices[0].message["content"]

            if language == "ja":
                translated_response = translator.translate(raw_response, src="en", dest="ja").text
                return translated_response, "ja"
            else:
                return raw_response, "en"

        except openai.error.OpenAIError as e:
            st.error("You exceeded your current quota or faced an API issue. Please check your OpenAI account and billing details.")
            raise RuntimeError("Stopping the assistant due to API error.")
        except Exception as e:
            return f"An error occurred: {str(e)}", "en"

    # Function to speak the response using gTTS
    def speak_response(response, lang):
        global is_speaking

        def run_tts():
            global is_speaking
            is_speaking = True
            try:
                tts = gTTS(response, lang=lang)  # Dynamically set language
                audio_file = NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(audio_file.name)
                st.audio(audio_file.name, format="audio/mp3")
            except Exception as e:
                st.error(f"Error in text-to-speech: {e}")
            finally:
                is_speaking = False

        tts_thread = Thread(target=run_tts)
        tts_thread.start()

    # Real-time Voice Interaction
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
                    chatbot_response, lang = get_response(user_query)
                st.write(f"**Chatbot:** {chatbot_response}")

                # Speak the response
                speak_response(chatbot_response, lang)
        except RuntimeError as stop_error:
            st.warning(str(stop_error))
            st.write("Voice Assistant stopped due to an error.")

if __name__ == "__main__":
    main()
