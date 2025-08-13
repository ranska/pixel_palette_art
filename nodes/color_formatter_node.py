# nodes/color_formatter_node.py
from ..lib.pixel_palette import PixelColor

class ColorFormatterNode:
    """
    Nœud dédié au formatage des couleurs individuelles
    Responsabilité unique: interface de formatage pour ComfyUI
    Utilise l'exporter intégré à PixelColor
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "color": ("PIXEL_COLOR",),
                "format_type": (["hex", "hex_alpha", "rgb", "rgba", "tuple", "tuple_alpha", "hsl", "css", "gimp"], 
                               {"default": "hex"}),
            },
            "optional": {
                "alpha_value": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.01,
                    "tooltip": "Valeur alpha pour les formats supportés"
                }),
                "alpha_int": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Valeur alpha entière (0-255)"
                }),
                "css_var_name": ("STRING", {
                    "default": "color", 
                    "tooltip": "Nom de la variable CSS (sans --)"
                }),
                "gimp_index": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 999,
                    "step": 1,
                    "tooltip": "Index pour format GIMP (-1 = auto)"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_color",)
    FUNCTION = "format_color"
    CATEGORY = "pixel_art/output"
    
    def format_color(self, color, format_type="hex", alpha_value=1.0, alpha_int=255, 
                    css_var_name="color", gimp_index=-1):
        """
        Formate une couleur selon le type demandé
        Interface simple vers l'exporter de PixelColor
        """
        # Validation de l'entrée
        if not isinstance(color, PixelColor):
            print("[ColorFormatter] ✗ Erreur: Objet couleur invalide")
            return ("# Erreur: Objet couleur invalide",)
        
        try:
            # Accès à l'exporter de la couleur
            exporter = color.exporter
            
            # Formatage selon le type demandé
            if format_type == "hex":
                result = exporter.to_hex()
            
            elif format_type == "hex_alpha":
                result = exporter.to_hex_alpha(alpha_int)
            
            elif format_type == "rgb":
                result = exporter.to_rgb_string()
            
            elif format_type == "rgba":
                result = exporter.to_rgba_string(alpha_value)
            
            elif format_type == "tuple":
                result = str(exporter.to_rgb_tuple())
            
            elif format_type == "tuple_alpha":
                result = str(exporter.to_rgba_tuple(alpha_int))
            
            elif format_type == "hsl":
                result = exporter.to_hsl_string()
            
            elif format_type == "css":
                result = exporter.to_css_var(css_var_name)
            
            elif format_type == "gimp":
                index = gimp_index if gimp_index >= 0 else None
                result = exporter.to_gimp_palette_line(index)
            
            else:
                raise ValueError(f"Format non supporté: {format_type}")
            
            # Log de succès
            color_name = color.name if color.name else "Sans nom"
            print(f"[ColorFormatter] ✓ Couleur formatée: '{color_name}' "
                  f"({color.r}, {color.g}, {color.b}) -> {format_type}: {result}")
            
            return (result,)
            
        except Exception as e:
            # Gestion d'erreur avec sortie valide
            error_msg = f"# Erreur de formatage couleur: {str(e)}"
            print(f"[ColorFormatter] ✗ Erreur: {e}")
            return (error_msg,)
