import streamlit as st
from pathlib import Path  
from pypdf import PdfReader 
from docx import Document
import re 

from transformers import pipeline

# Getting checkpoints of the model 
model_checkpoint = "atharvamundada99/bert-large-question-answering-finetuned-legal"
question_answerer = pipeline("question-answering", model=model_checkpoint, force_download=True, 
                             resume_download = True)

def context_handiling(file_path,type_):

  if type_ == 'pdf':
    reader = PdfReader(file_path) 
  
   # Import the PdfReader class from PyPDF2 library to work with PDFs.

    context = ''
    for i in reader.pages:
      context += i.extract_text()

   #   Extract text content from each page using the extract_text() method.

    step_1=re.findall('[A-Za-z0-9._,]+',context)
    context = (' ').join(step_1)
    return context
  
  elif type_ == 'docx':
    #  Import the Document class from python-docx library to work with docx files.

    document = Document(file_path)
    context = ''
    for paragraph in document.paragraphs:
      context += paragraph.text
    #  Extract text content from each paragraph using the text property.

    return context

  else:
    return False

def get_answer(question,context):
  # function to get the answer from the cotext by using context
  an = question_answerer(question=question, context=context)
  return an['answer']



# ============ USER INTERFACE ================= #


def main():



    st.set_page_config(page_title="AI Assistant", page_icon=":robot:")

    st.sidebar.header("Input Options")

    # File upload with selection for PDF or Docx
    uploaded_file = st.sidebar.file_uploader("Upload a PDF or Docx file (optional)",
                                              type=["pdf", "docx"])
    file_type = None
    if uploaded_file is not None:
        file_type = Path(uploaded_file.name).suffix

    # Question input from the user
    user_question = st.text_input("Ask your question:")

    # Display area for text and answer
    st.header("Text and Answer")

    # Display uploaded text (if applicable)
    if uploaded_file is not None:
        if file_type == ".pdf" or file_type == ".docx":
            st.write("Text extraction from uploaded file is not yet implemented.")
            if file_type == ".pdf" : 
                context =  context_handiling(uploaded_file,'pdf') 
            else : 
                context =  context_handiling(uploaded_file,'docx') 
        else:
            st.error("Unsupported file type. Please upload a PDF or Docx file.")
    else:
        # User might not have uploaded a file, handle it gracefully
        st.write("No file uploaded. You can either upload a file or directly enter text below.")

    # Get text from uploaded file or user input
   
    if uploaded_file is not None and (file_type == ".pdf" or file_type == ".docx"):
        pass
    else:
        context = st.text_area("Enter text here (optional):", height=100)

    # Call AI model only if there's text to process and a question is asked
    if context and user_question:
        answer = get_answer(user_question,context)  
        st.write(f"Answer: {answer}")

    # Option to ask another question or upload a new file
    st.subheader("What would you like to do next?")
    if st.button("Ask another question"):
        st.experimental_rerun()  # Reset the app for a new interaction
    if st.button("Upload a new file"):
        st.experimental_rerun()  # Reset the    app for a new file

if __name__ == "__main__":
    main()
