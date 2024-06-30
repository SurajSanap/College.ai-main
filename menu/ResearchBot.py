import os

google_api_key = os.environ["GOOGLE_API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import streamlit as st
import json
from streamlit_lottie import st_lottie

def chatfunction(research_topic, research_area, number):
    llm = ChatGoogleGenerativeAI(temperature=0.7, top_p = 0.5, model="gemini-1.5-pro", google_api_key=google_api_key)

    template = """
    You are a research assistant bot for a college student.

    User is researching {research_topic} in the field of {research_area}. Please provide latest and 5 most influential research papers on this topic. User is interested in papers published within the last {number} years.

    Instructions:
    1. Use original titles same as research papers' along with year.
    2. Provide a short summary and key highlights for each research paper.
    3. Ensure all information is accurate and sourced from reputable journals and databases.
    4. Provide accurate links to the research papers beside the title.
    5. Use Google Scholar and research databases (e.g., ACM Digital Library, IEEE Xplore) to find relevant papers.
    
    Please output in the following format only
    
    ---
    1. [Title of research paper](hyper-link to the research paper) (year) \n
    Summary:\n
        Summary of the research paper\n
    Key Highlights:\n
        * First Key highlight of the paper\n
        * Second Key highlight of the paper\n
        * Third Key highlight of the paper\n
    ---
    2. [Title of research paper](hyper-link to the research paper) (year) \n
    SSummary:\n
        Summary of the research paper\n
    Key Highlights:\n
        * First Key highlight of the paper\n
        * Second Key highlight of the paper\n
        * Third Key highlight of the paper\n
    ---
    3. [Title of research paper](hyper-link to the research paper) (year) \n
    SSummary:\n
        Summary of the research paper\n
    Key Highlights:\n
        * First Key highlight of the paper\n
        * Second Key highlight of the paper\n
        * Third Key highlight of the paper\n
    ---
    4. [Title of research paper](hyper-link to the research paper) (year) \n
    SSummary:\n
        Summary of the research paper\n
    Key Highlights:\n
        * First Key highlight of the paper\n
        * Second Key highlight of the paper\n
        * Third Key highlight of the paper\n
    ---
    5. [Title of research paper](hyper-link to the research paper) (year) \n
    SSummary:\n
        Summary of the research paper\n
    Key Highlights:\n
        * First Key highlight of the paper\n
        * Second Key highlight of the paper\n
        * Third Key highlight of the paper\n
    ---
    Ensure that the titles are hyperlinked to their corresponding research paper.

    """

    prompt = PromptTemplate(
        input_variables=["research_topic", "research_area", "number"],
        template=template,
    )
    
    result = llm.invoke(prompt.format(research_topic=research_topic, research_area=research_area, number=number))
    return result.content
    

def main():

    with open('../src/lens.json', 'r', encoding='utf-8') as f:
        animation_data = json.load(f)
    col1, col2 = st.columns([1, 3])
    with col1:
        st_lottie(animation_data, speed=1, reverse=False, loop=True, quality="high", height=100, width=-50)
    with col2:
        st.write("<h1>Research Assistant</h1>", unsafe_allow_html=True)
    st.write("<h4>I need few inputs to help you in your research 🤖</h4>", unsafe_allow_html=True)

    # Input fields for research topic, area, and number of years
    research_topic = st.text_input("Enter the 'Research Topic' (Eg: Diffusion Models)")
    research_area = st.text_input("Enter the 'Research Area' (Eg: Deep Learning)")
    number_of_years = st.number_input("Number of Previous Years of papers required", min_value=1, step=1)
    
    if st.button("Submit"):
        if research_topic and research_area and number_of_years:
            st.success("Inputs received successfully!")
            st.session_state['research_topic'] = research_topic
            st.session_state['research_area'] = research_area
            st.session_state['number_of_years'] = number_of_years
        else:
            st.error("Please fill in all fields.")
    
        if 'research_topic' in st.session_state and 'research_area' in st.session_state and 'number_of_years' in st.session_state:
            # st.write("Research Topic : ", st.session_state['research_topic'])
            # st.write("Research Area : ", st.session_state['research_area'])
            # st.write("Number of Years : ", st.session_state['number_of_years'])
            with st.spinner("🔍Getting Papers..."):
                result = chatfunction(research_topic, research_area, number_of_years)
                result = result.split("---")
                for i in range(len(result)):
                    container = st.container(border=True)
                    container.write(result[i])

        else:
            st.warning("Please fill in the research inputs first before starting the chat.")        

if __name__ == "__main__":
    main()
