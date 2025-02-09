import streamlit as st
from docx import Document
from openai import OpenAI
from io import BytesIO
import os

# Streamlit User Interface
st.title("📌 Code Evaluator")

code = """
Question 1 
write Python program to add two numbers?
code:
def add_numbers(a b):
    return a + b

# Example usage
num1 = 5
num2 = 7
result = add_numbers(num1, num2)
print("Sum:" result)

"""
# Function to extract code from the DOCX file
def extract_code_from_docx(file_path):
    doc = Document(file_path)
    code_blocks = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(code_blocks)


# Upload file
uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])

if uploaded_file:
    # Save the uploaded file temporarily
    with open("uploaded_file.docx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract the code from the DOCX file
    code = extract_code_from_docx("uploaded_file.docx")
    

    client = OpenAI(
    api_key=os.getenv("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"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an expert code evaluator."},
        {"role": "user", "content": f"Evaluate the following code and provide detailed feedback, including identifying errors, corrections and  a final mark out of 10 :\n{code}"}]
        )
 
 


# Show the result
    evaluation = response.choices[0].message.content
    st.subheader("Code Evaluation:")
    st.write(evaluation)
    
    # Function to create a Word file from text
    def save_text_to_docx(text, uploaded_filename):
        doc = Document()
        doc.add_paragraph(text)
        byte_io = BytesIO()
        doc.save(byte_io)
        byte_io.seek(0)
        return byte_io, f"{uploaded_filename}_evaluate_file.docx"
    

    # Create Word file for download
    if uploaded_file and code:
        uploaded_name = os.path.splitext(uploaded_file.name)[0]  # Extract filename without extension
        word_file, filename = save_text_to_docx(evaluation, uploaded_name)

        st.download_button(
            label="📥 Download Evaluation as Word File",
            data=word_file,
            file_name=filename,  # ✅ File will be named as "uploaded_name_evaluate_file.docx"
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
