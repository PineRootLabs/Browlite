import os
from pathlib import Path

def get_style(theme='dark'):
    """Carrega o arquivo CSS do tema selecionado"""
    styles_dir = Path(__file__).parent
    style_file = styles_dir / f"{theme}.css"
    
    if not style_file.exists():
        return ""
    
    with open(style_file, 'r') as f:
        return f.read()