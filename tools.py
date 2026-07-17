from duckduckgo_search import DDGS

class JarvisTools:
    """Modulo contenente le abilità speciali di Jarvis."""
    
    @staticmethod
    def cerca_sul_web(query):
        """Esegue una ricerca web e stampa nel log i risultati trovati."""
        print(f"DEBUG: Jarvis sta cercando: {query}") # Questo apparirà nei Log
        try:
            with DDGS() as ddgs:
                # Proviamo a forzare una ricerca più semplice
                results = list(ddgs.text(query, max_results=3))
                print(f"DEBUG: Risultati grezzi ricevuti: {results}") # Questo apparirà nei Log
                
                if not results:
                    return None
                
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        except Exception as e:
            print(f"DEBUG: ERRORE NELLA RICERCA: {e}")
            return None
