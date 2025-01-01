# AceTrackAI - A Student Feedback Generator

AceTrackAI is an AI-powered tool designed to evaluate student responses to historical questions and provide constructive, context-aware feedback. Developed using T5 transformers, the project automates the assessment process, offering actionable insights to students and instructors.

---

## Features

- **Upload PDF Exams**: Upload scanned exam papers directly for evaluation.  
- **Automated Parsing**: Extracts questions, responses, and reference answers from the uploaded documents.  
- **AI-Powered Feedback**: Generates accurate feedback based on predefined correct answers using a fine-tuned T5 model.  
- **User-Friendly Interface**: Built with Streamlit, ensuring simplicity and accessibility.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abmstpha/AceTrackAI.git
   cd AceTrackAI
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure the `sentencepiece` library is installed for T5 tokenizer compatibility:
   ```bash
   pip install sentencepiece
   ```

## Usage

1. **Prepare the Model Weights**: The repository does not include `.pt` files due to size constraints. Please download the model weights separately and place them in the appropriate directory.

2. Start the backend:
   ```bash
   python app.py
   ```

3. Start the frontend:
   ```bash
   streamlit run frontend.py
   ```

4. Access the application: Open your browser and navigate to `http://localhost:8501`.

5. Upload a PDF of the exam and view the AI-generated feedback.

## Project Structure

```plaintext
AceTrack/
├── app.py                 # Backend script
├── frontend.py           # Frontend script
├── requirements.txt      # List of dependencies 
├── model weights (PT file not included due to size) 
├── AceTrack_T5_weights/  # Directory for 
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── spiece.model
│   └── added_tokens.json
└── README.md             # This README file
```