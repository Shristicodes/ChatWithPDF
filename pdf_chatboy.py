import streamlit as st
import PyPDF2
import google.generativeai as genai

genai.configure(api_key="ENTER_SECRET_KEY_FROM_GEMINI_API")

st.set_page_config(page_title="PDF Chatbot with Gemini", layout="wide")
st.title("🤖 Chat with your PDF (Gemini)")

pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])

def extract_pdf_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

def ask_question_to_pdf(text, question):
    prompt = f"""
You are a helpful assistant. Use the following PDF content to answer the user's question.

PDF Content:
{text[:20000]}

Question: {question}
Answer:
"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if pdf_file:
    pdf_text = extract_pdf_text(pdf_file)
    question = st.text_input("Ask a question about the PDF:")
    
    if question:
        with st.spinner("Thinking..."):
            answer = ask_question_to_pdf(pdf_text, question)
        st.success("Answer:")
        st.write(answer)
        
    if st.button("Summarize PDF"):
        with st.spinner("Generating summary..."):
            summary_prompt = "Summarize this PDF in 3 concise bullet points:\n" + pdf_text[:20000]
            summary = ask_question_to_pdf(pdf_text, summary_prompt)
        st.success("Summary:")
        st.write(summary)
