import os

def resource_path(relative_path):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def load_favorites(favs_file):
    if not os.path.exists(favs_file):
        return []
    with open(favs_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_favorites(favs_file, favorites):
    with open(favs_file, 'w') as f:
        f.write('\n'.join(favorites))