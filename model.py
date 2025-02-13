# model.py

import os
import tempfile
import json
import logging
import base64
from openai import OpenAI
from dotenv import load_dotenv
import fitz
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from docx2pdf import convert

load_dotenv(override=True)

class ImageProcessor:
    def __init__(self, model="gpt-4o", api_key=None):
        self.model = model
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.json_schema = """
{
    "components": {
        "parts": [
            {
                "[Number given in the drawing]": {
                    "name": "<part_name>",
                    "quantity": <quantity_number>,
                    "description": "<description_description>",
                    "type": "part"
                }
            },
            ...
        ],
        "hardware": [
            {
                "[Number given in the drawing]": {
                    "name": "<hardware_name>",
                    "specs": "<specifications>",
                    "quantity": <quantity_number>,
                    "description": "<description_description>",
                    "type": "hardware"
                }
            },
            ...
        ],
        "tools": [
            {
                "[Number given in the drawing]": {
                    "name": "<tool_name>",
                    "quantity": <quantity_number>,
                    "description": "<description_description>",
                    "type": "tool"
                }
            },
            ...
        ]
    },
    "assembly_instructions": [
        {
            "step": <step_number>,  // As given in the drawing.
            "instructions": "<detailed_instructions>"
        }
    ],
    "final_product": "<final_product_description>"
}
"""

    def pdf_to_base64_images(self, pdf_path):
        parsed_path = urlparse(pdf_path)
        if parsed_path.scheme in ("http", "https", "ftp", "ftps"):
            response = requests.get(pdf_path)
            pdf_document = fitz.open(stream=response.content, filetype="pdf")
        else:
            pdf_document = fitz.open(pdf_path)
        
        base64_images = []

        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document.load_page(page_num)
            # Convert the page to a Pixmap (image)
            pix = page.get_pixmap()
            
            # Convert the Pixmap to a PIL Image
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Save the image to a bytes buffer
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            
            # Encode the image to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Append to the list
            base64_images.append(img_str)
        
        return base64_images

    def process_images(self, base64_images: list[bytes]):
        images = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
            }
            for base64_image in base64_images
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are an assembly line expert having expertise in recognising the parts, hardwares and tools with their names and specifications and also with writing instructions for the assembly of the products. 
You are provided with an assembly part drawing for a product.
The part drawing will be consisting of three types of objects:-
1. Parts
2. Hardwares
3. Tools
Along with the above objects, it will also consist a step by step pictorial tutorial for assembly of the product.
You will be given a JSON schema that represents the structure of the expected output of the instruction manual for the given product. By analyzing the part drawing make an instruction manual for the product as per the given schema. 
Follow the given instructions:-
1. Give the number of the objects as per the drawing only.
2. The assembly instructions should also be in the sequence similar to that given in the image.
3. The product numbers given in the assembly instructions should also be same as in the drawing.
4. Give each and every assembly instruction in very detail.
The JSON schema is as follows:
{self.json_schema}
""",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "The image of the instruction manual.",
                        },
                        *images,
                    ],
                },
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content

    def processing(self, file_path) -> dict:
        file_path = os.path.abspath(file_path)  # Ensure a safe path
        # Use case-insensitive file extension checking
        if file_path.lower().endswith((".docx", ".doc")):
            # Create a temporary file for the PDF conversion
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
                pdf_path = tmp_pdf.name
            try:
                convert(input_path=file_path, output_path=pdf_path)
            except Exception as e:
                logging.error(f"Error converting DOCX to PDF: {e}")
                raise
        elif file_path.lower().endswith(".pdf"):
            pdf_path = file_path
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
        
        logging.info(f"Processing PDF: {pdf_path}")
        try:
            base64_images = self.pdf_to_base64_images(pdf_path=pdf_path)
            logging.info("Converted PDF pages to base64 images.")
            result = self.process_images(base64_images)
            try:
                result_dict = json.loads(result)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON response: {e}")
                raise ValueError("The model did not return valid JSON.")
        finally:
            # Clean up the temporary PDF if one was created
            if file_path.lower().endswith((".docx", ".doc")) and os.path.exists(pdf_path):
                os.remove(pdf_path)
                logging.info("Temporary PDF file removed.")
        
        logging.info(f"Result: {result_dict}")
        return result_dict
    
if __name__ == "__main__":
    processor = ImageProcessor()
    result_dict = processor.processing(file_path="./Instruction Manual.pdf")
    print(result_dict)