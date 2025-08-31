# lib/palette/exporters/hex_exporter.py

from typing import List
from .base_exporter import BaseExporter
from ...pixel_color import PixelColor

class HexExporter(BaseExporter):
    """Exporteur pour le format hexadécimal."""

    def export(self, colors: List[PixelColor], **kwargs) -> str:
        """Exporte comme liste de couleurs hexadécimales"""
        include_names = kwargs.get('include_names', False)
        separator = kwargs.get('separator', '\n')

        lines = []
        for color in colors:
            line = color.hex
            if include_names and color.name:
                line += f" # {color.name}"
            lines.append(line)

        return separator.join(lines)