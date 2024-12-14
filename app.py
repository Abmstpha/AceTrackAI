from flask import Flask, request, jsonify
import os
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import PyPDF2

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the model and tokenizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
weights_path = "AceTrack_T5_weights.pt"
tokenizer_path = "AceTrack_T5_tokenizer"

try:
    tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    raise

# Function to parse the PDF
def parse_pdf(file_path):
    """
    Parses the PDF file and extracts questions, student answers, and correct answers.
    Returns a DataFrame with the parsed data.
    """
    data = {"Question": [], "Student Answer": [], "Correct Answer": []}

    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                lines = text.split("\n")
                
                # Parse lines for questions and answers
                for line in lines:
                    if line.startswith("Question"):
                        data["Question"].append(line.split(":", 1)[1].strip())
                    elif line.startswith("Student Answer"):
                        data["Student Answer"].append(line.split(":", 1)[1].strip())
                    elif line.startswith("Correct Answer"):
                        data["Correct Answer"].append(line.split(":", 1)[1].strip())

        # Check for consistent lengths
        if not (len(data["Question"]) == len(data["Student Answer"]) == len(data["Correct Answer"])):
            raise ValueError("Parsed data has inconsistent lengths.")
        
        return pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {e}")

# Function to generate feedback for all questions
def generate_feedback_for_all(dataframe, model, tokenizer, device):
    """
    Loops through each row in the DataFrame and generates feedback using the model.
    Returns a list of feedback.
    """
    feedback_list = []

    for _, row in dataframe.iterrows():
        question = row['Question']
        student_answer = row['Student Answer']
        correct_answer = row['Correct Answer']

        # Create the input text for the model
        input_text = (
            f"Question: '{question}' Correct Answer: '{correct_answer}' "
            f"Student Answer: '{student_answer}'"
        )

        # Tokenize and generate feedback
        inputs = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True).to(device)
        with torch.no_grad():
            outputs = model.generate(inputs['input_ids'], max_length=100, num_beams=3, early_stopping=True)
        feedback = tokenizer.decode(outputs[0], skip_special_tokens=True)
        feedback_list.append(feedback)

    return feedback_list

# Endpoint to upload a PDF file and generate feedback
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to upload a PDF file and process it to generate feedback.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Parse the PDF
        parsed_data = parse_pdf(file_path)

        # Generate feedback
        feedback_list = generate_feedback_for_all(parsed_data, model, tokenizer, device)

        # Combine results with the original questions and answers
        parsed_data['Feedback'] = feedback_list

        # Return the feedback as JSON
        return jsonify(parsed_data.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

