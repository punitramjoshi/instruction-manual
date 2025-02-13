# main.py

from flask import Flask, request, jsonify
from model import ImageProcessor

app = Flask(__name__)
processor = ImageProcessor()

@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    data = request.get_json()
    if not data or "file_path" not in data:
        return jsonify({"error": "No file path provided"}), 400
    
    if not isinstance(data.get("file_path"), str) or not data.get("file_path"):
        return jsonify({"error": "Invalid file path provided"}), 400

    file_path = data["file_path"]

    try:
        result_dict = processor.processing(file_path=file_path)
        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
