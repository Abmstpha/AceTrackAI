# AceTrackAI - A Student Feedback Generator

AceTrackAI is an AI-powered tool designed and developed by Abdellahi El Moustapha to evaluate student responses to historical questions and provide detailed, constructive feedback. It leverages the power of transformer models, specifically T5, to process and assess answers based on predefined correct responses.

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
    git clone https://github.com/Abmstpha/AceTrackAI.git
    cd AceTrackAI
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

### 1. **Reassemble the Model Weights**
Due to GitHub's file size limitations, the model weights have been:
1. Compressed into a `.gz` file: `AceTrack_T5_weights.pt.gz`.
2. Split into smaller chunks:
   - `AceTrack_T5_weights.part-aa`
   - `AceTrack_T5_weights.part-ab`
   - `AceTrack_T5_weights.part-ac`

To reassemble the weights:

#### **Step 1: Combine the Split Files**
- On Linux/macOS, run:
    ```bash
    cat AceTrack_T5_weights.part-* > AceTrack_T5_weights.pt.gz
    ```
- On Windows, run:
    ```cmd
    copy /b AceTrack_T5_weights.part-aa + AceTrack_T5_weights.part-ab + AceTrack_T5_weights.part-ac AceTrack_T5_weights.pt.gz
    ```

#### **Step 2: Decompress the `.gz` File**
- On Linux/macOS, run:
    ```bash
    gunzip AceTrack_T5_weights.pt.gz
    ```
- On Windows, use tools like 7-Zip to decompress the file.

#### **Step 3: Verify the Reassembled File**
Run the following command to ensure the `AceTrack_T5_weights.pt` file is correctly reassembled:
```bash
ls -lh AceTrack_T5_weights.pt
   ```

2. **Start the Backend**:
    ```bash
    python app.py
    ```

3. **Start the Frontend**:
    ```bash
    streamlit run frontend.py
    ```

4. **Access the Application**:
    Open your browser and navigate to `http://localhost:8501`.

5. **Upload a PDF File**:
    - Drag and drop a PDF of the exam.
    - View the feedback generated for each question.

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
