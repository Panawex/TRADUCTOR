from config.conexion import conectar_bd
from typing import Optional, List, Dict

def buscar_traduccion_palabra(palabra: str) -> Optional[str]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT pk.raiz
        FROM palabra_es pe
        JOIN traduccion t ON pe.id = t.palabra_es_id
        JOIN palabra_ki pk ON pk.id = t.palabra_ki_id
        WHERE pe.lema = %s
        LIMIT 1
    """, (palabra,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row["raiz"] if row else None

def buscar_pronombre_ki(pronombre_es: str) -> Optional[str]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT pronombre_ki FROM persona WHERE pronombre_es = %s LIMIT 1",
        (pronombre_es,)
    )
    row = cur.fetchone(); cur.close(); conn.close()
    return row["pronombre_ki"] if row else None

def buscar_persona_id(pronombre_es: str) -> Optional[int]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id FROM persona WHERE pronombre_es = %s LIMIT 1",
        (pronombre_es,)
    )
    row = cur.fetchone(); cur.close(); conn.close()
    return row["id"] if row else None

def buscar_numero_palabra(lema: str) -> Optional[str]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT numero FROM palabra_es WHERE lema = %s LIMIT 1",
        (lema,)
    )
    row = cur.fetchone(); cur.close(); conn.close()
    return row["numero"] if row else None

def buscar_morfemas_complemento(frase_es: str) -> List[Dict]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.id, m.forma, m.modo_aplicacion, m.elemento_a_eliminar
        FROM traduccion_morfema tm
        JOIN morfema m ON tm.morfema_id = m.id
        WHERE tm.frase_es = %s
    """, (frase_es,))
    res = cur.fetchall(); cur.close(); conn.close()
    return res

def buscar_morfema_desde_frase(frase_es: str) -> Optional[Dict]:
    lst = buscar_morfemas_complemento(frase_es)
    return lst[0] if lst else None

def obtener_marcadores_modo(tipo_modo: str) -> List[Dict]:
    conn = conectar_bd(); cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT marcador, posicion FROM modo_oracional WHERE tipo = %s",
        (tipo_modo,)
    )
    res = cur.fetchall(); cur.close(); conn.close()
    return res
