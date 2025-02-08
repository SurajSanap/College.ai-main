<img src="https://github.com/user-attachments/assets/93d7b577-f653-4507-9b9e-3dcb04114c44" alt="Logo College" width="150" height="150">


# College.ai

College.ai is an advanced AI-powered platform that leverages **OpenAI's ChatGPT** and **Google Gemini** to provide a comprehensive set of tools for students, job seekers, and professionals. This project offers a range of functionalities, including AI-driven resume analysis, applicant tracking, contest tracking, and AI-powered document search.

![College.ai Overview](https://github.com/SurajSanap/College.ai-main/assets/101057653/f5923134-c4c1-4586-975b-3247675bb475)

[Watch College.ai Demo](https://youtu.be/K2QHmboTf8o?si=42LbPMeTPQYCDgNX)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

### AI Interview (New in Version 2)

The **AI Interview** feature provides a real-time, voice-based assistant that helps users practice job interviews, learn languages, and refine communication skills. It integrates **OpenAI's ChatGPT** for conversational capabilities and supports **bilingual conversations (English & Japanese)**. The assistant can process spoken input, detect language, translate, and provide text-to-speech feedback, making it a valuable tool for interview preparation and language learning.

[Watch AI Interview Demo](https://youtu.be/K2QHmboTf8o?si=42LbPMeTPQYCDgNX)

### Ask To PDF

This feature allows users to **upload and train AI on PDFs**, enabling contextual search and Q&A on document content. It uses **Google Gemini embeddings** and **FAISS vector storage** for efficient search and retrieval.

### Resume Analyzer

The Resume Analyzer evaluates resumes against industry standards and job descriptions. It provides **skill recommendations, improvement suggestions, and career guidance** based on AI analysis.

### Applicant Tracking System (ATS)

This system helps job seekers **match their resumes with job descriptions**, highlighting missing keywords and scoring profile compatibility.

### Contest Calendar

A centralized dashboard that tracks **upcoming coding competitions** from platforms like **LeetCode, Codeforces, CodeChef, and GeeksforGeeks**.

### Job Tracker

Allows users to **track job applications**, update their statuses, and maintain an organized record of their job search progress.

### Project & Research Paper Ideas

Generates AI-suggested project ideas based on selected **domains** (Software Engineering, AI/ML, Electrical Engineering, etc.). Also fetches **relevant research papers** from sources like Google Scholar.

### Prompt Examples

Provides structured examples for **prompt engineering**, guiding users on how to frame AI queries effectively.

## Technology Stack

- **Natural Language Processing:** OpenAI ChatGPT-4, Google Gemini
- **Vector Search:** FAISS for embedding-based document retrieval
- **Web Application:** Streamlit for UI and backend integration
- **Databases:** SQLite for user and job tracking data
- **Text Processing:** LangChain, PyPDF2 for PDF parsing
- **Speech Processing:** gTTS for text-to-speech, SpeechRecognition for voice input

## Installation

Clone the repository:

```bash
git clone https://github.com/SurajSanap/College.ai.git
cd College.ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Contribution

If you'd like to contribute to College.ai, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and commit them.
4. Push your changes to your fork.
5. Create a pull request.

## License

This project is licensed under the **MIT License**.

### 📄 Documentation

Explore our comprehensive documentation in the [LEARN.md](https://github.com/SurajSanap/College.ai-main/blob/main/Learn.md) file, which serves as a detailed guide to understanding and contributing to College.ai.

### 🌟 Join Us 

<a href="https://github.com/SurajSanap/College.ai-main/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SurajSanap/College.ai-main" />
</a>

Ready to embark on a journey of collaborative learning? Join College.ai now and be a part of a community that believes in the power of collaboration!

Thank you for contributing to our open-source project! We appreciate your support.

Don't forget to leave a star ⭐

Happy Coding!

<p align="right"><a href="#top">Back to top</a></p>

