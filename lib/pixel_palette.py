
# lib/pixel_palette.py
import re
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from .pixel_color import PixelColor

@dataclass
class PixelPalette:
    """
    Classe métier pour gérer les palettes de couleurs
    Supporte les formats GIMP (.gpl), Adobe (.aco), etc.
    """
    
    def __init__(self, raw_content: str = "", source_filename: str = ""):
        self.raw_content = raw_content
        self.source_filename = source_filename
        self.colors: List[PixelColor] = []
        self.metadata: Dict[str, Any] = {}
        self.format_type = "unknown"
        
        # Parse automatiquement si du contenu est fourni
        if raw_content.strip():
            self._parse_content()
    
    def _parse_content(self):
        """Parse le contenu selon le format détecté"""
        if not self.raw_content.strip():
            return
        
        # Détection du format
        if self._is_gimp_format():
            self.format_type = "gimp"
            self._parse_gimp_palette()
        elif self._is_adobe_aco_format():
            self.format_type = "adobe_aco"
            self._parse_adobe_aco()
        else:
            # Format générique ou inconnu
            self.format_type = "generic"
            self._parse_generic_format()
    
    def _is_gimp_format(self) -> bool:
        """Détecte si c'est une palette GIMP"""
        lines = self.raw_content.strip().split('\n')
        return len(lines) > 0 and lines[0].strip().startswith('GIMP Palette')
    
    def _is_adobe_aco_format(self) -> bool:
        """Détecte si c'est une palette Adobe (binaire)"""
        return self.raw_content.startswith(b'\x00\x01') if isinstance(self.raw_content, bytes) else False
    
    def _parse_gimp_palette(self):
        """Parse une palette GIMP (.gpl)"""
        lines = self.raw_content.strip().split('\n')
        
        if not lines:
            return
        
        # Header
        header = lines[0].strip()
        if not header.startswith('GIMP Palette'):
            return
        
        # Métadonnées
        self.metadata['format'] = 'GIMP Palette'
        
        for i, line in enumerate(lines[1:], 1):
            line = line.strip()
            
            # Ignorer les lignes vides et commentaires
            if not line or line.startswith('#'):
                continue
            
            # Métadonnées de la palette
            if line.startswith('Name:'):
                self.metadata['name'] = line[5:].strip()
                continue
            elif line.startswith('Columns:'):
                try:
                    self.metadata['columns'] = int(line[8:].strip())
                except ValueError:
                    pass
                continue
            
            # Parse des couleurs
            color = self._parse_color_line(line)
            if color:
                self.colors.append(color)
    
    def _parse_generic_format(self):
        """Parse un format générique (hex, rgb, etc.)"""
        lines = self.raw_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            color = self._parse_color_line(line)
            if color:
                self.colors.append(color)
    
    def _parse_color_line(self, line: str) -> Optional[PixelColor]:
        """Parse une ligne de couleur dans différents formats"""
        line = line.strip()
        
        # Format GIMP: "R G B Name"
        gimp_match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)(?:\s+(.+))?$', line)
        if gimp_match:
            r, g, b = map(int, gimp_match.groups()[:3])
            name = gimp_match.group(4) or ""
            return PixelColor(r, g, b, name.strip())
        
        # Format hexadécimal: "#RRGGBB" ou "RRGGBB"
        hex_match = re.match(r'^#?([0-9a-fA-F]{6})(?:\s+(.+))?$', line)
        if hex_match:
            hex_color = hex_match.group(1)
            name = hex_match.group(2) or ""
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16) 
            b = int(hex_color[4:6], 16)
            return PixelColor(r, g, b, name.strip())
        
        # Format RGB: "rgb(r,g,b)" ou "r,g,b"
        rgb_match = re.match(r'^(?:rgb\()?(\d+)[,\s]+(\d+)[,\s]+(\d+)\)?(?:\s+(.+))?$', line)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups()[:3])
            name = rgb_match.group(4) or ""
            return PixelColor(r, g, b, name.strip())
        
        return None
    
    def _parse_adobe_aco(self):
        """Parse une palette Adobe ACO (binaire) - implémentation basique"""
        # Cette méthode nécessiterait une implémentation binaire plus complexe
        # Pour l'instant, on marque juste le format
        self.metadata['format'] = 'Adobe ACO'
        pass
    
    # === Méthodes utilitaires ===
    
    def add_color(self, r: int, g: int, b: int, name: str = "") -> None:
        """Ajoute une couleur à la palette"""
        self.colors.append(PixelColor(r, g, b, name))
    
    def remove_color(self, index: int) -> bool:
        """Supprime une couleur par index"""
        if 0 <= index < len(self.colors):
            del self.colors[index]
            return True
        return False
    
    def find_closest_color(self, target_color: PixelColor) -> Tuple[PixelColor, int]:
        """Trouve la couleur la plus proche dans la palette"""
        if not self.colors:
            raise ValueError("Palette vide")
        
        closest = self.colors[0]
        closest_index = 0
        min_distance = target_color.distance_to(closest)
        
        for i, color in enumerate(self.colors[1:], 1):
            distance = target_color.distance_to(color)
            if distance < min_distance:
                min_distance = distance
                closest = color
                closest_index = i
        
        return closest, closest_index
    
    def get_unique_colors(self) -> List[PixelColor]:
        """Retourne les couleurs uniques de la palette"""
        seen = set()
        unique = []
        
        for color in self.colors:
            rgb_key = color.rgb_tuple
            if rgb_key not in seen:
                seen.add(rgb_key)
                unique.append(color)
        
        return unique
    
    def sort_by_hue(self) -> None:
        """Trie les couleurs par teinte"""
        import colorsys
        
        def get_hue(color: PixelColor):
            r, g, b = color.rgb_normalized
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            return h
        
        self.colors.sort(key=get_hue)
    
    def sort_by_brightness(self) -> None:
        """Trie les couleurs par luminosité"""
        def get_brightness(color: PixelColor):
            # Formule de luminosité perceptuelle
            return 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        
        self.colors.sort(key=get_brightness)
    
    # === Export ===
    
    def to_gimp_format(self) -> str:
        """Exporte en format GIMP"""
        lines = ["GIMP Palette"]
        
        if 'name' in self.metadata:
            lines.append(f"Name: {self.metadata['name']}")
        
        if 'columns' in self.metadata:
            lines.append(f"Columns: {self.metadata['columns']}")
        
        lines.append("#")
        
        for color in self.colors:
            line = f"{color.r:3d} {color.g:3d} {color.b:3d}"
            if color.name:
                line += f"\t{color.name}"
            lines.append(line)
        
        return '\n'.join(lines)
    
    def to_hex_list(self) -> List[str]:
        """Exporte comme liste de couleurs hexadécimales"""
        return [color.hex for color in self.colors]
    
    def to_rgb_tuples(self) -> List[Tuple[int, int, int]]:
        """Exporte comme liste de tuples RGB"""
        return [color.rgb_tuple for color in self.colors]
    
    def to_formatted_string(self, format_type: str = "rgb", separator: str = "\n", 
                          include_header: bool = True, include_names: bool = True) -> str:
        """
        Formate la palette selon le type demandé
        
        Args:
            format_type: "rgb", "hex", "raw", "gimp"
            separator: Séparateur entre les couleurs
            include_header: Inclure les métadonnées en en-tête
            include_names: Inclure les noms des couleurs
        """
        if self.is_empty:
            return "# Palette vide"
        
        lines = []
        
        # En-tête avec métadonnées
        if include_header:
            lines.append(f"# Palette: {self.name}")
            lines.append(f"# Couleurs: {self.color_count}")
            lines.append(f"# Format: {self.format_type}")
            if self.source_filename:
                lines.append(f"# Source: {self.source_filename}")
            lines.append("#")
        
        # Formatage des couleurs
        if format_type == "hex":
            for color in self.colors:
                line = color.hex
                if include_names and color.name:
                    line += f" # {color.name}"
                lines.append(line)
        
        elif format_type == "rgb":
            for color in self.colors:
                line = f"rgb({color.r}, {color.g}, {color.b})"
                if include_names and color.name:
                    line += f" # {color.name}"
                lines.append(line)
        
        elif format_type == "raw":
            for color in self.colors:
                line = f"{color.r} {color.g} {color.b}"
                if include_names and color.name:
                    line += f" {color.name}"
                lines.append(line)
        
        elif format_type == "gimp":
            return self.to_gimp_format()
        
        else:
            # Format par défaut : rgb
            for color in self.colors:
                line = f"{color.r:3d} {color.g:3d} {color.b:3d}"
                if include_names and color.name:
                    line += f" # {color.name}"
                lines.append(line)
        
        return separator.join(lines)
    
    # === Propriétés ===
    
    @property
    def is_empty(self) -> bool:
        """Vérifie si la palette est vide"""
        return len(self.colors) == 0
    
    @property
    def color_count(self) -> int:
        """Nombre de couleurs dans la palette"""
        return len(self.colors)
    
    @property
    def name(self) -> str:
        """Nom de la palette"""
        return self.metadata.get('name', Path(self.source_filename).stem if self.source_filename else "Sans nom")
    
    @property
    def is_valid(self) -> bool:
        """Vérifie si la palette est valide"""
        return True  # Une palette peut être vide mais reste valide
    
    def __len__(self):
        return len(self.colors)
    
    def __getitem__(self, index):
        return self.colors[index]
    
    def __iter__(self):
        return iter(self.colors)
    
    def __str__(self):
        return f"PixelPalette('{self.name}', {self.color_count} couleurs, format: {self.format_type})"
    
    def __repr__(self):
        return self.__str__()
