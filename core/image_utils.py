import base64
from pathlib import Path

def encode_image(image_path: str) -> str:
    """Bild als Base64-String kodieren."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_media_type(image_path: str) -> str:
    """MIME-Type aus Dateiendung ableiten."""
    suffix = Path(image_path).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(suffix, "image/jpeg")
