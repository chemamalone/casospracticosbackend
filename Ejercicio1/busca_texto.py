from function_search_text import normalize_text, kmp_count

ARCHIVO_PARRAFO = r"D:\prueba tecnica\Ejercicio 1\parrafo.txt"
TEXTO_A_BUSCAR = "logística"

from busca_texto import ARCHIVO_PARRAFO, TEXTO_A_BUSCAR
from function_search_text import normalize_text, kmp_count

def run():
    with open(ARCHIVO_PARRAFO, "r", encoding="utf-8") as f:
        paragraph = f.read()

    paragraph_n = normalize_text(paragraph)
    text_n = normalize_text(TEXTO_A_BUSCAR)

    occurrences = kmp_count(paragraph_n, text_n)
    print(f"{occurrences} ocurrencias encontradas")

if __name__ == "__main__":
    run()
