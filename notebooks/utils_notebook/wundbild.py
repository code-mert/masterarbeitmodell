import os
import sys
import re
import ipywidgets as widgets
from IPython.display import Image, display

# Ensure parent directory (project root) is in the path to allow loading eval module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from eval.loaders import normalize_image_id

def zeige_wundbild(image_id, base_dir="../data/wundbilder"):
    """
    Lädt und zeigt das Wundbild für eine gegebene Image-ID (z.B. "wunde_02", "Bild2", "2", 2).
    """
    normalized = normalize_image_id(str(image_id))
    if not normalized:
        print(f"Fehler: Ungültige Image-ID '{image_id}'")
        return
        
    # Extrahiere die Nummer aus dem normalisierten Format (z.B. "wunde_02" -> 2)
    match = re.search(r"wunde_(\d+)", normalized)
    if not match:
        print(f"Fehler: Konnte Bildnummer aus '{normalized}' nicht extrahieren.")
        return
        
    num = int(match.group(1))
    file_name = f"Bild{num}.jpg"
    file_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(file_path):
        print(f"Zeige Wundbild {file_name} (ID: {normalized})")
        display(Image(filename=file_path, width=400))
    else:
        print(f"Fehler: Datei {file_path} existiert nicht.")

def zeige_wundbild_interactive(base_dir="../data/wundbilder"):
    """
    Erstellt ein interaktives Widget mit einem Nummern-Eingabefeld, 
    um die Wundbilder dynamisch anzuzeigen.
    """
    def _display_wund(num):
        if num is not None:
            zeige_wundbild(num, base_dir=base_dir)

    wund_input = widgets.BoundedIntText(
        value=1,
        min=1,
        max=50,
        step=1,
        description='Wund-Nummer:',
        style={'description_width': 'initial'},
        disabled=False
    )
    
    display(widgets.interactive(_display_wund, num=wund_input))
