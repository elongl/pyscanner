import sys
from collections.abc import Iterable, Mapping
from typing import Any, List, Tuple


PRIMITIVE_TYPES = (int, str, float, bool)
scanned_ids = set()


def get_obj_prop_items(obj):
    items = []
    for prop in dir(obj):
        val = getattr(obj, prop)
        if prop.startswith('__') or callable(val):
            continue
        items.append((prop, val))
    return items


def scan(obj, values: Iterable, types: Tuple, path: str = ''):
    if id(obj) in scanned_ids:
        return
    scanned_ids.add(id(obj))
    if isinstance(obj, PRIMITIVE_TYPES):
        return
    if isinstance(obj, Mapping):
        for key, val in obj.items():
            scan(val, values, types, f'{path}/{key}')
        return
    if isinstance(obj, Iterable):
        for val in obj:
            scan(val, values, types, f'{path}/{obj}')
        return

    if obj in values:
        print(f'Found value: {obj} @ {path}')
    if isinstance(obj, types):
        print(f'Found type: {obj} @ {path}')

    for prop_key, prop_val in get_obj_prop_items(obj):
        scan(prop_val, values, types, f'{path}/{prop_key}')

