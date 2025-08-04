import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

class PixelPaletteExtractor:
    """
    Un node ComfyUI qui extrait la palette de couleurs d'une image GIF indexée
    et génère une image de palette avec option d'affichage des index.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "palette_width": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 32,
                    "step": 1,
                    "display": "number"
                }),
                "color_size": ("INT", {
                    "default": 32,
                    "min": 8,
                    "max": 128,
                    "step": 4,
                    "display": "number"
                }),
                "show_indices": ("BOOLEAN", {"default": False}),
                "font_size": ("INT", {
                    "default": 10,
                    "min": 6,
                    "max": 24,
                    "step": 1,
                    "display": "number"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("palette_image",)
    FUNCTION = "extract_palette"
    CATEGORY = "image/color"
    
    def extract_palette(self, image, palette_width, color_size, show_indices, font_size):
        """
        Extrait la palette de couleurs de l'image et génère une image de palette
        
        Args:
            image: Tensor d'image ComfyUI (batch, height, width, channels)
            palette_width: Nombre de couleurs par ligne dans la palette
            color_size: Taille de chaque carré de couleur en pixels
            show_indices: Afficher les index des couleurs
            font_size: Taille de la police pour les index
        """
        
        try:
            # Convertir le tensor ComfyUI en PIL Image
            # ComfyUI utilise le format [batch, height, width, channels] avec valeurs 0-1
            if len(image.shape) == 4:
                img_tensor = image[0]  # Prendre la première image du batch
            else:
                img_tensor = image
                
            # Convertir de [0,1] à [0,255]
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            
            # Créer l'image PIL en RGB
            if len(img_np.shape) == 3 and img_np.shape[2] == 3:
                img_pil = Image.fromarray(img_np, 'RGB')
            elif len(img_np.shape) == 3 and img_np.shape[2] == 4:
                img_pil = Image.fromarray(img_np, 'RGBA').convert('RGB')
            else:
                # Fallback pour les images en niveaux de gris
                if len(img_np.shape) == 2:
                    img_pil = Image.fromarray(img_np, 'L').convert('RGB')
                else:
                    img_pil = Image.fromarray(img_np[:,:,0], 'L').convert('RGB')
            
            # Extraire les couleurs uniques
            colors = self.extract_unique_colors(img_pil)
            
            # Créer l'image de palette
            palette_img = self.create_palette_image(colors, palette_width, color_size, show_indices, font_size)
            
            # Convertir l'image PIL en tensor ComfyUI
            palette_array = np.array(palette_img).astype(np.float32) / 255.0
            
            # S'assurer que le tensor a la bonne forme [batch, height, width, channels]
            if len(palette_array.shape) == 3:
                palette_tensor = torch.from_numpy(palette_array).unsqueeze(0)
            else:
                palette_tensor = torch.from_numpy(palette_array)
            
            return (palette_tensor,)
            
        except Exception as e:
            print(f"Erreur dans PixelPaletteExtractor: {e}")
            # Retourner une image d'erreur
            error_img = Image.new('RGB', (color_size, color_size), (255, 0, 0))
            error_array = np.array(error_img).astype(np.float32) / 255.0
            error_tensor = torch.from_numpy(error_array).unsqueeze(0)
            return (error_tensor,)
    
    def extract_unique_colors(self, img_pil):
        """Extrait les couleurs uniques de l'image"""
        colors = []
        
        try:
            # Méthode 1: Essayer de convertir en palette indexée
            img_palette = img_pil.convert('P', palette=Image.ADAPTIVE, colors=256)
            palette_data = img_palette.getpalette()
            
            if palette_data is not None:
                # Extraire les couleurs uniques utilisées
                img_array = np.array(img_palette)
                unique_indices = np.unique(img_array)
                
                for idx in unique_indices:
                    if idx * 3 + 2 < len(palette_data):
                        r = palette_data[idx * 3]
                        g = palette_data[idx * 3 + 1]
                        b = palette_data[idx * 3 + 2]
                        colors.append((r, g, b, idx))
            else:
                raise Exception("Pas de palette trouvée")
                
        except:
            # Méthode 2: Quantifier l'image directement
            try:
                img_quantized = img_pil.quantize(colors=256)
                palette_data = img_quantized.getpalette()
                
                if palette_data is not None:
                    img_array = np.array(img_quantized)
                    unique_indices = np.unique(img_array)
                    
                    for idx in unique_indices:
                        if idx * 3 + 2 < len(palette_data):
                            r = palette_data[idx * 3]
                            g = palette_data[idx * 3 + 1]
                            b = palette_data[idx * 3 + 2]
                            colors.append((r, g, b, idx))
                else:
                    raise Exception("Quantification échouée")
                    
            except:
                # Méthode 3: Extraire les couleurs directement (fallback)
                img_array = np.array(img_pil)
                # Reshaper et obtenir les couleurs uniques
                pixels = img_array.reshape(-1, 3)
                unique_colors = np.unique(pixels, axis=0)
                
                for i, color in enumerate(unique_colors):
                    colors.append((int(color[0]), int(color[1]), int(color[2]), i))
        
        return colors
    
    def create_palette_image(self, colors, palette_width, color_size, show_indices, font_size):
        """Crée l'image de palette"""
        num_colors = len(colors)
        
        if num_colors == 0:
            # Image vide, retourner une image noire
            return Image.new('RGB', (color_size, color_size), (0, 0, 0))
        
        palette_height = (num_colors + palette_width - 1) // palette_width
        
        # Taille de l'image finale
        img_width = palette_width * color_size
        img_height = palette_height * color_size
        
        # Créer l'image de palette
        palette_img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
        draw = ImageDraw.Draw(palette_img)
        
        # Charger une police si possible
        font = None
        if show_indices:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Dessiner chaque couleur
        for i, (r, g, b, idx) in enumerate(colors):
            row = i // palette_width
            col = i % palette_width
            
            x1 = col * color_size
            y1 = row * color_size
            x2 = x1 + color_size
            y2 = y1 + color_size
            
            # Dessiner le carré de couleur
            draw.rectangle([x1, y1, x2-1, y2-1], fill=(r, g, b))
            
            # Ajouter l'index si demandé
            if show_indices and font is not None:
                text = str(idx)
                
                # Position du texte (centré approximativement)
                text_x = x1 + 4
                text_y = y1 + 4
                
                # Fond blanc pour le texte
                try:
                    bbox = draw.textbbox((text_x, text_y), text, font=font)
                    draw.rectangle([bbox[0]-1, bbox[1]-1, bbox[2]+1, bbox[3]+1], 
                                 fill=(255, 255, 255))
                except:
                    # Fallback si textbbox n'est pas disponible
                    draw.rectangle([text_x-1, text_y-1, text_x+20, text_y+12], 
                                 fill=(255, 255, 255))
                
                # Dessiner le texte en noir
                draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
        
        return palette_img

# Mappage des nodes pour ComfyUI
NODE_CLASS_MAPPINGS = {
    "PixelPaletteExtractor": PixelPaletteExtractor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PixelPaletteExtractor": "Pixel Palette Extractor"
}
