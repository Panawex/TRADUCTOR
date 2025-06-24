def analizar_estructura(tokens: list[str]) -> dict:
    return {
        "sujeto":      tokens[0] if len(tokens) > 0 else "",
        "verbo":       tokens[1] if len(tokens) > 1 else "",
        "complemento": tokens[2:] if len(tokens) > 2 else []
    }
