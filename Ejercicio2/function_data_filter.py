#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para Ejercicio 2:
- Filtros dinámicos (N filtros) con operadores: <, <=, >, >=, ==, !=
- Orden estable por 'priority' con MergeSort manual
Restricciones: stdlib, sin sort/sorted, sin 'in', 'find', 'index', etc.
"""

def _get_value(dct, key, default=None):
    """Obtiene dct[key] sin usar 'in'."""
    keys = list(dct.keys())
    i = 0
    n = len(keys)
    while i < n:
        k = keys[i]
        if k == key:
            return dct[k]
        i += 1
    return default


def _compare(a, b, asc):
    """Devuelve -1/0/1 comparando a vs b; invierte si asc=False."""
    res = 0
    if a < b:
        res = -1
    elif a > b:
        res = 1
    if not asc:
        res = -res
    return res


def _merge(left, right, asc):
    """Merge estable por 'priority'."""
    i = 0
    j = 0
    out = []
    ln = len(left)
    rn = len(right)

    while i < ln and j < rn:
        lp = _get_value(left[i], "priority", 0)
        rp = _get_value(right[j], "priority", 0)
        cmpv = _compare(lp, rp, asc)
        if cmpv <= 0:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    while i < ln:
        out.append(left[i]); i += 1
    while j < rn:
        out.append(right[j]); j += 1
    return out


def mergesort_by_priority(items, asc=True):
    """Ordena estable por 'priority' (sin sort/sorted)."""
    n = len(items)
    if n <= 1:
        return items[:]
    mid = n // 2

    left = []
    i = 0
    while i < mid:
        left.append(items[i]); i += 1

    right = []
    while i < n:
        right.append(items[i]); i += 1

    left_s = mergesort_by_priority(left, asc)
    right_s = mergesort_by_priority(right, asc)
    return _merge(left_s, right_s, asc)


def _passes_single_filter(item, triplet):
    """Evalúa (campo, operador, valor)."""
    field = triplet[0]
    op = triplet[1]
    val = triplet[2]

    v = _get_value(item, field, None)
    if v is None:
        return False

    if op == "<":
        return v < val
    if op == "<=":
        return v <= val
    if op == ">":
        return v > val
    if op == ">=":
        return v >= val
    if op == "==":
        return v == val
    if op == "!=":
        return v != val
    return False


def split_by_filters(items, filters_triplets):
    """Devuelve (matched, rest) preservando orden original en rest."""
    matched = []
    rest = []

    i = 0
    n = len(items)
    while i < n:
        it = items[i]
        all_ok = True
        j = 0
        m = len(filters_triplets)
        while j < m:
            if not _passes_single_filter(it, filters_triplets[j]):
                all_ok = False
                j = m  # corto-circuito
            else:
                j += 1
        if all_ok:
            matched.append(it)
        else:
            rest.append(it)
        i += 1
    return matched, rest


def solve(items, filters_triplets, order_str):
    """
    Regresa:
      primero -> items que cumplen filtros ordenados por 'priority'
      después -> los demás en su orden original
    """
    o = str(order_str).upper()
    asc = True
    if o == "DESC":
        asc = False

    matched, rest = split_by_filters(items, filters_triplets)
    matched_sorted = mergesort_by_priority(matched, asc)

    out = []
    i = 0
    lm = len(matched_sorted)
    while i < lm:
        out.append(matched_sorted[i]); i += 1
    j = 0
    lr = len(rest)
    while j < lr:
        out.append(rest[j]); j += 1
    return out
