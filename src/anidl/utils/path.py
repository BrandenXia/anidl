from pathlib import Path


def directory_completion(value: str) -> list[Path]:
    p = original = Path(value)
    try:
        full_path = p.expanduser()
    except RuntimeError:
        return []
    if not full_path.exists():
        p = p.parent
        full_path = p.expanduser()

    if not full_path.is_dir():
        return []

    return [
        p / dname
        for d in full_path.iterdir()
        if (dname := d.name)
        if d.is_dir() and (dname.startswith(original.name) or p == original)
    ]
