import spacy

# spaCy con el modelo español
_nlp = spacy.load("es_core_news_sm")

def lematizar_espanol(token: str) -> str:
    """
    Usa spaCy para devolver el lema, en minúscula.
    (p.ej. 'juego'→'jugar', 'jugué'→'jugar', 'comeré'→'comer')
    """
    doc = _nlp(token)
    return doc[0].lemma_.lower()
