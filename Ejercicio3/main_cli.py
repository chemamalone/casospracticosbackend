from typing import Any, Dict, Tuple, List

class Sheet:
    def __init__(self) -> None:
        self._cells: Dict[Tuple[int, int], Any] = {}

    def _exists_key(self, r: int, c: int) -> bool:
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
        try:
            return self._cells[(r, c)]
        except KeyError:
            return default

    def _set_value(self, r: int, c: int, value: Any) -> None:
        self._cells[(r, c)] = value

    def _max_bounds(self) -> Tuple[int, int]:
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

    def preview(self) -> str:
        max_r, max_c = self._max_bounds()
        if max_r == 0 or max_c == 0:
            return "(hoja vacía)"

        parts: List[str] = []
        header = ["   "]
        col = 1
        while col <= max_c:
            header.append(f"[{col:>3}]")
            col += 1
        parts.append(" ".join(header))

        r = 1
        while r <= max_r:
            row_parts = [f"[{r:>3}]"]
            c = 1
            while c <= max_c:
                v = self._get_value(r, c, "")
                row_parts.append(f"{str(v):>4}")
                c += 1
            parts.append(" ".join(row_parts))
            r += 1

        return "\n".join(parts)

    def row_values_and_sum(self, r: int) -> Tuple[List[Any], float]:
        max_r, max_c = self._max_bounds()
        if r < 1 or r > max_r:
            return [], 0.0

        values: List[Any] = []
        total = 0.0
        c = 1
        while c <= max_c:
            v = self._get_value(r, c, None)
            values.append(v)
            if isinstance(v, (int, float)):
                total += float(v)
            c += 1
        return values, total

    def col_values_and_sum(self, c: int) -> Tuple[List[Any], float]:
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

def _demo() -> None:
    sheet = Sheet()

    sheet.insert_cell(1, 1, 10)
    sheet.insert_cell(1, 2, 20)
    sheet.insert_cell(2, 1, "hi")
    sheet.insert_cell(3, 3, 7.5)

    sheet.update_cell(1, 2, 25) 
    sheet.update_cell(4, 1, "nueva")

    has_1_1 = sheet.has_value(1, 1) 
    has_4_4 = sheet.has_value(4, 4) 

    print("=== Preview ===")
    print(sheet.preview())

    vals_row_1, sum_row_1 = sheet.row_values_and_sum(1)
    print("\nFila 1 -> valores:", vals_row_1, "| suma:", sum_row_1)

    vals_col_1, sum_col_1 = sheet.col_values_and_sum(1)
    print("Columna 1 -> valores:", vals_col_1, "| suma:", sum_col_1)

    print("\nhas(1,1):", has_1_1, " | has(4,4):", has_4_4)


if __name__ == "__main__":
    _demo()
