from fastapi import FastAPI,UploadFile,File,Form,HTTPException,status,APIRouter,Depends
from fastapi.responses import StreamingResponse
import PyPDF2
import io,os
import re
from typing import List
from transformers import pipeline
from docx import Document
from gtts import gTTS
from sqlalchemy.orm import Session
from .. import database,schemas,models,oauth2


app =FastAPI()

router=APIRouter(
    tags=['AI part']
)


qa_pipeline=pipeline("question-answering",model="deepset/roberta-large-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_user_document(db: Session, document_id: int, user_id: int):
    doc = db.query(models.Documents).filter(
        models.Documents.id == document_id,
        models.Documents.user_id == user_id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or access denied")
    return doc


def get_user_summary(db: Session, summary_id: int, user_id: int):
    summary = (
        db.query(models.Summary)
        .join(models.Documents, models.Summary.document_id == models.Documents.id)
        .filter(
            models.Summary.id == summary_id,
            models.Documents.user_id == user_id
        )
        .first()
    )
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found or access denied")
    return summary


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
async def upload_pdf(file:UploadFile=File(...),db:Session=Depends(database.get_db),current_user:schemas.Show_User=Depends(oauth2.get_current_user),chat_session:int=Form(...)):
    Upload_folder="../uploads/"
    os.makedirs(Upload_folder, exist_ok=True)
    file_location=f"{Upload_folder}{file.filename}"
    with open(file_location,"wb") as f:
        f.write(await file.read())
    
    user=db.query(models.User).filter(models.User.id==current_user.id).first()
    chat_session=db.query(models.ChatSessions).filter(models.ChatSessions.id==chat_session,models.ChatSessions.user_id==current_user.id).first()
    pdf_file=io.BytesIO(open(file_location,"rb").read())
    text=extract_pdf(pdf_file)
    full_text=" ".join([page["text"] for page in text])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not chat_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no chat session created")
    new_doc=models.Documents(user_id=current_user.id,filename=file.filename,session_id=chat_session.id, file_path=file_location,document_text=full_text)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    preview=new_doc.document_text[:500]
   
   
    
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
async def upload_docx(file: UploadFile = File(...),current_user:schemas.Show_User=Depends(oauth2.get_current_user),db:Session=Depends(database.get_db),session_id:int=Form(...)):
    Upload_folder="../uploads/"
    os.makedirs(Upload_folder, exist_ok=True)
    file_location=f"{Upload_folder}{file.filename}"
    with open(file_location,"wb") as f:
        f.write(await file.read())
    user=db.query(models.User).filter(models.User.id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    file_content=io.BytesIO(open(file_location,"rb").read())

    new_chat=db.query(models.ChatSessions).filter(models.ChatSessions.id==session_id).first()
    if not new_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No chat session created")
    
    global text
    text = extract_docx(file_content)
    full_text=" ".join(d["text"]for d in text)
    new_doc=models.Documents(user_id=current_user.id,filename=file.filename,session_id=new_chat.id ,file_path=file_location,document_text=full_text)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    preview=new_doc.document_text[:500]
   
    return {'document':{"id":new_doc.id,"filename":new_doc.filename , "usern name":user.name},"preview":preview}


@router.post('/ask')
async def ask_question(
    ask_question: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.Show_User = Depends(oauth2.get_current_user),
    document_id: int = Form(...)
):
    document = get_user_document(db, document_id, current_user.id)
    
    uploaded_text = document.document_text.split("\f")
    final_text = [{"text":page} for page in uploaded_text if page.strip()]
    
    model_answer = ask_agent(ask_question, final_text)
    
    new_question = models.ChatHistory(
        session_id=document.session_id,
        question=ask_question,
        answer=model_answer
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return {"answer": model_answer}



@router.post('/summarize_pdf')
async def summarize_pdf_endpoint(current_user:schemas.Show_User=Depends(oauth2.get_current_user),db:Session=Depends(database.get_db),document_id:int=Form(...)):
    users=db.query(models.User).filter(models.User.id==current_user.id).first()

    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")
    
    doc = db.query(models.Documents).filter(
    models.Documents.id == document_id,
    models.Documents.user_id == current_user.id   # <--- enforce ownership
    ).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No document uploaded yet")
    summary = summarize_pdf_chunks([{"text":doc.document_text}])
    full_summary=" ".join(summary)
    new_summary=models.Summary(document_id=doc.id , summary_text=full_summary,session_id=doc.session_id)
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    flashcards=[]
    for i ,flash in enumerate(summary):
        new_flash=models.Flashcards(summary_id=new_summary.id,point=f"Point{i+1}",answer=flash)
        db.add(new_flash)
        flashcards.append({"Point":new_flash.point,"Answer":new_flash.answer})
    db.commit()
    db.refresh(new_flash)
    return{
        "document_id":doc.id,
        "summary_id":new_summary.id,
        "flashcards":flashcards,
        "user name":users.name
    }

    
    

@router.post('/tts')
async def texttospeech(
    current_user: schemas.Show_User = Depends(oauth2.get_current_user),
    summary_id: int = Form(...),
    db: Session = Depends(database.get_db)
):
    summary = get_user_summary(db, summary_id, current_user.id)
    
    Upload_folder = "../audio/"
    os.makedirs(Upload_folder, exist_ok=True)
    filename = f"flashcard_{summary_id}.mp3"
    file_path = os.path.join(Upload_folder, filename)

    tts = gTTS(text=summary.summary_text, lang="en")
    tts.save(file_path)

    voice = models.Audio(flashcard_id=summary_id, audio_path=file_path, session_id=summary.session_id)
    db.add(voice)
    db.commit()
    db.refresh(voice)

    with open(file_path, "rb") as f:
        audio_bytes = io.BytesIO(f.read())
    audio_bytes.seek(0)

    return StreamingResponse(audio_bytes, media_type="audio/mpeg")


@router.get('/documents',response_model=List[schemas.Document])
def get_documents(db:Session=Depends(database.get_db),current_user:schemas.Show_User=Depends(oauth2.get_current_user)):
    all_docs = db.query(models.Documents).filter(models.Documents.user_id == current_user.id).all()

    return all_docs


@router.post('/chat_session')
def chat_session(chat_title:str=Form(...),db:Session=Depends(database.get_db),current_user:schemas.Show_User=Depends(oauth2.get_current_user)):
    new_chat_session=models.ChatSessions(user_id=current_user.id,title=chat_title)
    db.add(new_chat_session)
    db.commit()
    db.refresh(new_chat_session)

    return {"title":new_chat_session.title,"user":current_user.name,"id":new_chat_session.id}


@router.get('/chat_session',response_model=List[schemas.ChatSessionBase])
def get_all_chats(db:Session=Depends(database.get_db),current_user:schemas.Show_User=Depends(oauth2.get_current_user)):
    print(current_user.id)
    all_chats=db.query(models.ChatSessions).filter(models.ChatSessions.user_id==current_user.id).all()
    if not all_chats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Chats been made")
    return all_chats

@router.get('/session_data/{session_id}')
def get_full_session(
    session_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.Show_User = Depends(oauth2.get_current_user)
):
    # Ensure the session belongs to the current user
    session = db.query(models.ChatSessions).filter(
        models.ChatSessions.id == session_id,
        models.ChatSessions.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    document=db.query(models.Documents).filter(models.Documents.session_id==session_id).all()

    summary=db.query(models.Summary).filter(models.Summary.session_id==session_id).all()

    audio=db.query(models.Audio).filter(models.Audio.session_id==session_id).all()

    question=db.query(models.ChatHistory).filter(models.ChatHistory.session_id==session_id).all()

    return {
        "session": session,
        "documents": document,
        "chats": question,
        "summaries": summary,
        "audio_files": audio
    }




