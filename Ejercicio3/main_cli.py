from typing import Any, Dict, Tuple, List

class Sheet:
    def __init__(self) -> None:
        self._cells: Dict[Tuple[int, int], Any] = {}

    def _exists_key(self, r: int, c: int) -> bool:
        return (r, c) in self._cells

    def _get_value(self, r: int, c: int, default: Any = None) -> Any:
        return self._cells.get((r, c), default)

    def _set_value(self, r: int, c: int, value: Any) -> None:
        self._cells[(r, c)] = value

    def _max_bounds(self) -> Tuple[int, int]:
        if not self._cells:
            return 0, 0
        max_r = max(r for r, _ in self._cells.keys())
        max_c = max(c for _, c in self._cells.keys())
        return max_r, max_c

    def insert_cell(self, r: int, c: int, value: Any) -> bool:
        if self._exists_key(r, c):
            return False
        self._set_value(r, c, value)
        return True

    def update_cell(self, r: int, c: int, value: Any) -> bool:
        if not self._exists_key(r, c):
            return False
        self._set_value(r, c, value)
        return True

    def has_value(self, r: int, c: int) -> bool:
        return self._exists_key(r, c)

    def preview(self, max_rows: int | None = None, max_cols: int | None = None) -> str:
        max_r, max_c = self._max_bounds()
        if max_r == 0 or max_c == 0:
            return "(hoja vacía)"

        to_r = min(max_r, max_rows) if max_rows is not None else max_r
        to_c = min(max_c, max_cols) if max_cols is not None else max_c

        col_widths = [0] * (to_c + 1)
        for c in range(1, to_c + 1):
            col_widths[c] = max(col_widths[c], len(f"[{c:>3}]"))

        for c in range(1, to_c + 1):
            for r in range(1, to_r + 1):
                v = self._get_value(r, c, "")
                s = "" if v is None else str(v)
                col_widths[c] = max(col_widths[c], len(s), 4)

        parts: List[str] = []

        header_cells = ["    "]
        for c in range(1, to_c + 1):
            header_cells.append(f"[{c:>3}]".ljust(col_widths[c] + 1))
        parts.append("".join(header_cells).rstrip())

        for r in range(1, to_r + 1):
            row_out = [f"[{r:>3}] "]
            for c in range(1, to_c + 1):
                v = self._get_value(r, c, "")
                s = "" if v is None else str(v)
                row_out.append(s.ljust(col_widths[c] + 1))
            parts.append("".join(row_out).rstrip())

        return "\n".join(parts)

    def row_values_and_sum(self, r: int) -> Tuple[List[Any], float]:
        max_r, max_c = self._max_bounds()
        if r < 1 or r > max_r:
            return [], 0.0

        values: List[Any] = []
        total = 0.0
        for c in range(1, max_c + 1):
            v = self._get_value(r, c, None)
            values.append(v)
            if isinstance(v, (int, float)):
                total += float(v)
        return values, total

    def col_values_and_sum(self, c: int) -> Tuple[List[Any], float]:
        max_r, max_c = self._max_bounds()
        if c < 1 or c > max_c:
            return [], 0.0

        values: List[Any] = []
        total = 0.0
        for r in range(1, max_r + 1):
            v = self._get_value(r, c, None)
            values.append(v)
            if isinstance(v, (int, float)):
                total += float(v)
        return values, total

def _demo() -> None:
    sheet = Sheet()
    sheet.insert_cell(1, 1, 10)
    sheet.insert_cell(1, 2, 20)
    sheet.insert_cell(2, 1, "hi")
    sheet.insert_cell(3, 3, 7.5)
    sheet.update_cell(1, 2, 25)
    sheet.update_cell(4, 1, "nueva")

    print("=== Preview (todo) ===")
    print(sheet.preview())

    print("\n=== Preview (máx 3x3) ===")
    print(sheet.preview(max_rows=3, max_cols=3))

    vals_row_1, sum_row_1 = sheet.row_values_and_sum(1)
    print("\nFila 1 -> valores:", vals_row_1, "| suma:", sum_row_1)

    vals_col_1, sum_col_1 = sheet.col_values_and_sum(1)
    print("Columna 1 -> valores:", vals_col_1, "| suma:", sum_col_1)

    print("\nhas(1,1):", sheet.has_value(1, 1), " | has(4,4):", sheet.has_value(4, 4))

if __name__ == "__main__":
    _demo()
