# lib/palette/exporters/rgb_exporter.py

from typing import List, Tuple
from .base_exporter import BaseExporter
from ...pixel_color import PixelColor

class RGBExporter(BaseExporter):
    """Exporteur pour le format RGB."""

    def export(self, colors: List[PixelColor], **kwargs) -> str:
        """Exporte comme format RGB"""
        include_names = kwargs.get('include_names', True)
        separator = kwargs.get('separator', '\n')

        lines = []
        for color in colors:
            line = f"rgb({color.r}, {color.g}, {color.b})"
            if include_names and color.name:
                line += f" # {color.name}"
            lines.append(line)

        return separator.join(lines)

    def export_tuples(self, colors: List[PixelColor], **kwargs) -> List[Tuple[int, int, int]]:
        """Exporte comme liste de tuples RGB"""
        return [color.rgb_tuple for color in colors]