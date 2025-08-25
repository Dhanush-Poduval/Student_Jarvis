from fastapi import FastAPI,UploadFile,File
import PyPDF2
import io

app =FastAPI()

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

