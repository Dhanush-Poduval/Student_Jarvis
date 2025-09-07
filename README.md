# Student Jarvis
Student Jarvis is a smart study assistant that helps students read, understand, and retain information from PDFs or Word documents. Upload your study material, and it automatically generates **summaries**, **flashcards**, and even **TTS audio files** for on-the-go learning.

---

## Features

- Upload PDFs or DOCX files
- Generate concise, easy-to-read **summaries**
- Create **flashcards** for quick revision
- Convert summaries to **MP4 voice/audio files**
- Built for efficiency and convenience: all-in-one study tool

---

## Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Next.js + ShadCN  
- **Python Libraries:** PyPDF2 / pdfplumber (for PDF parsing), TTS libraries  
- **Other Tools:** [Add if any other AI or libraries used]

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/student-jarvis.git
cd student-jarvis

Setup Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Setup Frontend
cd frontend
npm install
npm run dev
