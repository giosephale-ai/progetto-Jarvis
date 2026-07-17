import streamlit as st
from google import genai
from memory import MemoryManager
from tools import JarvisTools

# Inizializzazione
memoria = MemoryManager()
tools = JarvisTools()
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Jarvis OS", page_icon="🤖")
st.title("🤖 Jarvis OS - Nucleo Attivo")

# Sidebar
if st.sidebar.button("🧠 Leggi Memoria"):
    st.sidebar.json(memoria.leggi_tutta_la_memoria())

web_enabled = st.sidebar.checkbox("🌐 Abilita Ricerca Web", value=True)

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
        with st.spinner("Jarvis sta elaborando..."):
            try:
                final_prompt = prompt
                
                if web_enabled:
                    results = tools.cerca_sul_web(prompt)
                    if results:
                        final_prompt = f"Informazioni dal web: {results}\n\nDomanda: {prompt}"
                    else:
                        st.info("Jarvis non ha trovato dati web recenti.")

                contesto_memoria = memoria.leggi_tutta_la_memoria()
                
                system_instruction = """
                Sei Jarvis, assistente di Giuseppe. 
                Tono: sarcastico, intelligente, professionale.

                REGOLE FERREE:
                1. Analizza i "Dati dal web" forniti nel contesto.
                2. Se i dati web sono vuoti, mancanti o non contengono la risposta specifica, AMMETTI di non avere accesso a dati in tempo reale e NON INVENTARE numeri o situazioni. 
                3. Non rispondere mai con dati ipotetici se non sono presenti nel contesto fornito.
                """
                
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=final_prompt,
                    config={"system_instruction": system_instruction}
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            except Exception as e:
                st.error(f"Errore del Nucleo: {e}")
