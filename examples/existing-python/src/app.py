"""Minimal existing Python project fixture: no external dependencies."""


def greet(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    return f"Hello, {name.strip()}!"
