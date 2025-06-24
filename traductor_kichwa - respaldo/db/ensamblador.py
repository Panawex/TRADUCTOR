def construir_oracion_kichwa(partes: dict) -> str:
    sujeto     = partes.get("sujeto", "")
    complemento = " ".join(partes.get("complemento", []))
    verbo      = partes.get("verbo", "")
    frase = f"{sujeto} {complemento} {verbo}".strip()
    return " ".join(frase.split())
