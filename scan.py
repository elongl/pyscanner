import inspect
from collections.abc import Iterable, Mapping
from typing import Tuple

_PRIMITIVE_TYPES = (int, str, float, bool)
_scanned_ids = set()


def _get_obj_prop_items(obj, only_public_props: bool, scan_path: str):
    items = []
    for prop in dir(obj):
        try:
            val = inspect.getattr_static(obj, prop)
            if only_public_props and prop.startswith('_'):
                continue
            if prop.startswith('__') or callable(val):
                continue
            items.append((prop, val))
        except Exception as err:
            print(f'Unable to scan {scan_path}.{prop}: {err}')
    return items


def scan(
        obj,
        scan_values: Iterable = tuple(),
        scan_types: Tuple = tuple(),
        scan_path: str = 'obj',
        max_depth: int = 5,
        depth: int = 0,
        only_public_props: bool = False,
        is_initial_run: bool = True,
):
    if is_initial_run:
        _scanned_ids.clear()

    if depth == max_depth:
        return

    if id(obj) in _scanned_ids:
        return
    _scanned_ids.add(id(obj))

    if isinstance(obj, _PRIMITIVE_TYPES):
        return
    if isinstance(obj, Mapping):
        for key, val in obj.items():
            if only_public_props and str(key).startswith('_'):
                continue
            scan(val, scan_values, scan_types, f'{scan_path}.{key}', max_depth, depth + 1, only_public_props,
                 is_initial_run=False)
        return
    if isinstance(obj, Iterable):
        for val in obj:
            scan(val, scan_values, scan_types, f'{scan_path}.{val}', max_depth, depth + 1, only_public_props,
                 is_initial_run=False)
        return

    if obj in scan_values:
        print(f'[*] Found value @ {scan_path}')
        _scanned_ids.remove(id(obj))
    if isinstance(obj, scan_types):
        print(f'[*] Found type @ {scan_path}')

    for prop_key, prop_val in _get_obj_prop_items(obj, only_public_props, scan_path):
        try:
            scan(prop_val, scan_values, scan_types, f'{scan_path}.{prop_key}', max_depth, depth + 1, only_public_props,
                 is_initial_run=False)
        except Exception as err:
            print(f'Unable to scan {scan_path}.{prop_key}: {err}')
