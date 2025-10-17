#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI para Ejercicio 3 (hoja tipo Excel).

Subcomandos:
  insert  --row R --col C --value V
  update  --row R --col C --value V
  has     --row R --col C
  preview
  row     --row R
  col     --col C

Restricciones:
- Python 3.13
- Solo stdlib (argparse)
- Sin usar helpers prohibidos para manejo de listas/cadenas (in, find, index, sort, etc.) en la lógica de hoja.
"""

import argparse
import sys
from main_cli import Sheet


def parse_int(value_str, default=None):
    try:
        return int(value_str)
    except Exception:
        return default


def parse_float(value_str, default=None):
    try:
        return float(value_str)
    except Exception:
        return default


def main():
    sheet = Sheet()

    parser = argparse.ArgumentParser(
        description="Hoja básica: insertar, actualizar, validar, preview, sumar por fila/columna."
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    # insert
    p_insert = sub.add_parser("insert", help="Insertar valor en celda vacía")
    p_insert.add_argument("--row", type=int, required=True)
    p_insert.add_argument("--col", type=int, required=True)
    p_insert.add_argument("--value", type=str, required=True)

    # update
    p_update = sub.add_parser("update", help="Actualizar valor en celda existente")
    p_update.add_argument("--row", type=int, required=True)
    p_update.add_argument("--col", type=int, required=True)
    p_update.add_argument("--value", type=str, required=True)

    # has
    p_has = sub.add_parser("has", help="Validar si una celda tiene información")
    p_has.add_argument("--row", type=int, required=True)
    p_has.add_argument("--col", type=int, required=True)

    # preview
    sub.add_parser("preview", help="Mostrar preview de toda la hoja")

    # row
    p_row = sub.add_parser("row", help="Recuperar elementos de una fila y sumar")
    p_row.add_argument("--row", type=int, required=True)

    # col
    p_col = sub.add_parser("col", help="Recuperar elementos de una columna y sumar")
    p_col.add_argument("--col", type=int, required=True)

    args = parser.parse_args(sys.argv[1:])

    # Para demo rápida: empezamos con algunos datos como en el ejemplo del _demo()
    sheet.insert_cell(1, 1, 10)
    sheet.insert_cell(1, 2, 20)
    sheet.insert_cell(2, 1, "hola")
    sheet.insert_cell(3, 3, 7.5)
    sheet.update_cell(1, 2, 25)

    if args.cmd == "insert":
        # intentar castear numéricos cuando sea posible
        v_int = parse_int(args.value)
        v = v_int if v_int is not None else parse_float(args.value, args.value)
        ok = sheet.insert_cell(args.row, args.col, v)
        print("OK" if ok else "Celda ocupada")

    elif args.cmd == "update":
        v_int = parse_int(args.value)
        v = v_int if v_int is not None else parse_float(args.value, args.value)
        ok = sheet.update_cell(args.row, args.col, v)
        print("OK" if ok else "Celda inexistente")

    elif args.cmd == "has":
        print("True" if sheet.has_value(args.row, args.col) else "False")

    elif args.cmd == "preview":
        print(sheet.preview())

    elif args.cmd == "row":
        vals, total = sheet.row_values_and_sum(args.row)
        print("Valores:", vals)
        print("Suma:", total)

    elif args.cmd == "col":
        vals, total = sheet.col_values_and_sum(args.col)
        print("Valores:", vals)
        print("Suma:", total)


if __name__ == "__main__":
    main()
