# Instruction Manual Generator

## Overview
This project is an **AI-powered Instruction Manual Generator** that extracts assembly instructions from **PDF** or **DOCX** files containing part drawings and step-by-step guides. It leverages **OpenAI's GPT-4o model** to analyze images of these drawings and generate a structured instruction manual in JSON format.

## Tech Stack
- **Python** (Backend)
- **Flask** (API Endpoint)
- **Streamlit** (User Interface)
- **OpenAI API** (GPT-4o for image processing & text generation)
- **PyMuPDF (fitz)** (PDF handling)
- **Pillow (PIL)** (Image processing)
- **Docx2pdf** (DOCX to PDF conversion)

---

## Architecture

### Components:
1. **Model (`model.py`)**  
   - Converts **PDF pages** into **Base64 images**
   - Sends images to **OpenAI API** for processing
   - Generates structured **JSON output** for the instruction manual

2. **Backend (`main.py`)**  
   - **Flask API** endpoint (`/process_pdf`) to accept file paths
   - Calls the **model processor** and returns JSON response

3. **Frontend (`app.py`)**  
   - **Streamlit UI** for file uploads
   - Displays the generated instruction manual in a readable format

---

## Workflow

1. **File Upload & Preprocessing:**
   - User uploads a **PDF** or **DOCX** file.
   - If DOCX, it is converted to **PDF**.

2. **Image Extraction & Processing:**
   - PDF pages are converted into **Base64 images**.
   - Images are sent to **OpenAI's GPT-4o**.

3. **AI Analysis & JSON Generation:**
   - The model extracts **Parts, Hardware, and Tools** with their numbers and descriptions.
   - Step-by-step **Assembly Instructions** are extracted.
   - A **Final Product Description** is generated.

4. **Results Display & API Response:**
   - The Streamlit UI displays **formatted JSON output**.
   - The Flask API returns the result as a **JSON response**.

---

## Execution Guide

### 1. Install Dependencies
Ensure you have Python **3.8+** installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key
Create a **.env** file in the project root and add:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Flask API
Start the backend server:
```bash
python main.py
```

### 4. Run the Streamlit App
Launch the UI:
```bash
streamlit run app.py
```

---

## API Usage
### Endpoint: `/process_pdf`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "file_path": "path_to_your_pdf_or_docx"
  }
  ```
- **Response:**
  ```json
  {
      "components": { ... },
      "assembly_instructions": [ ... ],
      "final_product": "..."
  }
  ```

---

## Future Improvements
- **Optimize OpenAI API Calls** to reduce latency.
- **Improve UI** with better visualization of generated instructions.
- **Allow direct file uploads via Flask API** instead of passing file paths.
- **Add multi-language support** for instruction generation.

---

## Author & License
- **Author:** Punitram Joshi
- **License:** MIT License