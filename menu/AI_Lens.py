import io
import json
import os

import google.ai.generativelanguage as glm
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from streamlit_lottie import st_lottie

load_dotenv()


def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


def main():

    st.write(
        "<h1><center>Virtual Assistant Interface</center></h1>", unsafe_allow_html=True
    )
    st.write("")

    gemini_pro, gemini_vision = st.tabs(["ChatBot", "Ai Lens"])

    with gemini_pro:
        st.header("ChatBot Tab")
        st.write("")
        with open("src/AI Lens.json", encoding="utf-8") as anim_source:
            animation = json.load(anim_source)
            st_lottie(animation, 1, True, True, "high", 200, -200)

        prompt = st.text_input(
            "prompt please...", placeholder="Prompt", label_visibility="visible"
        )
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND", use_container_width=True):
            response = model.generate_content(prompt)

            st.write("")
            st.header(":blue[Response]")
            st.write("")

            st.markdown(response.text)

    with gemini_vision:
        st.header("Ai Lens Tab")
        st.write("")
        with open("src/AI Lens.json", encoding="utf-8") as anim_source:
            animation = json.load(anim_source)
            st_lottie(animation, 1, True, True, "high", 200, -200)

        image_prompt = st.text_input(
            "Interact with the Image", placeholder="Prompt", label_visibility="visible"
        )
        uploaded_file = st.file_uploader(
            "Choose and Image",
            accept_multiple_files=False,
            type=["png", "jpg", "jpeg", "img", "webp"],
        )

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown(
                """
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """,
                unsafe_allow_html=True,
            )

        if st.button("GET RESPONSE", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts=[
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image),
                                    )
                                ),
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[Response]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")


if __name__ == "__main__":
    main()
