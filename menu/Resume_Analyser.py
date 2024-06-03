import asyncio
import json
import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from PyPDF2 import PdfReader
from streamlit_lottie import st_lottie

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    """
    The function `get_pdf_text` takes a list of PDF documents, extracts text from each page of the
    documents, and returns the concatenated text as a single string.

    Args:
      pdf_docs: It looks like the code snippet you provided is a function named `get_pdf_text` that
    takes a list of PDF documents as input and extracts text from each page of the PDF documents using
    the `PdfReader` class. The extracted text is then concatenated and returned as a single string.

    Returns:
      The function `get_pdf_text` returns the combined text content extracted from all the pages of the
    PDF documents provided in the `pdf_docs` list.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def get_text_chunks(text):
    """
    The function `get_text_chunks` splits a given text into chunks of 1000 characters with a
    200-character overlap using a RecursiveCharacterTextSplitter.

    Args:
      text: The `get_text_chunks` function takes a text input and splits it into chunks of 1000
    characters with an overlap of 200 characters using the `RecursiveCharacterTextSplitter` class. If
    you provide me with the text input, I can demonstrate how the function works by splitting the text
    into

    Returns:
      The function `get_text_chunks` returns a list of text chunks that are split from the input text
    based on the specified chunk size and overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """
    The function `get_vector_store` generates embeddings for text chunks using Google Generative AI
    Embeddings and saves them in a FAISS index.

    Args:
      text_chunks: Text chunks are small pieces of text that have been divided or segmented from a
    larger body of text. These chunks can be individual sentences, paragraphs, or any other division of
    text that is used for analysis or processing.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def load_vector_store():
    """
    The function `load_vector_store` loads a vector store using Google Generative AI embeddings and a
    FAISS index.

    Returns:
      A vector store is being returned.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    return vector_store


async def get_conversational_chain():
    """
    This Python function defines an asynchronous function that generates a conversational chain using a
    prompt template and a chat model to provide answers based on a given context.

    Returns:
      The `get_conversational_chain` function returns a conversational chain that uses a prompt template
    to interact with a ChatGoogleGenerativeAI model. The chain is loaded with a specific type ("stuff")
    and prompt template that includes a context variable for input. The model is set to "gemini-pro"
    with a temperature of 0.3 for generating responses based on the provided context.
    """
    prompt_template = """
    You are an Advanced resume Analyzer.
    1. Analyze the resume and give the best 3 job domains relevant to the skills in the given context.
    2. Based on those job domains, separately suggest more skills and best courses from YouTube.
    3. Suggest improvements in the resume.
    4. Use bullet points, tables, and keep the text more interactive.
    5. Ensure the provided YouTube links are working and are the latest.

    Context:\n {context}?\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    """
    The function `user_input` takes a user question, performs a similarity search on a vector store,
    runs an asynchronous function to generate a conversational response, and displays the response.

    Args:
      user_question: The `user_question` parameter in the `user_input` function is the question or input
    provided by the user that will be used for similarity search and conversational chain processing.
    This input will be used to find similar documents in the vector store and generate a response using
    a conversational chain model.
    """
    try:
        vector_store = load_vector_store()
        docs = vector_store.similarity_search(user_question)

        # Create an event loop and run the asynchronous function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        chain = loop.run_until_complete(get_conversational_chain())

        response = chain({"input_documents": docs}, return_only_outputs=True)

        st.session_state.output_text = response["output_text"]
        st.write("Reply: ", st.session_state.output_text)
    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
    """
    The `main` function in the provided Python code snippet loads an animation from a JSON file, allows
    users to upload PDF files for processing, and displays additional course videos if the "Process"
    button is clicked.
    """
    # Load animation from JSON

    st.write("<h1><center>Resume Analyser</center></h1>", unsafe_allow_html=True)
    st.write("")
    try:
        with open("src/Resume.json", encoding="utf-8") as anim_source:
            animation = json.load(anim_source)
        st_lottie(animation, 1, True, True, "high", 200, -200)
    except FileNotFoundError:
        st.warning("Animation file not found.")
    if "pdf_docs" not in st.session_state:
        st.session_state.pdf_docs = None

    if "output_text" not in st.session_state:
        st.session_state.output_text = ""

    pdf_docs = st.file_uploader(
        "Upload your PDF Files and Click on the Submit & Process Button",
        accept_multiple_files=True,
    )

    if st.button("Process"):
        if pdf_docs:
            with st.spinner("Analysing..."):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        user_input(raw_text)
                    else:
                        st.warning("No text found in the uploaded PDFs.")
                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")

            # Additional Courses
            st.divider()
            st.text("Additional Courses:")
            st.video("https://www.youtube.com/watch?v=JxgmHe2NyeY&t")
            st.divider()
            st.video("https://www.youtube.com/watch?v=5NQjLBuNL0I")
            st.divider()

    if pdf_docs:
        st.session_state.pdf_docs = pdf_docs


if __name__ == "__main__":
    main()
