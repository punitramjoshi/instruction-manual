# Image Processor Project

## Overview

This project consists of two primary files: `model.py` and `main.py`. The goal of the project is to process images of assembly instruction manuals and convert them into a structured JSON format using the OpenAI API. The project includes a Flask web application that provides an API endpoint to process these images.

## Project Structure

- `model.py`: This file contains the main logic for processing images using the OpenAI API.
- `main.py`: This file sets up a Flask web application that exposes an API endpoint for processing images.
- `.env`: This file stores environment variables such as the OpenAI API key.

## Installation

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/yourusername/image-processor-project.git
cd image-processor-project
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the project root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Running the Model Script

To run the model script directly and process an image:

1. Update the `image_path` variable in `model.py` with the path to your image.
2. Run the script:

```bash
python model.py
```

This will generate a JSON file `main_image.json` containing the structured output.

### Running the Flask App

To run the Flask web application:

```bash
python main.py
```

This will start the Flask server, which will be accessible at `http://127.0.0.1:5000`.

## API Endpoint

### Endpoint: `/process_image`

- **Method**: POST
- **Description**: Processes an image of an instruction manual and returns the structured JSON output.
- **Content-Type**: application/json

#### Request Body

```json
{
    "file_path": "path_to_your_image"
}
```

#### Response

- **Success (200)**

```json
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
            }
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
            }
        ],
        "tools": [
            {
                "[Number given in the drawing]": {
                    "name": "<tool_name>",
                    "quantity": <quantity_number>,
                    "description": "<description_description>",
                    "type": "tool"
                }
            }
        ]
    },
    "assembly_instructions": [
        {
            "step": <step_number>,
            "instructions": "<detailed_instructions>"
        }
    ],
    "final_product": "<final_product_description>"
}
```

- **Error (400)**

```json
{
    "error": "No file path provided"
}
```

- **Error (500)**

```json
{
    "error": "Detailed error message"
}
```

## Example Usage with Curl

```bash
curl -X POST http://127.0.0.1:5000/process_image \
    -H "Content-Type: application/json" \
    -d '{"file_path": "path_to_your_image"}'
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Acknowledgements

- OpenAI for providing the API used in this project.
- Flask for the web framework.