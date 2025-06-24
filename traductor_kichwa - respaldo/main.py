import re
from utils.tokenizer    import normalizar_texto, tokenizar_oracion, agrupar_ngramas
from utils.estructuras  import analizar_estructura
from utils.lemmatizer   import lematizar_espanol
from db.consultas       import (
    buscar_traduccion_palabra,
    buscar_pronombre_ki,
    buscar_persona_id,
    buscar_morfema_desde_frase,
    obtener_marcadores_modo
)
from db.ensamblador     import construir_oracion_kichwa

# Sufijos en Kichwa
SUF_PRESENT = {1:"ni",2:"nki",3:"n",4:"n",5:"nchik",6:"nkichik",7:"nkuna"}
SUF_PAST    = {1:"rkani",2:"rkanki",3:"rkan",4:"rkan",5:"rkanchik",6:"rkankichik",7:"rkanuna"}

def conjugar_present(inf_ki: str, pid: int) -> str:
    base = inf_ki[:-2] if inf_ki.endswith("na") else inf_ki
    return base + SUF_PRESENT.get(pid, "")

def conjugar_past(inf_ki: str, pid: int) -> str:
    base = inf_ki[:-2] if inf_ki.endswith("na") else inf_ki
    return base + SUF_PAST.get(pid, "")

def aplicar_morfema(raiz: str, morf: dict) -> str:
    modo = morf["modo_aplicacion"]
    if modo == "anexar":
        return raiz + morf["forma"]
    if modo == "eliminar_y_anexar":
        return raiz.replace(morf["elemento_a_eliminar"], "") + morf["forma"]
    if modo == "reemplazar":
        return raiz[:-len(morf["elemento_a_eliminar"])] + morf["forma"]
    return raiz

def construir_complemento(tokens: list[str]) -> list[str]:
    res, buf = [], []
    for t in tokens:
        m = buscar_morfema_desde_frase(t)
        if m:
            buf.append(m)
            continue
        raiz = buscar_traduccion_palabra(t)
        if not raiz:
            continue
        for mf in buf:
            raiz = aplicar_morfema(raiz, mf)
        buf.clear()
        res.append(raiz)
    return res

def detectar_modo(texto: str) -> str:
    t = texto.strip()
    if t.startswith("¿") or t.endswith("?"):
        return "pregunta"
    if " no " in f" {t.lower()} ":
        return "negacion"
    return "afirmacion"

def traducir_oracion(entrada: str) -> str:
    # 1) Normalizar sin quitar tildes
    norm = normalizar_texto(entrada)
    # 2) Tokenizar + agrupar morfemas
    toks = agrupar_ngramas(tokenizar_oracion(norm), buscar_morfema_desde_frase)
    # 3) Analizar estructura
    estr = analizar_estructura(toks)

    # 4) SUJETO
    sub_es = estr["sujeto"]
    sub_ki = buscar_pronombre_ki(sub_es) or ""
    pid    = buscar_persona_id(sub_es)   or 1

    # 5) VERBO
    v_es   = estr["verbo"]
    inf_es = lematizar_espanol(v_es)           # “juego”→“jugar”, “jugué”→“jugar”
    inf_ki = buscar_traduccion_palabra(inf_es) or inf_es

    # si tiene tilde o acabados de pretérito, usamos pasado…
    if re.search(r"[áéíóú]|aste|iste|ó|é|aron|ieron$", v_es):
        v_ki = conjugar_past(inf_ki, pid)
    else:
        v_ki = conjugar_present(inf_ki, pid)

    # 6) COMPLEMENTO
    comp_ki = construir_complemento(estr["complemento"])

    # 7) ENSAMBLAR + marcadores
    partes = {"sujeto": sub_ki, "verbo": v_ki, "complemento": comp_ki}
    modo   = detectar_modo(entrada)
    for m in obtener_marcadores_modo(modo):
        if m["posicion"] == "antes_verbo":
            partes["verbo"] = f"{m['marcador']} {partes['verbo']}"
        else:
            partes["verbo"] += f" {m['marcador']}"

    return construir_oracion_kichwa(partes)

if __name__ == "__main__":
    print("=== Traductor Español → Kichwa ===")
    while True:
        o = input("Oración (o 'salir'): ")
        if o.lower() in ("salir", "exit"):
            print("¡Hasta luego!")
            break
        print("Kichwa:", traducir_oracion(o))
