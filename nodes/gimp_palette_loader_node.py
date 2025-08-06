# nodes/gimp_palette_loader_node.py
import os
import folder_paths
from ..lib import PixelPalette

class GimpPaletteLoaderNode:
    """
    Node ComfyUI qui charge des fichiers GIMP et retourne des objets PixelPalette
    Responsabilité unique: interface fichier <-> objet
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if f.lower().endswith('.gpl')]
        
        if not files:
            files = ["Aucun fichier .gpl - Utilisez le bouton de chargement"]
        
        return {
            "required": {
                "palette_file": (sorted(files), {
                    "image_upload": True,
                    "accept": "text/plain,.gpl",
                    "tooltip": "Charger un fichier palette GIMP (.gpl)"
                }),
            }
        }
    
    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("palette",)
    FUNCTION = "load_palette"
    CATEGORY = "pixel_art/io"
    
    @classmethod
    def IS_CHANGED(cls, palette_file):
        palette_path = folder_paths.get_annotated_filepath(palette_file)
        if palette_path and os.path.exists(palette_path):
            return os.path.getmtime(palette_path)
        return float("NaN")
    
    @classmethod
    def VALIDATE_INPUTS(cls, palette_file, **kwargs):
        if not palette_file or not palette_file.lower().endswith('.gpl'):
            return "Le fichier doit être une palette GIMP (.gpl)"
        return True
    
    def load_palette(self, palette_file):
        """
        Charge un fichier et retourne un objet PixelPalette
        Gestion d'erreurs avec objets valides
        """
        # Cas d'erreur: retourner une palette vide mais valide
        if not palette_file or "Aucun fichier" in palette_file:
            return (PixelPalette(raw_content="", source_filename=""),)
        
        try:
            palette_path = folder_paths.get_annotated_filepath(palette_file)
            
            if not palette_path or not os.path.exists(palette_path):
                return (PixelPalette(raw_content="", source_filename=palette_file),)
            
            # Lecture avec gestion encodage
            content = self._read_file_with_encoding(palette_path)
            
            if content is None:
                return (PixelPalette(raw_content="", source_filename=palette_file),)
            
            # Créer l'objet palette - il se parse automatiquement
            palette = PixelPalette(raw_content=content, source_filename=palette_file)
            
            return (palette,)
            
        except Exception as e:
            # Même en cas d'erreur, retourner un objet valide
            error_content = f"# Erreur de chargement: {str(e)}"
            return (PixelPalette(raw_content=error_content, source_filename=palette_file),)
    
    def _read_file_with_encoding(self, file_path):
        """Lit un fichier avec plusieurs encodages possibles"""
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        return None
