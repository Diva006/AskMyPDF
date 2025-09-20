import streamlit as st
import fitz  # PyMuPDF

# Try to import transformers with error handling
try:
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
    TORCH_AVAILABLE = True
except ImportError as e:
    st.error(f"Required libraries not available: {e}")
    TRANSFORMERS_AVAILABLE = False
    TORCH_AVAILABLE = False

st.title("📚 StudyMate – AI-Powered PDF Q&A")

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
        if not TRANSFORMERS_AVAILABLE or not TORCH_AVAILABLE:
            st.error("❌ AI features are not available. Please install required dependencies:")
            st.code("pip install torch transformers")
            st.info("📄 **PDF Text Preview:** You can still view the extracted text below.")
            st.text_area("Extracted PDF Text", pdf_text, height=300)
        else:
            # Add a short context slice to keep demo fast (for production use RAG retrieval)
            context = pdf_text[:2000]
            messages = [{"role": "user", "content": f"{user_question}\n\nContext:\n{context}"}]

            # ---------- Approach 1: High-level pipeline ----------
            st.markdown("### 🔹 Granite – High-level pipeline")
            with st.spinner("Generating answer..."):
                try:
                    pipe = pipeline("text-generation", model="ibm-granite/granite-3.3-2b-instruct")
                    result = pipe(messages)
                    st.write(result)
                except Exception as e:
                    st.error(f"Error with pipeline: {e}")

            # ---------- Approach 2: Low-level model/tokenizer ----------
            st.markdown("### 🔹 Granite – Low-level model")
            with st.spinner("Generating answer..."):
                try:
                    tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
                    model = AutoModelForCausalLM.from_pretrained("ibm-granite/granite-3.3-2b-instruct")

                    inputs = tokenizer.apply_chat_template(
                        messages,
                        add_generation_prompt=True,
                        tokenize=True,
                        return_dict=True,
                        return_tensors="pt",
                    ).to(model.device)

                    outputs = model.generate(**inputs, max_new_tokens=40)
                    answer = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error with model: {e}")
else:
    st.info("⬆️ Upload a PDF to begin.")

"""
Run this in VS Code terminal:
    streamlit run studymate_app.py
"""
