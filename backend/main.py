from fastapi import FastAPI,UploadFile,File,Form
import PyPDF2
import io
from transformers import pipeline
from docx import Document

app =FastAPI()

qa_pipeline=pipeline("question-answering",model="deepset/roberta-large-squad2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text=""
def chunk_text(pages,chunk_size=400,overlaps=50):
    chunks=[]
    for page in pages:
        words=page["text"].split()
        start=0
        while start<len(words):
            end=min(start+chunk_size,len(words))
            chunk=" ".join(words[start:end])
            chunks.append({"page":page["page"],"text":chunk})
            start+=chunk_size-overlaps
    return chunks

def summarize_pdf_chunks(pages, chunk_size=400, overlap=50):
    chunks = chunk_text(pages, chunk_size=chunk_size, overlaps=overlap)
    summaries = []
    for chunk in chunks:
        if len(chunk["text"].strip()) < 20:
            continue
        summary = summarizer(chunk["text"], max_length=60, min_length=20, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return summaries

def ask_agent(question , pages):
   chunks=chunk_text(pages)
   best_score=0
   best_answer="No answer found"
   for chunk in chunks:
    if len(chunk["text"].strip())<20:
        continue
    print(f"[DEBUG] Page {chunk['page']} chunk preview: {chunk['text'][:100]}")
    result = qa_pipeline(question=question, context=chunk["text"])
    print(f"[DEBUG] Score: {result['score']}, Answer: {result['answer']}")

    if result['score']>best_score:
        best_score=result['score']
        best_answer=result['answer']
        best_page=chunk["page"]
   print(f"the best score is :{best_score:.2f}")
   return best_answer , best_page

def clean_page_text(page_text: str):
    # remove author/title metadata
    page_text = page_text.split("Submitted By:")[0]
    # fix hyphenation and line breaks
    page_text = page_text.replace("-\n", "")
    page_text = page_text.replace("\n", " ").strip()
    return page_text
    


def extract_docx(file: io.BytesIO):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            clean_para = clean_page_text(para.text)
            full_text.append(clean_para)
    pages_text = [{"page": i+1, "text": para} for i, para in enumerate(full_text)]
    return pages_text



def extract_pdf(file:io.BytesIO):
    pdf_reader=PyPDF2.PdfReader(file)
    pages_text=[]
    for i,page in enumerate(pdf_reader.pages):
        raw_page_text=page.extract_text()or" "
        clean_page=clean_page_text(raw_page_text)
        pages_text.append({"page":i+1,"text":clean_page})

    return pages_text


@app.post('/student_pdf')
async def upload_pdf(file:UploadFile=File(...)):
    file_content=await file.read()
    pdf_file=io.BytesIO(file_content)
    global text
    text=extract_pdf(pdf_file)
    preview=text[0]["text"][:500]
    preview_page=text[0]["page"]
    return {'The text is ':preview,"The page is ":preview_page}
@app.post('/student_docx')
async def upload_docx(file: UploadFile = File(...)):
    file_content = await file.read()
    docx_file = io.BytesIO(file_content)
    global text
    text = extract_docx(docx_file)
    preview = text[0]["text"][:500]
    preview_page = text[0]["page"]
    return {"The text is": preview, "The page is": preview_page}


@app.post('/ask')
async def ask_question(question:str=Form(...)):
    
    if not text:
        return{"error":"No PDF uploaded yet"}
    
    answer ,page =ask_agent(question,text)
    return{"answer":answer , "page":page}


@app.post('/summarize_pdf')
async def summarize_pdf_endpoint():
    if not text:
        return {"error": "No document uploaded yet"}
    flashcards=[]
    summary = summarize_pdf_chunks(text)
    for i, page in enumerate(summary):
        
        page_number = text[i]["page"] if i < len(text) else None
        flashcards.append({
            "Point": f"Key point {i+1}",
            "answer": page,
            "page": page_number
        })

    return {"flashcard":flashcards}



