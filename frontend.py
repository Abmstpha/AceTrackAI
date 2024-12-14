import streamlit as st
import requests
import json

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000/upload"


# # Streamlit app title
# st.title("AceTrack AI") 
# st.markdown(
#     "Upload a scan of the student exam to generate feedback."
# )

st.markdown(
    "<h1 style='text-align: center;'>AceTrack AI</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Upload a scan of the student exam to generate feedback.</p>", 
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    # Show the uploaded file
    st.write(f"File uploaded: {uploaded_file.name}")

    # Button to process the uploaded file
    if st.button("Generate Feedback"):
        try:
            # Send the file to the backend
            files = {"file": uploaded_file}
            with st.spinner("Processing the uploaded file..."):
                response = requests.post(BACKEND_URL, files=files)

            # Check for errors in the response
            if response.status_code == 200:
                feedback_data = response.json()

                # Display the feedback for each question
                st.markdown("### Feedback Results")
                for idx, entry in enumerate(feedback_data):
                    st.markdown(f"**Question {idx + 1}:** {entry['Question']}")
                    st.markdown(f"*Student Answer:* {entry['Student Answer']}")
                    st.markdown(f"*Correct Answer:* {entry['Correct Answer']}")
                    st.markdown(f"**Feedback:** {entry['Feedback']}")
                    st.markdown("---")
            else:
                # Handle errors from the backend
                error_message = response.json().get("error", "Unknown error occurred.")
                st.error(f"Error: {error_message}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend: {e}")
