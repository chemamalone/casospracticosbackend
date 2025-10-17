"""
CLI para Ejercicio 3 (hoja tipo Excel) con persistencia en JSON.

Subcomandos:
  insert  --row R --col C --value V
  update  --row R --col C --value V
  has     --row R --col C
  preview
  row     --row R
  col     --col C
  reset   (opcional) borra el estado guardado

Restricciones:
- Python 3.13
- Solo stdlib (argparse, json, os, sys)
"""

import argparse
import sys
import os
import json
from main_cli import Sheet

STATE_FILE = os.path.join(os.path.dirname(__file__), "sheet_state.json")


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


def _sheet_to_serializable(sheet):
    data = {}
    cells = getattr(sheet, "_cells", None)
    if isinstance(cells, dict):
        for (r, c), v in cells.items():
            data[f"{int(r)},{int(c)}"] = v
    else:
        data["_nopersist"] = True
    return data


def _serializable_to_sheet(data, sheet):
    """
    Carga el dict serializado en la hoja.
    """
    if not isinstance(data, dict) or "_nopersist" in data:
        return
    for key, v in data.items():
        if not isinstance(key, str) or "," not in key:
            continue
        rs, cs = key.split(",", 1)
        try:
            r = int(rs.strip())
            c = int(cs.strip())
        except ValueError:
            continue
        sheet.insert_cell(r, c, v)


def save_state(sheet):
    try:
        data = _sheet_to_serializable(sheet)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] No se pudo guardar estado: {e}", file=sys.stderr)


def load_state(sheet):
    if not os.path.exists(STATE_FILE):
        return False
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _serializable_to_sheet(data, sheet)
        return True
    except Exception as e:
        print(f"[WARN] No se pudo cargar estado: {e}", file=sys.stderr)
        return False


def init_demo_data(sheet):
    sheet.insert_cell(1, 1, 10)
    sheet.insert_cell(1, 2, 20)
    sheet.insert_cell(2, 1, "hola")
    sheet.insert_cell(3, 3, 7.5)
    sheet.update_cell(1, 2, 25)


def main():
    sheet = Sheet()

    parser = argparse.ArgumentParser(
        description="Hoja básica: insertar, actualizar, validar, preview, sumar por fila/columna (con persistencia)."
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

    # reset (opcional)
    sub.add_parser("reset", help="Borrar estado persistido y reiniciar demo")

    args = parser.parse_args(sys.argv[1:])

    # Cargar estado si existe; si no, inicializar demo
    loaded = load_state(sheet)
    if not loaded and args.cmd != "reset":
        init_demo_data(sheet)

    if args.cmd == "insert":
        # castear numéricos cuando sea posible
        v_int = parse_int(args.value)
        v = v_int if v_int is not None else parse_float(args.value, args.value)
        ok = sheet.insert_cell(args.row, args.col, v)
        print("OK" if ok else "Celda ocupada")
        if ok:
            save_state(sheet)

    elif args.cmd == "update":
        v_int = parse_int(args.value)
        v = v_int if v_int is not None else parse_float(args.value, args.value)
        ok = sheet.update_cell(args.row, args.col, v)
        print("OK" if ok else "Celda inexistente")
        if ok:
            save_state(sheet)

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

    elif args.cmd == "reset":
        try:
            if os.path.exists(STATE_FILE):
                os.remove(STATE_FILE)
        except Exception as e:
            print(f"[WARN] No se pudo borrar el estado: {e}", file=sys.stderr)
        sheet = Sheet()
        init_demo_data(sheet)
        save_state(sheet)
        print("Estado reiniciado a datos de demo.")


if __name__ == "__main__":
    main()
