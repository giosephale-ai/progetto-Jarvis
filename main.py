import streamlit as st
from google import genai
from memory import MemoryManager
from tools import JarvisTools # Importiamo le nuove abilità

# Inizializzazione
memoria = MemoryManager()
tools = JarvisTools() # Inizializziamo gli strumenti
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Jarvis OS", page_icon="🤖")

st.title("🤖 Jarvis OS - Nucleo Attivo")

# Sidebar
if st.sidebar.button("🧠 Leggi Memoria"):
    st.sidebar.json(memoria.leggi_tutta_la_memoria())

# Opzione per il Web
st.sidebar.divider()
web_enabled = st.sidebar.checkbox("🌐 Abilita Ricerca Web", value=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Comanda Jarvis..."):
    memoria.salva_ricordo("conversazione", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis sta analizzando..."):
            try:
                # Logica di ricerca opzionale
                info_web = ""
                if web_enabled:
                    info_web = f"\n\nInformazioni trovate sul web: {tools.cerca_sul_web(prompt)}"

                contesto_memoria = memoria.leggi_tutta_la_memoria()
                
                system_instruction = f"""
                Sei Jarvis. Hai accesso alla memoria: {contesto_memoria}.
                {info_web}
                Rispondi basandoti sulle info web se presenti, altrimenti usa la tua conoscenza.
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
