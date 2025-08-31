from fastapi import FastAPI,UploadFile,File,Form,HTTPException,status,APIRouter,Depends
from fastapi.responses import StreamingResponse
import PyPDF2
import io,os
import re
from transformers import pipeline
from docx import Document
from gtts import gTTS
from sqlalchemy.orm import Session
from .. import database,schemas,models


app =FastAPI()

router=APIRouter(
    tags=['AI part']
)


qa_pipeline=pipeline("question-answering",model="deepset/roberta-large-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text=""
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


@router.post('/student_pdf')
async def upload_pdf(file:UploadFile=File(...),db:Session=Depends(database.get_db),user_id:int=Form(...)):
    Upload_folder="../uploads/"
    os.makedirs(Upload_folder, exist_ok=True)
    file_location=f"{Upload_folder}{file.filename}"
    with open(file_location,"wb") as f:
        f.write(await file.read())
    new_doc=models.Documents(user_id=user_id,filename=file.filename,file_path=file_location)
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    pdf_file=io.BytesIO(open(file_location,"rb").read())
    global text
    text=extract_pdf(pdf_file)
    preview=text[:500]
   
   
    
    return {'document':{"id":new_doc.id,"filename":new_doc.filename , "usern name":user.name},"preview":preview}

@router.post('/text')
async def text_type(type_text:str):
    textbar=type_text
    if len(textbar.split())>500:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The amount of words crossed the word limit")
    global text
    text=[{"text":textbar}]
    return{"text":text[0]['text'][:500]}


@router.post('/student_docx')
async def upload_docx(file: UploadFile = File(...)):
    file_content = await file.read()
    docx_file = io.BytesIO(file_content)
    global text
    text = extract_docx(docx_file)
    preview = text[:500]
   
    return {"The text is": preview}


@router.post('/ask')
async def ask_question(question:str=Form(...)):
    
    if not text :
        return{"error":"No text input or document given"}
   
    else:
      answer=ask_agent(question,text)
    return{"answer":answer}


@router.post('/summarize_pdf')
async def summarize_pdf_endpoint(user_id:int=Form(...),db:Session=Depends(database.get_db),document_id:int=Form(...)):
    users=db.query(models.User).filter(models.User.id==user_id).first()

    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")
    
    doc_id=db.query(models.Documents).filter(models.Documents.id==document_id).first()
    if not doc_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No document uploaded yet")
    summary = summarize_pdf_chunks(text)
    full_summary=" ".join(summary)
    new_summary=models.Summary(document_id=doc_id.id , summary_text=full_summary)
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    global flashcards
    flashcards=[{"Point":f"Key Point{i+1}","answer":flash} for i , flash in enumerate(summary)]
    return{
        "document_id":doc_id.id,
        "summary_id":new_summary.id,
        "flashcards":flashcards,
        "user name":users.name
    }
    

@router.post('/tts')
async def texttospeech():
  if not flashcards:
      return{"error":"No file uploaded yet"}
  text=" ".join([f["answer"]for f in flashcards])

  tts=gTTS(text=text,lang="en")
  audio_bytes=io.BytesIO()
  tts.write_to_fp(audio_bytes)
  audio_bytes.seek(0)

  return StreamingResponse(audio_bytes,media_type="audio/mpeg")




