import os
import re
import folder_paths

class GimpPaletteLoader:
    """
    Un node ComfyUI qui charge une palette GIMP (.gpl) via bouton d'upload uniquement
    et retourne son contenu sous forme de string
    """
    
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if f.lower().endswith('.gpl')]
        # Ajouter une option vide pour forcer l'affichage du bouton même sans fichiers
        if not files:
            files = ["Aucun fichier .gpl - Cliquez sur le bouton de chargement"]
        return {
            "required": {
                "palette": (sorted(files), {
                    "image_upload": True,
                    "accept": "text/plain,.gpl",
                    "tooltip": "Charger un fichier palette GIMP (.gpl)"
                }),
            },
            "optional": {
                "output_format": (["colors_only", "full_content", "hex_colors"], {"default": "colors_only"}),
                "separator": ("STRING", {"default": "\n", "multiline": False})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("palette_data",)
    FUNCTION = "load_gimp_palette"
    CATEGORY = "image/color"
    
    @classmethod
    def IS_CHANGED(s, palette, output_format, separator):
        """Vérifier si le fichier a changé pour forcer la re-évaluation"""
        palette_path = folder_paths.get_annotated_filepath(palette)
        if palette_path and os.path.exists(palette_path):
            return os.path.getmtime(palette_path)
        return float("NaN")
    
    @classmethod
    def VALIDATE_INPUTS(s, palette, **kwargs):
        """Valider que le fichier existe et est un .gpl"""
        if not palette:
            return "Aucun fichier sélectionné"
        
        if not palette.lower().endswith('.gpl'):
            return "Le fichier doit être une palette GIMP (.gpl)"
            
        return True
    
    def load_gimp_palette(self, palette, output_format="colors_only", separator="\n"):
        """
        Charge une palette GIMP et retourne les données formatées
        """
        
        try:
            if not palette or palette == "Aucun fichier .gpl - Cliquez sur le bouton de chargement":
                return ("Erreur: Aucun fichier sélectionné. Utilisez le bouton de chargement pour uploader un fichier .gpl",)
            
            # Obtenir le chemin complet du fichier uploadé
            palette_path = folder_paths.get_annotated_filepath(palette)
            
            if not palette_path or not os.path.exists(palette_path):
                return ("Erreur: Fichier non trouvé",)
            
            # Lire le contenu du fichier avec gestion d'encodage
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(palette_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return ("Erreur: Impossible de lire le fichier (problème d'encodage)",)
            
            # Parser le contenu selon le format demandé
            if output_format == "full_content":
                return (content,)
            
            # Extraire les couleurs
            colors, palette_info = self.parse_gimp_palette(content)
            
            if not colors:
                return ("Erreur: Aucune couleur trouvée dans le fichier",)
            
            if output_format == "hex_colors":
                # Convertir en format hexadécimal
                hex_colors = []
                for r, g, b, name in colors:
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    if name:
                        hex_colors.append(f"{hex_color} ({name})")
                    else:
                        hex_colors.append(hex_color)
                result = separator.join(hex_colors)
            
            else:  # colors_only
                # Format RGB avec noms optionnels
                rgb_colors = []
                for r, g, b, name in colors:
                    if name:
                        rgb_colors.append(f"RGB({r},{g},{b}) - {name}")
                    else:
                        rgb_colors.append(f"RGB({r},{g},{b})")
                result = separator.join(rgb_colors)
            
            # Ajouter les infos de la palette si disponibles
            if palette_info and output_format != "full_content":
                header = f"# Palette: {palette_info.get('name', 'Sans nom')}"
                if 'columns' in palette_info:
                    header += f" | Colonnes: {palette_info['columns']}"
                header += f" | Couleurs: {len(colors)}"
                result = header + separator + result
            
            return (result,)
            
        except Exception as e:
            return (f"Erreur lors du chargement: {str(e)}",)
    
    def parse_gimp_palette(self, content):
        """
        Parse le contenu d'un fichier palette GIMP
        
        Format GIMP palette (.gpl):
        GIMP Palette
        Name: Nom de la palette
        Columns: X
        #
        R G B    Nom de la couleur (optionnel)
        
        Returns:
            tuple: (colors_list, palette_info_dict)
        """
        
        colors = []
        palette_info = {}
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Ignorer les lignes vides
            if not line:
                continue
            
            # Ignorer les commentaires (mais pas l'en-tête)
            if line.startswith('#') and not line.startswith('GIMP'):
                continue
            
            # Parser l'en-tête GIMP
            if line.startswith('GIMP Palette'):
                continue
            elif line.startswith('Name:'):
                palette_info['name'] = line[5:].strip()
                continue
            elif line.startswith('Columns:'):
                try:
                    palette_info['columns'] = int(line[8:].strip())
                except ValueError:
                    pass
                continue
            
            # Essayer de parser une ligne de couleur
            # Format: "R G B Nom" ou "R G B" (nom optionnel)
            # Supporter aussi les variations avec tabulations
            color_match = re.match(r'^\s*(\d+)\s+(\d+)\s+(\d+)(?:\s+(.*))?', line)
            
            if color_match:
                try:
                    r = int(color_match.group(1))
                    g = int(color_match.group(2))
                    b = int(color_match.group(3))
                    name = color_match.group(4) if color_match.group(4) else ""
                    
                    # Vérifier que les valeurs RGB sont valides (0-255)
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        colors.append((r, g, b, name.strip()))
                except ValueError:
                    # Ignorer les lignes avec des valeurs non numériques
                    continue
        
        return colors, palette_info

# Mappage du node
GIMP_NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader": GimpPaletteLoader
}

GIMP_NODE_DISPLAY_NAME_MAPPINGS = {
    "GimpPaletteLoader": "GIMP Palette Loader"
}
