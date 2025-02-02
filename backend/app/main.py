from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.youtube_downloader import download_youtube_audio
from app.audio_processor import convert_audio_to_notes
import os

app = FastAPI()

@app.post("/process-youtube")
async def process_youtube(
    url: str = Form(...),
):
    try:
        audio_path = download_youtube_audio(url)
        notes = convert_audio_to_notes(audio_path)
        os.remove(audio_path)
        return {"notes": notes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/process-file")
async def process_file(
    file: UploadFile = File(...),
):
    try:
        # Save uploaded file
        temp_dir = "app/temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = f"{temp_dir}/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        notes = convert_audio_to_notes(file_path)
        os.remove(file_path)
        return {"notes": notes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))