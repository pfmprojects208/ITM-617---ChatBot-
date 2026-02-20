import streamlit as st
import time
import os
from motor_rag import iniciar_rag

# 1. Page Configuration (Strictly Professional)
st.set_page_config(
    page_title="Enterprise Document AI | ITM-617",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for a Clean, Corporate Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1, h2, h3 {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #1f2937;
    }
    
    /* Dark mode text adjustment */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 { color: #f9fafb; }
    }
    
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    @media (prefers-color-scheme: dark) {
        [data-testid="stSidebar"] {
            background-color: #16181a;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar: Control Panel & Uploader
with st.sidebar:
    st.title("System Parameters")
    st.caption("Local RAG Engine Configuration")
    st.markdown("---")
    
    st.subheader("Knowledge Base")
    
    # Drag & Drop File Uploader
    uploaded_file = st.file_uploader("Upload PDF Document", type="pdf")
    
    pdf_path = None
    if uploaded_file is not None:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Index Ready: {uploaded_file.name}")
        pdf_path = uploaded_file.name
    else:
        st.info("Awaiting PDF upload to begin analysis.")
    
    st.markdown("---")
    st.subheader("Llama 3.1 Tuning")
    st.slider("Temperature (Creativity)", 0.0, 1.0, 0.1, 0.1, help="0.0 = Strict & factual. 1.0 = Highly creative.")
    st.slider("Retrieval Chunks (k)", 2, 8, 4, help="Number of document fragments retrieved per query.")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #888; font-size: 12px; margin-top: 20px;'>ITM-617 Document AI v1.0<br>Mateo & Team</div>", unsafe_allow_html=True)

# 4. Main Chat Area
st.title("Document Intelligence Agent")
st.markdown("Synthesizing answers based strictly on the uploaded knowledge base context.")
st.markdown("---")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "System initialized. Please upload a PDF in the sidebar to begin."}
    ]

# 6. Render Chat Messages (Using Streamlit's default professional SVGs)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input (Disabled until PDF is uploaded)
prompt = st.chat_input("Enter your query regarding the document...", disabled=not uploaded_file)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# 8. AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Reading PDF and querying Llama 3.1...*")
        
        # --- AQUÍ OCURRE LA MAGIA REAL ---
        try:
            # Llamamos a tu motor_rag.py pasándole el PDF subido y la pregunta
            respuesta_real = iniciar_rag(pdf_path, prompt)
            
            # Mostramos la respuesta real en la web
            message_placeholder.markdown(respuesta_real)
            
            # Guardamos la respuesta en el historial del chat
            st.session_state.messages.append({"role": "assistant", "content": respuesta_real})
            
        except Exception as e:
            # Por si algo falla (ej. el PDF está corrupto)
            error_msg = f"⚠️ **Error connecting to the engine:** {e}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})