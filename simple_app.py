import streamlit as st
import fitz  # PyMuPDF

st.title("📚 StudyMate – PDF Text Extractor & Simple Q&A")

# ---------------- PDF Upload & Text Extraction ---------------- #
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf:
    pdf = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text = ""
    for page in pdf:
        pdf_text += page.get_text()
    
    st.success("✅ Text extracted from PDF")
    
    # Show text preview
    st.text_area("Preview of extracted text", pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""), height=200)
    
    # ---------------- Simple Search Functionality ---------------- #
    user_question = st.text_input("Search for keywords in the PDF:")
    
    if user_question:
        # Simple keyword search
        keywords = user_question.lower().split()
        found_sentences = []
        
        # Split text into sentences
        sentences = pdf_text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                found_sentences.append(sentence.strip())
        
        if found_sentences:
            st.success(f"Found {len(found_sentences)} relevant sentences:")
            for i, sentence in enumerate(found_sentences[:5]):  # Show first 5 matches
                st.write(f"{i+1}. {sentence}")
        else:
            st.warning("No matching sentences found. Try different keywords.")
    
    # ---------------- Full Text Display ---------------- #
    if st.checkbox("Show full extracted text"):
        st.text_area("Full PDF Text", pdf_text, height=400)
        
else:
    st.info("⬆️ Upload a PDF to begin.")

"""
Simple StudyMate - PDF Text Extractor
- Upload PDFs and extract text
- Search for keywords
- View full text content
"""
