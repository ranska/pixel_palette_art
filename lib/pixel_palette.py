
# lib/pixel_palette.py
import re
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path
from .pixel_color import PixelColor
from .palette.exporter_context import PaletteExporter

@dataclass
class PixelPalette:
    """
    Classe métier pour gérer les palettes de couleurs
    Supporte les formats GIMP (.gpl), Adobe (.aco), etc.
    """

    name:   str              = "Untitled Palette"
    colors: List[PixelColor] = field(default_factory=list)
    raw_content: str = ""
    source_filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    format_type: str = "unknown"

    def __post_init__(self):
        # Parse automatiquement si du contenu est fourni
        if self.raw_content.strip():
            self._parse_content()

    @classmethod
    def create_monochrome(cls, color: PixelColor, count: int, name: Optional[str] = None) -> 'PixelPalette':
        """
        Crée une palette monochrome avec une couleur répétée count fois

        Args:
            color: La couleur de base à répéter
            count: Le nombre de fois à répéter la couleur
            name: Nom optionnel de la palette

        Returns:
            PixelPalette: Une nouvelle palette contenant la couleur répétée

        Raises:
            ValueError: Si count est inférieur ou égal à 0
        """
        if count <= 0:
            raise ValueError("Le count doit être supérieur à 0")

        # Nom par défaut basé sur la couleur
        if name is None:
            color_name = color.name if color.name else color.hex
            name = f"Palette monochrome - {color_name}"

        # Créer la liste de couleurs
        colors = []
        for i in range(count):
            color_copy = color.create_copy()
            colors.append(color_copy)

        pixel_palette = cls()
        #  pixel_palette.name = name
        pixel_palette.colors = colors
        return pixel_palette

    def __init__(self, name: str = "Untitled Palette",
                 colors: Optional[List[PixelColor]] = None,
                 raw_content: str = "",
                 source_filename: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None,
                 format_type: str = "unknown"):
        self.name = name
        self.colors = colors if colors is not None else []
        self.raw_content = raw_content
        self.source_filename = source_filename
        self.metadata = metadata if metadata is not None else {}
        self.format_type = format_type

        # Parse automatiquement si du contenu est fourni
        if self.raw_content.strip():
            self._parse_content()
    
    def _parse_content(self):
        """Parse le contenu selon le format détecté"""
        if not self.raw_content.strip():
            return

        from .parsers.parser_registry import ParserRegistry

        # Essayer les parsers enregistrés
        for format_name in ParserRegistry.available_formats():
            parser_class = ParserRegistry.get_parser_class(format_name)
            parser = parser_class()
            if parser.can_parse(self.raw_content):
                self.format_type = format_name
                self.colors = parser.parse(self.raw_content)
                break
    

    
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

    def create_gradient(self, index1: int, index2: int, color_space: str = "rgb") -> None:
        """
        Crée un dégradé entre deux couleurs en modifiant les couleurs existantes entre les index.

        Args:
            index1: Index de la première couleur (doit être < index2)
            index2: Index de la deuxième couleur
            color_space: Espace de couleur pour l'interpolation ("rgb" ou "hsv")

        Raises:
            ValueError: Si index1 >= index2 ou s'il n'y a pas au moins une couleur entre
            IndexError: Si les index sont hors limites
        """
        # Validation des paramètres
        if index1 >= index2:
            raise ValueError("index1 doit être inférieur à index2")

        if index1 < 0 or index2 >= len(self.colors):
            raise IndexError("Index hors limites")

        # Vérifier qu'il y a au moins une couleur entre les deux
        if index2 - index1 < 2:
            raise ValueError("Il doit y avoir au moins une couleur entre index1 et index2")

        # Récupérer les couleurs de départ et d'arrivée
        start_color = self.colors[index1]
        end_color = self.colors[index2]

        # Calculer le nombre de couleurs intermédiaires
        num_intermediate = index2 - index1 - 1

        # Pour chaque couleur intermédiaire
        for i in range(1, num_intermediate + 1):
            # Calculer le ratio (de 0.0 à 1.0)
            ratio = i / (num_intermediate + 1)

            # Calculer l'index de la couleur à modifier
            current_index = index1 + i

            # Utiliser le mixer approprié selon l'espace de couleur
            from .color.color_space_registry import ColorSpaceRegistry
            mixer = ColorSpaceRegistry.get_mixer_class(color_space)

            # Calculer la nouvelle couleur
            new_r, new_g, new_b = mixer.mix_with(start_color, end_color, ratio)

            # Mettre à jour la couleur existante (conserver le nom)
            original_name = self.colors[current_index].name
            self.colors[current_index] = PixelColor(new_r, new_g, new_b, original_name)
    
    # === Export ===

    def to_list(self, format_type: str = "hex", include_names: bool = False) -> List[str]:
        """
        Exporte la palette comme liste de strings

        Args:
            format_type: "hex", "rgb", etc.
            include_names: Inclure les noms des couleurs

        Returns:
            List[str]: Liste des couleurs formatées
        """
        with PaletteExporter(self, format_type) as ctx:
            return ctx.export_list(include_names=include_names)

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

        # En-tête avec métadonnées
        header = ""
        if include_header:
            header_lines = [
                f"# Palette: {self.name}",
                f"# Couleurs: {self.color_count}",
                f"# Format: {self.format_type}"
            ]
            if self.source_filename:
                header_lines.append(f"# Source: {self.source_filename}")
            header_lines.append("#")
            header = "\n".join(header_lines) + "\n"

        # Utiliser le contexte d'export
        with PaletteExporter(self, format_type) as ctx:
            content = ctx.export(separator=separator, include_names=include_names)
            return header + content

    def to_rgb_tuples(self) -> List[Tuple[int, int, int]]:
        """
        Exporte la palette comme liste de tuples RGB

        Returns:
            List[Tuple[int, int, int]]: Liste des tuples RGB
        """
        with PaletteExporter(self, "rgb") as ctx:
            return ctx.export_tuples()


    
    # === Propriétés ===
    
    @property
    def is_empty(self) -> bool:
        """Vérifie si la palette est vide"""
        return len(self.colors) == 0
    
    @property
    def color_count(self) -> int:
        """Nombre de couleurs dans la palette"""
        return len(self.colors)
    
    #  @property
    #  def name(self) -> str:
        #  """Nom de la palette"""
        #  return self.metadata.get('name', Path(self.source_filename).stem if self.source_filename else "Sans nom")
    
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
    
    #  def __str__(self):
        #  return f"PixelPalette('{self.name}', {self.color_count} couleurs, format: {self.format_type})"
    
    #  def __repr__(self):
        #  return self.__str__()
