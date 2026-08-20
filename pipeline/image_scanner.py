from pathlib import Path

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def scan_images(input_folder: str):
    """Return supported images recursively, in deterministic order."""
    root = Path(input_folder)
    if not root.exists():
        raise FileNotFoundError(f'Input folder does not exist: {root}')

    return sorted(
        path for path in root.rglob('*')
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
