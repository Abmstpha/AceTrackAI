# AceTrackAI - A Student Feedback Generator

AceTrack is an AI-powered tool designed to evaluate student responses to historical questions and provide detailed, constructive feedback. It leverages the power of transformer models, specifically T5, to process and assess answers based on predefined correct responses.

---

## Features

- **Upload PDF Exams**: Students or instructors can upload scanned exam papers in PDF format.
- **Automatic Parsing**: The backend extracts questions, student responses, and correct answers from the uploaded document.
- **Feedback Generation**: Using a fine-tuned T5 model, the application provides accurate and context-aware feedback for each question.
- **User-Friendly Interface**: A simple and intuitive UI built with Streamlit.

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/YourUsername/AceTrack.git
    cd AceTrack
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Additional Libraries**:
    Ensure `sentencepiece` is installed for the T5 tokenizer:
    ```bash
    pip install sentencepiece
    ```

5. **Set Up CUDA (Optional)**:
    If running on a GPU, install CUDA and cuDNN compatible with TensorFlow.

---

## Usage

1. **Start the Backend**:
    ```bash
    python app.py
    ```

2. **Start the Frontend**:
    ```bash
    streamlit run frontend.py
    ```

3. **Access the Application**:
    Open your browser and navigate to `http://localhost:8501`.

4. **Upload a PDF File**:
    - Drag and drop a PDF of the exam.
    - View the feedback generated for each question.

---

## Reassembling Model Weights

Due to GitHub's file size limitations, the model weights have been split into smaller chunks. To reassemble and use them, follow the steps below:

1. **Ensure All Chunks are Present**:
    The following files must exist in the project directory:
    - `AceTrack_T5_weights.part-aa`
    - `AceTrack_T5_weights.part-ab`
    - `AceTrack_T5_weights.part-ac`

2. **Rejoin the Chunks**:
    Use the `cat` command (or equivalent for your OS):
    ```bash
    cat AceTrack_T5_weights.part-* > AceTrack_T5_weights.pt
    ```

    On Windows, you can use:
    ```cmd
    copy /b AceTrack_T5_weights.part-aa + AceTrack_T5_weights.part-ab + AceTrack_T5_weights.part-ac AceTrack_T5_weights.pt
    ```

3. **Verify Rejoined File**:
    Confirm the file has been reassembled:
    ```bash
    ls -lh AceTrack_T5_weights.pt
    ```

4. **Load the Model**:
    Use the following Python code to load the model and tokenizer:
    ```python
    from transformers import T5Tokenizer, T5ForConditionalGeneration
    import torch

    # Paths
    weights_path = "AceTrack_T5_weights.pt"
    tokenizer_path = "AceTrack_T5_tokenizer"

    # Load tokenizer
    tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

    # Load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)

    print("Model and tokenizer loaded successfully.")
    ```

---

## Project Structure

```plaintext
AceTrack/
├── app.py                 # Backend script
├── frontend.py            # Frontend script
├── requirements.txt       # List of dependencies
├── AceTrack_T5_weights.part-aa  # Model weights (chunked)
├── AceTrack_T5_weights.part-ab  # Model weights (chunked)
├── AceTrack_T5_weights.part-ac  # Model weights (chunked)
├── AceTrack_T5_tokenizer/ # Tokenizer files
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── spiece.model
│   └── added_tokens.json
└── README.md              # This README file
