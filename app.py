import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
hey act like a skilled or very experinece ATS with a deep understanding of 
tech field,software engineering ,data science,data analytics,full stack,data engineer.Your task is to evalauate the resume based on teh given job description
you must conisder the job market is very competative and oyu should provide best assistanve for imporving teh resumes.Assign the percentage matching based
on teh Jd and teh missing key words with high accuracy  
resume:{text}
description:{jd}
i want teh response in one single string having teh structure
{{"JD Match":"%","MissingKeywords:[]","Profile summary":""}}
"""

st.title("Smart ATS")
st.text("Improve your resume ATS")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf")
submit = st.button("Check the response")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader(response)
