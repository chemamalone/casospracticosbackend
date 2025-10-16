import unicodedata

def normalize_text(s):
    """
    Normaliza el texto:
    - Convierte a minúsculas
    - Elimina acentos y diacríticos
    """
    s = s.lower()
    nfd = unicodedata.normalize("NFD", s)
    out = []
    i = 0
    n = len(nfd)
    while i < n:
        ch = nfd[i]
        cat = unicodedata.category(ch)
        if cat != "Mn":  # Mn = marca diacrítica
            out.append(ch)
        i += 1
    return "".join(out)


def build_lps(pattern):
    """
    Construye la tabla LPS (Longest Prefix Suffix)
    usada por el algoritmo KMP.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_count(text, pattern):
    """
    Cuenta las ocurrencias (incluyendo traslapes)
    de 'pattern' dentro de 'text' usando KMP.
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return 0

    lps = build_lps(pattern)
    i = 0  
    j = 0  
    count = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return count
