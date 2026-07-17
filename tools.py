from duckduckgo_search import DDGS

class JarvisTools:
    """Modulo contenente le abilità speciali di Jarvis."""
    
    @staticmethod
    def cerca_sul_web(query):
        """Esegue una ricerca web veloce."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "Nessun risultato trovato."
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        except Exception as e:
            return f"Errore durante la navigazione web: {e}"
