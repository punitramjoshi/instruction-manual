import streamlit as st
import os
import json
import ast
from model import ImageProcessor

st.title("Instruction Manual Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "docx"])

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    processor = ImageProcessor()
    try:
        result_dict = processor.processing(file_path=file_path)
        st.json(result_dict)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        os.remove(file_path)