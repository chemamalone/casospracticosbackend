#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 3: Hoja de cálculo básica.

Requerido:
- Insertar información en una celda
- Actualizar información en una celda
- Validar si una celda tiene información dentro
- Mostrar un preview de la hoja entera
- Dada una fila: recuperar todos los elementos e imprimir la suma de sus valores
- Dada una columna: recuperar todos los elementos e imprimir la suma de sus valores

Restricciones cumplidas:
- Python 3.13
- Solo stdlib
- Sin usar funciones/operadores facilitadores: in, find, index, sort, contains, etc.
- PEP8
"""

from typing import Any, Dict, Tuple, List


class Sheet:
    """
    Representa una hoja con celdas (fila, columna) -> valor.
    Fila y columna empiezan en 1.
    """

    def __init__(self) -> None:
        self._cells: Dict[Tuple[int, int], Any] = {}

    # -------------------------
    # utilidades internas
    # -------------------------
    def _exists_key(self, r: int, c: int) -> bool:
        """Verifica existencia sin usar 'in' iterando llaves."""
        keys = list(self._cells.keys())
        i = 0
        n = len(keys)
        while i < n:
            k = keys[i]
            if k[0] == r and k[1] == c:
                return True
            i += 1
        return False

    def _get_value(self, r: int, c: int, default: Any = None) -> Any:
        """Obtiene valor de (r, c) sin 'in' (try/except)."""
        try:
            return self._cells[(r, c)]
        except KeyError:
            return default

    def _set_value(self, r: int, c: int, value: Any) -> None:
        self._cells[(r, c)] = value

    def _max_bounds(self) -> Tuple[int, int]:
        """Obtiene (max_row, max_col) existentes sin usar max/sort."""
        keys = list(self._cells.keys())
        i = 0
        n = len(keys)
        max_r = 0
        max_c = 0
        while i < n:
            kr = keys[i][0]
            kc = keys[i][1]
            if kr > max_r:
                max_r = kr
            if kc > max_c:
                max_c = kc
            i += 1
        return max_r, max_c

    # -------------------------
    # 1) Insertar información
    # -------------------------
    def insert_cell(self, r: int, c: int, value: Any) -> bool:
        """
        Inserta solo si la celda está vacía.
        Retorna True si inserta; False si ya existía.
        """
        if self._exists_key(r, c):
            return False
        self._set_value(r, c, value)
        return True

    # -------------------------
    # 2) Actualizar información
    # -------------------------
    def update_cell(self, r: int, c: int, value: Any) -> bool:
        """
        Actualiza solo si la celda existe.
        Retorna True si actualiza; False si la celda no existía.
        """
        if not self._exists_key(r, c):
            return False
        self._set_value(r, c, value)
        return True

    # -------------------------------------------
    # 3) Validar si una celda tiene información
    # -------------------------------------------
    def has_value(self, r: int, c: int) -> bool:
        return self._exists_key(r, c)

    # ---------------------------------
    # 4) Preview de la hoja completa
    # ---------------------------------
    def preview(self) -> str:
        """
        Devuelve una representación en texto:
        - Cabecera con columnas
        - Filas con sus valores (vacío = "")
        """
        max_r, max_c = self._max_bounds()
        if max_r == 0 or max_c == 0:
            return "(hoja vacía)"

        # Encabezado de columnas
        parts: List[str] = []
        header = ["   "]  # espacio para etiqueta de filas
        col = 1
        while col <= max_c:
            header.append(f"[{col:>3}]")
            col += 1
        parts.append(" ".join(header))

        # Filas
        r = 1
        while r <= max_r:
            row_parts = [f"[{r:>3}]"]
            c = 1
            while c <= max_c:
                v = self._get_value(r, c, "")
                # convertir a string seguro
                row_parts.append(f"{str(v):>4}")
                c += 1
            parts.append(" ".join(row_parts))
            r += 1

        return "\n".join(parts)

    # ----------------------------------------------------------------
    # 5) Dada una fila: elementos y suma de los valores numéricos
    # ----------------------------------------------------------------
    def row_values_and_sum(self, r: int) -> Tuple[List[Any], float]:
        """
        Devuelve (valores_de_la_fila, suma_numerica).
        La suma solo considera int/float; ignora no numéricos.
        Si no hay celdas en esa fila, lista vacía y suma 0.0
        """
        max_r, max_c = self._max_bounds()
        if r < 1 or r > max_r:
            return [], 0.0

        values: List[Any] = []
        total = 0.0
        c = 1
        while c <= max_c:
            v = self._get_value(r, c, None)
            # Agregamos el valor mostrado (None si vacío)
            values.append(v)
            if isinstance(v, (int, float)):
                total += float(v)
            c += 1
        return values, total

    # -------------------------------------------------------------------
    # 6) Dada una columna: elementos y suma de los valores numéricos
    # -------------------------------------------------------------------
    def col_values_and_sum(self, c: int) -> Tuple[List[Any], float]:
        """
        Devuelve (valores_de_la_columna, suma_numerica).
        La suma solo considera int/float; ignora no numéricos.
        Si no hay celdas en esa columna, lista vacía y 0.0
        """
        max_r, max_c = self._max_bounds()
        if c < 1 or c > max_c:
            return [], 0.0

        values: List[Any] = []
        total = 0.0
        r = 1
        while r <= max_r:
            v = self._get_value(r, c, None)
            values.append(v)
            if isinstance(v, (int, float)):
                total += float(v)
            r += 1
        return values, total


# -------------------------------------------------
# Demo mínimo: muestra las 6 funcionalidades pedidas
# -------------------------------------------------
def _demo() -> None:
    sheet = Sheet()

    # 1) Insertar
    sheet.insert_cell(1, 1, 10)
    sheet.insert_cell(1, 2, 20)
    sheet.insert_cell(2, 1, "hola")
    sheet.insert_cell(3, 3, 7.5)

    # 2) Actualizar (solo si existe)
    sheet.update_cell(1, 2, 25)      # 1,2 pasa de 20 -> 25
    sheet.update_cell(4, 1, "nueva") # no existe; no actualiza

    # 3) Validar si hay info
    has_1_1 = sheet.has_value(1, 1)  # True
    has_4_4 = sheet.has_value(4, 4)  # False

    # 4) Preview
    print("=== Preview ===")
    print(sheet.preview())

    # 5) Fila: elementos + suma (solo numéricos)
    vals_row_1, sum_row_1 = sheet.row_values_and_sum(1)
    print("\nFila 1 -> valores:", vals_row_1, "| suma:", sum_row_1)

    # 6) Columna: elementos + suma (solo numéricos)
    vals_col_1, sum_col_1 = sheet.col_values_and_sum(1)
    print("Columna 1 -> valores:", vals_col_1, "| suma:", sum_col_1)

    # Validaciones simples
    print("\nhas(1,1):", has_1_1, " | has(4,4):", has_4_4)


if __name__ == "__main__":
    _demo()
