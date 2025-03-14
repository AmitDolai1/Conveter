from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from pdf2docx import Converter
from PIL import Image
import moviepy.editor as mp
import speech_recognition as sr
import os
import uuid
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

import atexit
import shutil

@atexit.register
def cleanup():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

@app.post("/convert")
async def convert_file(file: UploadFile = File(...), type: str = Form(...)):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file first
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # PDF to Word
    if type == "pdfToWord":
        docx_filename = file_path.replace(".pdf", ".docx")
        cv = Converter(file_path)
        cv.convert(docx_filename, start=0, end=None)
        cv.close()
        return FileResponse(docx_filename, filename="converted.docx")

    # Image Compression
    elif type == "compressImage":
        image = Image.open(file_path)
        compressed_path = file_path.replace(".jpg", "_compressed.jpg")
        image.save(compressed_path, quality=50, optimize=True)
        return FileResponse(compressed_path, filename="compressed.jpg")

    # Video to MP3
    elif type == "videoToMp3":
        video = mp.VideoFileClip(file_path)
        mp3_filename = file_path.replace(".mp4", ".mp3")
        video.audio.write_audiofile(mp3_filename)
        return FileResponse(mp3_filename, filename="audio.mp3")

    # Audio to Text
    elif type == "audioToText":
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        text_filename = file_path.replace(".wav", ".txt")
        with open(text_filename, "w") as f:
            f.write(text)
        return FileResponse(text_filename, filename="transcription.txt")

    # Image Resizing
    elif type == "resizeImage":
        image = Image.open(file_path)
        resized_path = file_path.replace(".jpg", "_resized.jpg")
        image = image.resize((300, 300))
        image.save(resized_path)
        return FileResponse(resized_path, filename="resized.jpg")

    return {"error": "Invalid conversion type"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
