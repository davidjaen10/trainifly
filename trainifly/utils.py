import os
from pathlib import Path

def get_secret(name):
    # Intenta leer desde Docker secrets
    path = f"/run/secrets/{name}"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    
    # Intenta leer desde archivo local (desarrollo)
    base_dir = Path(__file__).resolve().parent.parent
    local_path = base_dir / "secrets" / f"{name}.txt"
    if local_path.exists():
        with open(local_path) as f:
            content = f.read().strip()
            # Elimina comillas si existen
            if content.startswith("'") and content.endswith("'"):
                content = content[1:-1]
            return content
    
    return os.environ.get(name)