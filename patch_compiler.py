#!/usr/bin/env python3
"""Patch ocsf-schema-compiler to warn (not crash) when datetime profile is missing.

The v2.0 schema removed the datetime profile but still uses datetime_t type.
The upstream compiler requires the profile and throws SchemaException.
This patch changes the raise to a logger.warning().

Usage: /tmp/ocsf-venv/bin/python3.14 patch_compiler.py
"""
import importlib
import pathlib

mod = importlib.import_module("ocsf_schema_compiler.compiler")
path = pathlib.Path(mod.__file__)
src = path.read_text()

old = """        elif got_datetime_t:
            raise SchemaException(
                'Schema defines "datetime_t" dictionary type but does not define'
                ' "datetime" profile'
            )"""

new = """        elif got_datetime_t:
            logger.warning(
                'Schema defines "datetime_t" dictionary type but does not define'
                ' "datetime" profile. Datetime siblings will not be added.'
            )"""

if old not in src:
    if new in src:
        print("Already patched.")
    else:
        print("ERROR: Could not find the expected code to patch. Compiler version may have changed.")
        raise SystemExit(1)
else:
    path.write_text(src.replace(old, new))
    print(f"Patched: {path}")
