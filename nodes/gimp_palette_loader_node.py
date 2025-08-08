# nodes/gimp_palette_loader_node.py
import os
import folder_paths
from ..lib.pixel_palette import PixelPalette

class GimpPaletteLoaderNode:
    """
    Nœud ComfyUI pour charger des palettes GIMP
    Responsabilité unique: interface fichier <-> objet PixelPalette
    Toute la logique métier est dans PixelPalette
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Configuration des entrées du nœud"""
        input_dir = folder_paths.get_input_directory()
        
        try:
            files = [f for f in os.listdir(input_dir) 
                    if f.lower().endswith(('.gpl', '.pal', '.aco')) 
                    and os.path.isfile(os.path.join(input_dir, f))]
        except (OSError, FileNotFoundError):
            files = []
        
        if not files:
            files = ["Aucun fichier palette - Utilisez le bouton de chargement"]
        
        return {
            "required": {
                "palette_file": (sorted(files), {
                    "image_upload": True,
                    "accept": "text/plain,.gpl,.pal,.aco",
                    "tooltip": "Charger un fichier palette (.gpl, .pal, .aco)"
                }),
            }
        }
    
    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("palette",)
    FUNCTION = "load_palette"
    CATEGORY = "pixel_art/io"
    
    @classmethod
    def IS_CHANGED(cls, palette_file):
        """Détection des changements pour le cache ComfyUI"""
        try:
            palette_path = folder_paths.get_annotated_filepath(palette_file)
            if palette_path and os.path.exists(palette_path):
                return os.path.getmtime(palette_path)
        except (OSError, TypeError):
            pass
        return float("NaN")
    
    @classmethod
    def VALIDATE_INPUTS(cls, palette_file, **kwargs):
        """Validation des entrées"""
        if not palette_file or not isinstance(palette_file, str):
            return "Le fichier palette est requis"
        
        if "Aucun fichier" in palette_file:
            return True  # Cas spécial autorisé
        
        supported_extensions = ('.gpl', '.pal', '.aco')
        if not any(palette_file.lower().endswith(ext) for ext in supported_extensions):
            return f"Format non supporté. Extensions autorisées: {', '.join(supported_extensions)}"
        
        return True
    
    def load_palette(self, palette_file):
        """
        Charge un fichier palette et retourne un objet PixelPalette
        Interface simple: lecture fichier -> création objet
        """
        # Cas d'erreur ou absence de fichier
        if not palette_file or "Aucun fichier" in palette_file:
            print("[GimpPaletteLoader] Aucun fichier sélectionné")
            return (PixelPalette(raw_content="", source_filename=""),)
        
        try:
            # Résolution du chemin du fichier
            palette_path = folder_paths.get_annotated_filepath(palette_file)
            
            if not palette_path or not os.path.exists(palette_path):
                print(f"[GimpPaletteLoader] Fichier introuvable: {palette_file}")
                return (PixelPalette(raw_content="", source_filename=palette_file),)
            
            # Lecture du contenu
            content = self._read_file_safe(palette_path)
            
            if content is None:
                print(f"[GimpPaletteLoader] Impossible de lire le fichier: {palette_file}")
                return (PixelPalette(raw_content="", source_filename=palette_file),)
            
            # Création de l'objet palette (parse automatique)
            palette = PixelPalette(raw_content=content, source_filename=palette_file)
            
            # Log de succès
            print(f"[GimpPaletteLoader] ✓ Palette chargée: '{palette.name}' "
                  f"({palette.color_count} couleurs, format: {palette.format_type})")
            
            return (palette,)
            
        except Exception as e:
            # En cas d'erreur, toujours retourner un objet valide
            print(f"[GimpPaletteLoader] ✗ Erreur: {e}")
            error_palette = PixelPalette(
                raw_content=f"# Erreur de chargement: {str(e)}", 
                source_filename=palette_file
            )
            return (error_palette,)
    
    def _read_file_safe(self, file_path: str) -> str:
        """
        Lecture sécurisée avec gestion des encodages
        Déléguée à une méthode simple car la logique métier est dans PixelPalette
        """
        # Liste d'encodages à tenter, du plus strict au plus permissif
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    if content.strip():  # Pas complètement vide
                        return content
            except (UnicodeDecodeError, UnicodeError):
                continue
            except OSError as e:
                print(f"[GimpPaletteLoader] Erreur I/O avec {encoding}: {e}")
                continue
        
        # Dernier recours: lecture binaire + décodage forcé
        try:
            with open(file_path, 'rb') as f:
                raw_bytes = f.read()
                return raw_bytes.decode('latin-1', errors='replace')
        except Exception as e:
            print(f"[GimpPaletteLoader] Échec lecture binaire: {e}")
        
        return None
