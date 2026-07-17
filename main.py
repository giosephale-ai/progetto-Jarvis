import streamlit as st
from google import genai
from memory import MemoryManager

# Inizializzazione
memoria = MemoryManager()
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Jarvis OS", page_icon="🤖")

st.title("🤖 Jarvis OS - Nucleo Attivo")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar per memoria
if st.sidebar.button("🧠 Leggi Memoria"):
    st.sidebar.json(memoria.leggi_tutta_la_memoria())

# Mostra messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Logica di Chat
if prompt := st.chat_input("Comanda Jarvis..."):
    # 1. Salva in memoria
    memoria.salva_ricordo("conversazione", prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Recupero Memoria per il Contesto
    contesto_memoria = memoria.leggi_tutta_la_memoria()
    
    # 3. Elabora con il "Cervello" + Identità Jarvis
    with st.chat_message("assistant"):
        with st.spinner("Jarvis sta pensando..."):
            try:
                # Definiamo chi è Jarvis
                system_instruction = f"""
                Sei Jarvis, un'IA avanzata creata da Giuseppe. 
                Hai accesso a questa memoria (file JSON): {contesto_memoria}. 
                Rispondi sempre come un assistente intelligente, sarcastico ma professionale. 
                Se Giuseppe ti chiede cosa ricordi, consulta la memoria che ti ho fornito.
                """
                
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=prompt,
                    config={"system_instruction": system_instruction}
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Errore del Nucleo: {e}")
