import base64
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import ast
import fitz
import requests
from urllib.parse import urlparse

load_dotenv()


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


    def pdf_to_png(self, pdf_path, output_path):
        """
        Convert a single-paged PDF to a PNG image.
        
        :param pdf_path: Path to the PDF file.
        :param output_path: Path to save the PNG image.
        """
        response = requests.get(pdf_path)
        print(response.content)
        # Open the PDF file
        pdf_document = fitz.open(stream=response.content, filetype="pdf")
        
        # Check if the PDF is empty
        if pdf_document.page_count < 1:
            raise ValueError("The PDF file is empty.")
        
        # Get the first page
        page = pdf_document.load_page(0)
        
        # Define the zoom matrix
        matrix = fitz.Matrix(2, 2)
        
        # Render the page to an image
        pix = page.get_pixmap(matrix=matrix)
        
        # Save the image as a PNG file
        pix.save(output_path)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process_image(self, image_path:str):
        base64_image = self.encode_image(image_path)
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
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content

    def processing(self, file_path) -> dict:
        self.pdf_to_png(pdf_path=file_path, output_path=image_path)
        print(f"Processing {image_path}")
        result = self.process_image(image_path)
        result_dict:dict = ast.literal_eval(result)
        print(result_dict)
        # os.remove(image_path)
        return result_dict
