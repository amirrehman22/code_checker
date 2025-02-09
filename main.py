import streamlit as st
from docx import Document
from openai import OpenAI
from io import BytesIO
import os

# Streamlit User Interface
st.title("📌 Code Evaluator")

# Function to extract code from the DOCX file
def extract_code_from_docx(file):
    try:
        doc = Document(file)
        code_blocks = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(code_blocks) if code_blocks else "No code found in the document."
    except Exception as e:
        return f"Error reading file: {e}"

# Upload file
uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

if uploaded_file:
    # Extract the code from the DOCX file
    code = extract_code_from_docx(uploaded_file)
    
    if "Error" in code or code.strip() == "No code found in the document.":
        st.error(code)
    else:
        # API Key Handling
        api_key = os.getenv("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")  # Use environment variable
        if not api_key:
            st.error("API key not found. Set OPENAI_API_KEY in your environment.")
        else:
            client = OpenAI(api_key=api_key)

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert code evaluator."},
                        {"role": "user", "content": f"Evaluate the following code and provide detailed feedback, including identifying errors, corrections, and a final mark out of 10:\n{code}"}
                    ]
                )
                
                evaluation = response.choices[0].message.content
                
                # Show the result
                st.subheader("Code Evaluation:")
                st.write(evaluation)
                
                # Function to create a Word file from text
                def save_text_to_docx(text, filename):
                    doc = Document()
                    doc.add_paragraph(text)
                    byte_io = BytesIO()
                    doc.save(byte_io)
                    byte_io.seek(0)
                    return byte_io, f"{filename}_evaluation.docx"
                
                # Create Word file for download
                uploaded_name = os.path.splitext(uploaded_file.name)[0]
                word_file, filename = save_text_to_docx(evaluation, uploaded_name)

                st.download_button(
                    label="📥 Download Evaluation as Word File",
                    data=word_file,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            except Exception as e:
                st.error(f"Error during evaluation: {e}")
