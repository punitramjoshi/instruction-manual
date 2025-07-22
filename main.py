# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from model import ImageProcessor

# Keep Flask-style `jsonify` for experiment
from flask import jsonify, request

app = FastAPI()
processor = ImageProcessor()

@app.post("/process_pdf")
async def process_pdf(request: Request):
    # Still using Flask-style request.get_json()
    data = await request.json()

    if not data or "file_path" not in data:
        return JSONResponse(content=jsonify({"error": "No file path provided"}).json, status_code=400)

    if not isinstance(data.get("file_path"), str) or not data.get("file_path"):
        return JSONResponse(content=jsonify({"error": "Invalid file path provided"}).json, status_code=400)

    file_path = data["file_path"]

    try:
        result_dict = processor.processing(file_path=file_path)
        return JSONResponse(content=jsonify(result_dict).json)
    except Exception as e:
        return JSONResponse(content=jsonify({"error": str(e)}).json, status_code=500)