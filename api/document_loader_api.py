from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scripts.load_ba_document import BADocumentLoader
from scripts.load_sa_document import SADocumentLoader
import tempfile
import os

# uvicorn api.document_loader_api:app --reload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/ba-document")
async def upload_ba_document(
    file: UploadFile,
    confluence_link: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            loader = BADocumentLoader()
            loader.load_document(temp_file_path, confluence_link)
            
            return {"status": "success", "message": "BA document uploaded and processed successfully"}
        finally:
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/sa-document")
async def upload_sa_document(
    file: UploadFile,
    confluence_link: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            loader = SADocumentLoader()
            loader.load_document(temp_file_path, confluence_link)
            
            return {"status": "success", "message": "SA document uploaded and processed successfully"}
        finally:
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))