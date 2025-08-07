import io
import os
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware

from office_media_utils import office_media_to_zip_stream

load_dotenv()
origins = os.getenv("CORS_ORIGINS", "").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, hello, hello, how low?"}


@app.post("/extract-office-media")
async def extract_media_zip(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        zip_bytes = office_media_to_zip_stream(io.BytesIO(file_bytes))
        return Response(
            zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=mediafiles.zip"},
        )
    except Exception as e:
        return {"error": str(e)}
