import re
from pathlib import Path

NOISE_WORDS = {
    'profile', 'photo', 'picture', 'pic', 'image', 'img',
    'copy', 'final', 'new', 'edited'
}


def clean_filename(filename: str) -> str:
    name = Path(filename).stem
    # Handles names such as Person.jpg_01.jpg.
    name = re.sub(r'\.(jpg|jpeg|png|webp)$', '', name, flags=re.I)
    name = re.sub(r'[_\-\s]+(?:v?\d+)$', '', name, flags=re.I)
    name = re.sub(r'[_\-]+', ' ', name)
    tokens = [token for token in name.split() if token.lower() not in NOISE_WORDS]
    return re.sub(r'\s+', ' ', ' '.join(tokens)).strip()
