# nodes/create_color_from_rgb_node.py
from ..lib.pixel_palette import PixelColor

class CreateColorFromRGBNode:
    """
    Nœud ComfyUI pour créer une couleur depuis des valeurs RGB
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "red": ("INT", {
                    "default": 255,
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Composante rouge (0-255)"
                }),
                "green": ("INT", {
                    "default": 0,
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Composante verte (0-255)"
                }),
                "blue": ("INT", {
                    "default": 0,
                    "min": 0, 
                    "max": 255, 
                    "step": 1,
                    "tooltip": "Composante bleue (0-255)"
                }),
            },
            "optional": {
                "color_name": ("STRING", {
                    "default": "", 
                    "tooltip": "Nom optionnel de la couleur"
                }),
            }
        }
    
    RETURN_TYPES = ("PIXEL_COLOR",)
    RETURN_NAMES = ("color",)
    FUNCTION = "create_color_from_rgb"
    CATEGORY = "pixel_art/colors"
    
    def create_color_from_rgb(self, red, green, blue, color_name=""):
        """
        Crée une couleur depuis des valeurs RGB
        """
        # Créer l'objet couleur
        color = PixelColor(
            r=red, 
            g=green, 
            b=blue,
            name=color_name.strip() if color_name else ""
        )
        
        return (color,)
