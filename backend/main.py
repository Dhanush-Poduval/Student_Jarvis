from fastapi import FastAPI,UploadFile,File,Form
import PyPDF2
import io
from transformers import pipeline

app =FastAPI()

qa_pipeline=pipeline("question-answering",model="deepset/roberta-large-squad2")

text=""
def chunk_text(text,chunk_size=400,overlaps=50):
    words=text.split()
    chunks=[]
    start=0
    while start<len(words):
        end=min(start+chunk_size,len(words))
        chunk=" ".join(words[start:end])
        chunks.append(chunk)
        start+=chunk_size-overlaps
    return chunks
def ask_agent(question , context_text):
   chunks=chunk_text(context_text)
   best_score=0
   best_answer="No answer found"
   for chunk in chunks:
    result = qa_pipeline(question=question, context=chunk)
    if result['score']>best_score:
        best_score=result['score']
        best_answer=result['answer']
   print(f"the best score is :{best_score:.2f}")
   return best_answer

   
    
    

def extract_pdf(file:io.BytesIO):
    pdf_reader=PyPDF2.PdfReader(file)
    text=""
    for pages in pdf_reader.pages:
        text+=pages.extract_text()or"Empty file"
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


