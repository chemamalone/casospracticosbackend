DECISIONES DE DISEÑO Y EXPLICACIÓN TÉCNICA


Ejercicio 1
- Se evita el uso de `in`, `find` o expresiones regulares para simular un substring search manual.
- Se recorre el texto carácter a carácter, comparando con el patrón.
- Permite extenderse fácilmente para análisis de archivos grandes o texto multilineal.

Ejercicio 2
- Muestra control de estructuras condicionales, bucles y funciones puras.
- Los filtros se implementan a bajo nivel (sin `filter()` ni `list comprehensions`).
- El código está preparado para agregar validaciones dinámicas o combinadas.

Ejercicio 3
- La clase `Sheet` encapsula toda la lógica de la hoja de cálculo.
- Cada celda se maneja con coordenadas `(row, col)` y se almacena en un diccionario interno: {(row, col): value}
- Los métodos `insert_cell`, `update_cell`, `has_value`, `preview`, `row_values_and_sum` y `col_values_and_sum` permiten simular operaciones básicas de Excel sin librerías externas.
- `argparse` gestiona subcomandos de manera limpia, similar a una CLI profesional (`git`, `docker`, etc.).
- Los tipos se infieren automáticamente (`int`, `float`, `str`) al insertar o actualizar.


REQUISITOS

- Python 3.13
- Editor de texto recomendado: Visual Studio Code
- No se utilizan librerías externas (solo `argparse`, `json`, etc.)

"""
