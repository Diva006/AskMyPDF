import streamlit as st
import fitz  # PyMuPDF

st.title("📚 StudyMate – PDF Q&A (No AI Dependencies)")

# ---------------- PDF Upload & Text Extraction ---------------- #
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf:
    pdf = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text = ""
    for page in pdf:
        pdf_text += page.get_text()
    st.success("✅ Text extracted from PDF")
    st.text_area("Preview of extracted text", pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""), height=200)

    # ---------------- Question Input ---------------- #
    user_question = st.text_input("Ask a question about the PDF content:")

    if user_question:
        st.info("🔍 **Searching for relevant content...**")
        
        # Simple keyword-based search
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
            for i, sentence in enumerate(found_sentences[:10]):  # Show first 10 matches
                st.write(f"**{i+1}.** {sentence}")
        else:
            st.warning("No matching content found. Try different keywords or check the full text below.")
        
        # Show context around matches
        if found_sentences:
            st.markdown("### 📄 **Relevant Context:**")
            context_text = " ".join(found_sentences[:5])  # First 5 matches
            st.text_area("Context from PDF", context_text, height=200)
        
        # Option to show full text
        if st.checkbox("Show full PDF text"):
            st.text_area("Full PDF Text", pdf_text, height=400)
            
        # Simple summary
        st.markdown("### 📝 **Quick Summary:**")
        word_count = len(pdf_text.split())
        sentence_count = len(pdf_text.split('.'))
        st.write(f"• **Word count:** {word_count}")
        st.write(f"• **Sentence count:** {sentence_count}")
        st.write(f"• **Relevant matches:** {len(found_sentences)}")
        
else:
    st.info("⬆️ Upload a PDF to begin.")

st.markdown("---")
st.markdown("**Note:** This version uses keyword search instead of AI. For AI features, install torch and transformers.")
