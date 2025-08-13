
# nodes/color_preview_node.py
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ..lib.pixel_palette import PixelColor

class ColorPreviewNode:
    """
    Nœud pour créer une image de prévisualisation d'une couleur
    Affiche la couleur avec son code formaté en overlay
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "color": ("PIXEL_COLOR",),
                "width": ("INT", {
                    "default": 256,
                    "min": 64,
                    "max": 1024,
                    "step": 8,
                    "tooltip": "Largeur de l'image"
                }),
                "height": ("INT", {
                    "default": 256,
                    "min": 64,
                    "max": 1024,
                    "step": 8,
                    "tooltip": "Hauteur de l'image"
                }),
            },
            "optional": {
                "show_text": ("BOOLEAN", {"default": True}),
                "text_format": (["hex", "rgb", "hsl", "css"], {"default": "hex"}),
                "text_color": (["black", "white", "auto"], {"default": "auto"}),
                "text_size": ("INT", {
                    "default": 24,
                    "min": 12,
                    "max": 72,
                    "step": 2,
                    "tooltip": "Taille de la police"
                }),
                "text_position": (["center", "bottom", "top"], {"default": "center"}),
                "background_color": ("STRING", {
                    "default": "transparent", 
                    "tooltip": "Couleur de fond (hex, rgb, ou 'transparent')"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "create_color_preview"
    CATEGORY = "pixel_art/output"
    
    def create_color_preview(self, color, width=256, height=256, show_text=True, 
                           text_format="hex", text_color="auto", text_size=24,
                           text_position="center", background_color="transparent"):
        """
        Crée une image de prévisualisation de la couleur
        """
        # Validation
        if not isinstance(color, PixelColor):
            print("[ColorPreview] ✗ Erreur: Objet couleur invalide")
            # Image d'erreur rouge
            error_img = np.full((height, width, 3), [255, 0, 0], dtype=np.uint8)
            return (torch.from_numpy(error_img).float() / 255.0,)
        
        try:
            # Création de l'image PIL
            if background_color.lower() == "transparent":
                img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            else:
                # Parse background color (hex ou rgb)
                bg_color = self._parse_color(background_color)
                img = Image.new('RGB', (width, height), bg_color)
            
            draw = ImageDraw.Draw(img)
            
            # Couleur principale (rectangle de fond)
            main_color = (color.r, color.g, color.b)
            draw.rectangle([(0, 0), (width, height)], fill=main_color)
            
            # Affichage du texte si demandé
            if show_text:
                # Format du texte selon le type demandé
                text = self._get_formatted_text(color, text_format)
                
                # Couleur du texte
                if text_color == "auto":
                    # Auto: noir sur couleur claire, blanc sur couleur sombre
                    luminance = (0.299 * color.r + 0.587 * color.g + 0.114 * color.b) / 255
                    text_rgb = (0, 0, 0) if luminance > 0.5 else (255, 255, 255)
                elif text_color == "white":
                    text_rgb = (255, 255, 255)
                else:  # black
                    text_rgb = (0, 0, 0)
                
                # Police (utilise police par défaut PIL)
                try:
                    font = ImageFont.truetype("arial.ttf", text_size)
                except:
                    font = ImageFont.load_default()
                
                # Position du texte
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                if text_position == "center":
                    x = (width - text_width) // 2
                    y = (height - text_height) // 2
                elif text_position == "top":
                    x = (width - text_width) // 2
                    y = 10
                else:  # bottom
                    x = (width - text_width) // 2
                    y = height - text_height - 10
                
                # Dessiner le texte
                draw.text((x, y), text, fill=text_rgb, font=font)
            
            # Conversion vers format ComfyUI
            if img.mode == 'RGBA':
                # Convertir RGBA vers RGB avec fond blanc
                bg = Image.new('RGB', img.size, (255, 255, 255))
                img = Image.alpha_composite(bg.convert('RGBA'), img).convert('RGB')
            
            # Conversion PIL -> numpy -> torch
            img_array = np.array(img).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img_array)[None,]  # Add batch dimension
            
            # Log de succès
            color_name = color.name if color.name else "Sans nom"
            print(f"[ColorPreview] ✓ Image créée: '{color_name}' "
                  f"({color.r}, {color.g}, {color.b}) -> {width}x{height}")
            
            return (img_tensor,)
            
        except Exception as e:
            print(f"[ColorPreview] ✗ Erreur: {e}")
            # Image d'erreur
            error_img = np.full((height, width, 3), [255, 0, 0], dtype=np.uint8)
            return (torch.from_numpy(error_img).float() / 255.0,)
    
    def _get_formatted_text(self, color, text_format):
        """Récupère le texte formaté selon le type demandé"""
        exporter = color.exporter
        
        if text_format == "hex":
            return exporter.to_hex()
        elif text_format == "rgb":
            return exporter.to_rgb_string()
        elif text_format == "hsl":
            return exporter.to_hsl_string()
        elif text_format == "css":
            var_name = color.name.lower().replace(" ", "-") if color.name else "color"
            return exporter.to_css_var(var_name)
        else:
            return exporter.to_hex()  # fallback
    
    def _parse_color(self, color_str):
        """Parse une couleur depuis une string (hex ou rgb)"""
        color_str = color_str.strip()
        
        if color_str.startswith('#'):
            # Hex color
            hex_clean = color_str[1:]
            if len(hex_clean) == 6:
                return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
        
        # Default: blanc
        return (255, 255, 255)
