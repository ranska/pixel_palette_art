
# lib/color/rgb_exporter.py

class RGBExporter:
    """
    Module d'export pour les couleurs PixelColor
    Formats supportés: hex, rgb, rgba, hsl, css
    """
    
    def __init__(self, color):
        """Initialise l'exporter avec une couleur"""
        self.color = color
    
    def to_hex(self):
        """Export au format hexadécimal #RRGGBB"""
        return f"#{self.color.r:02X}{self.color.g:02X}{self.color.b:02X}"
    
    def to_hex_alpha(self, alpha=255):
        """Export au format hexadécimal avec alpha #RRGGBBAA"""
        return f"#{self.color.r:02X}{self.color.g:02X}{self.color.b:02X}{alpha:02X}"
    
    def to_rgb_string(self):
        """Export au format RGB: rgb(255, 128, 0)"""
        return f"rgb({self.color.r}, {self.color.g}, {self.color.b})"
    
    def to_rgba_string(self, alpha=1.0):
        """Export au format RGBA: rgba(255, 128, 0, 1.0)"""
        return f"rgba({self.color.r}, {self.color.g}, {self.color.b}, {alpha})"
    
    def to_rgb_tuple(self):
        """Export au format tuple RGB: (255, 128, 0)"""
        return (self.color.r, self.color.g, self.color.b)
    
    def to_rgba_tuple(self, alpha=255):
        """Export au format tuple RGBA: (255, 128, 0, 255)"""
        return (self.color.r, self.color.g, self.color.b, alpha)
    
    def to_hsl_string(self):
        """Export au format HSL: hsl(30, 100%, 50%)"""
        r, g, b = self.color.r / 255.0, self.color.g / 255.0, self.color.b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2
        
        if diff == 0:
            h = s = 0  # Achromatic
        else:
            # Saturation
            s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
            
            # Hue
            if max_val == r:
                h = (g - b) / diff + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / diff + 2
            else:
                h = (r - g) / diff + 4
            h /= 6
        
        return f"hsl({int(h * 360)}, {int(s * 100)}%, {int(l * 100)}%)"
    
    def to_css_var(self, var_name):
        """Export au format variable CSS: --color-name: #FF8000;"""
        hex_color = self.to_hex()
        return f"--{var_name}: {hex_color};"
    
    def to_gimp_palette_line(self, index=None):
        """Export au format ligne palette GIMP: 255 128 0 Color Name"""
        name = self.color.name if self.color.name else f"Color_{index}" if index is not None else "Untitled"
        return f"{self.color.r:3d} {self.color.g:3d} {self.color.b:3d}\t{name}"
