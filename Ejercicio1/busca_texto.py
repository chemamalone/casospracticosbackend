from function_search_text import normalize_text, kmp_count

ARCHIVO_PARRAFO = r"D:\prueba tecnica\Ejercicio 1\parrafo.txt"
TEXTO_A_BUSCAR = "logística"

from busca_texto import ARCHIVO_PARRAFO, TEXTO_A_BUSCAR
from function_search_text import normalize_text, kmp_count

def run():
    # Lee el párrafo desde archivo (UTF-8)
    with open(ARCHIVO_PARRAFO, "r", encoding="utf-8") as f:
        paragraph = f.read()

    # Normaliza ambos
    paragraph_n = normalize_text(paragraph)
    text_n = normalize_text(TEXTO_A_BUSCAR)

    # Cuenta ocurrencias
    occurrences = kmp_count(paragraph_n, text_n)

    # Salida concisa y clara
    print(f"{occurrences} ocurrencias encontradas")

if __name__ == "__main__":
    run()
