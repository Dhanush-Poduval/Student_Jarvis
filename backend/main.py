from fastapi import FastAPI,UploadFile,File,Form,HTTPException,status
from fastapi.responses import StreamingResponse
import PyPDF2
import io
import re
from transformers import pipeline
from docx import Document
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
app =FastAPI()




qa_pipeline=pipeline("question-answering",model="deepset/roberta-large-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text=""
textbar=""
flashcards=[]
def chunk_text(pages,chunk_size=100,overlaps=50):
    chunks=[]
   
    for page in pages:
        words=page["text"].split() 
        start=0
        while start<len(words):
            end=min(start+chunk_size,len(words))
            chunk=" ".join(words[start:end])
            chunks.append({"text":chunk})
            start+=chunk_size-overlaps
    return chunks

def summarize_pdf_chunks(pages):
    
    chunks = chunk_text(pages, chunk_size=100, overlaps=50)
    
    
    summaries = []
    for chunk in chunks:
        if len(chunk["text"].strip()) < 20:
            continue
        summary = summarizer(chunk["text"], max_length=80, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return summaries

def ask_agent(question ,pages):
   
   total_words=sum(len(p["text"].split())for p in pages)
   if len(pages)==1 or total_words<400:
       chunks=pages
   else:
       chunks=chunk_text(pages)
       
   best_score=0
   best_answer="No answer found"
   for chunk in chunks:
    if len(chunk["text"].strip())<20:
        continue
    print(f"[DEBUG] chunk preview: {chunk['text'][:100]}")
    result = qa_pipeline(question=question, context=chunk["text"])
    print(f"[DEBUG] Score: {result['score']}, Answer: {result['answer']}")

    if result['score']>best_score:
        best_score=result['score']
        best_answer=result['answer']
        
   print(f"the best score is :{best_score:.2f}")
   return best_answer 

def clean_page_text(page_text: str):
    page_text = re.sub(r"Submitted By:.*", "", page_text)
    page_text = re.sub(r"Author[s]*:.*", "", page_text)
    page_text = re.sub(r"Name[s]*:.*", "", page_text)
    page_text = re.sub(r"Affiliation[s]*:.*", "", page_text)
    
    # Remove headers like 'Introduction' if you want
    page_text = re.sub(r"^Introduction\s*", "", page_text, flags=re.IGNORECASE)
    
    # Fix hyphenation and line breaks
    page_text = page_text.replace("-\n", "")
    page_text = page_text.replace("\n", " ").strip()
    return page_text
    


def extract_docx(file: io.BytesIO , min_words=7, chunk_size=300, overlap=50):
    doc = Document(file)
    meaningful_paras = []
    for para in doc.paragraphs:
        if para.text.strip():
            clean_para = clean_page_text(para.text)
            if len(clean_para.split()) < min_words:
                continue
            if re.fullmatch(r"[0-9\s\-]+", clean_para):
                continue
            meaningful_paras.append(clean_para)
    
    # Split into chunks like PDF
    full_text = " ".join(meaningful_paras)
    words = full_text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])
        chunks.append({"text": chunk_text})
        start += chunk_size - overlap

    return chunks




def extract_pdf(file:io.BytesIO):
    pdf_reader=PyPDF2.PdfReader(file)
    pages_text=[]
    for i,page in enumerate(pdf_reader.pages):
        raw_page_text=page.extract_text()or" "
        clean_page=clean_page_text(raw_page_text)
        if len(clean_page.split()) < 10:
            continue
        pages_text.append({"text":clean_page})


    return pages_text


@app.post('/student_pdf')
async def upload_pdf(file:UploadFile=File(...)):
    file_content=await file.read()
    pdf_file=io.BytesIO(file_content)
    global text
    text=extract_pdf(pdf_file)
    preview=text[:500]
    return {'The text is ':preview}

@app.post('/text')
async def text_type(type_text:str):
    global textbar
    textbar=type_text
    if len(textbar.split())>500:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The amount of words crossed the word limit")
    return{"text":textbar}


@app.post('/student_docx')
async def upload_docx(file: UploadFile = File(...)):
    file_content = await file.read()
    docx_file = io.BytesIO(file_content)
    global text
    text = extract_docx(docx_file)
    preview = text[:500]
   
    return {"The text is": preview}


@app.post('/ask')
async def ask_question(question:str=Form(...)):
    
    if not text and not textbar:
        return{"error":"No text input or document given"}
    if textbar:
        result=qa_pipeline(question=question, context=textbar)
        answer=result['answer']
    else:
      answer=ask_agent(question,text)
    return{"answer":answer}


@app.post('/summarize_pdf')
async def summarize_pdf_endpoint():

    if not text:
        return {"error": "No document uploaded yet"}
    global flashcards
    summary = summarize_pdf_chunks(text)
    for i, page in enumerate(summary):
        
        
        flashcards.append({
            "Point": f"Key point {i+1}",
            "answer": page,
            
        })

    return {"flashcard":flashcards}

@app.post('/tts')
async def texttospeech():
  if not flashcards:
      return{"error":"No file uploaded yet"}
  text=" ".join([f["answer"]for f in flashcards])

  tts=gTTS(text=text,lang="en")
  audio_bytes=io.BytesIO()
  tts.write_to_fp(audio_bytes)
  audio_bytes.seek(0)

  return StreamingResponse(audio_bytes,media_type="audio/mpeg")




