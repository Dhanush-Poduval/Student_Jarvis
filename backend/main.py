from fastapi import FastAPI,UploadFile,File,Form
import PyPDF2
import io
import torch
from transformers import pipeline

app =FastAPI()

qa_pipeline=pipeline("question-answering",model="distilbert-base-cased-distilled-squad")

text=""
def ask_agent(question , context_text):
    result=qa_pipeline(question=question,context=context_text)
   
    
    return result['answer']

def extract_pdf(file:io.BytesIO):
    pdf_reader=PyPDF2.PdfReader(file)
    text=""
    for pages in pdf_reader.pages:
        text+=pages.extract_text()or""
    return text


@app.post('/student_pdf')
async def upload_pdf(file:UploadFile=File(...)):
    file_content=await file.read()
    pdf_file=io.BytesIO(file_content)
    global text
    text=extract_pdf(pdf_file)
    return {'The text is ':text[:500]}

@app.post('/ask')
async def ask_question(question:str=Form(...)):
    
    if not text:
        return{"error":"No PDF uploaded yet"}
    
    answer =ask_agent(question,text)
    return{"answer":answer}


