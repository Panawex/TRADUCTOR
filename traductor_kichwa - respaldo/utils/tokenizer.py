import re
from db.consultas import buscar_morfema_desde_frase

def normalizar_texto(texto: str) -> str:
    """
    Sólo pasa a minúsculas; conserva tildes para lematización correcta.
    """
    return texto.lower()

def tokenizar_oracion(texto: str) -> list[str]:
    """
    Elimina puntuación pero preserva letras acentuadas.
    """
    # quitamos todo lo que no sea letra (incluye ÁÉÍÓÚñÑ), dígito o espacio
    texto = re.sub(r"[^\w\sÁÉÍÓÚáéíóúÑñ]", "", texto)
    return texto.split()

def agrupar_ngramas(tokens: list[str], buscar_morfema_desde_frase) -> list[str]:
    """
    Junta secuencias de 2–3 tokens que formen morfema compuesto.
    """
    out, i, n = [], 0, len(tokens)
    while i < n:
        match = None
        for size in (3, 2):
            if i + size <= n:
                frase = " ".join(tokens[i : i + size])
                if buscar_morfema_desde_frase(frase):
                    match = frase
                    break
        if match:
            out.append(match)
            i += size
        else:
            out.append(tokens[i])
            i += 1
    return out
