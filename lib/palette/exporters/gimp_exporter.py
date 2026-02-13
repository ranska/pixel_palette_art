# lib/palette/exporters/gimp_exporter.py

from typing import List, Dict, Any, Optional
from .base_exporter import BaseExporter
from ...pixel_color import PixelColor

class GimpExporter(BaseExporter):
    """Exporteur pour le format GIMP (.gpl)."""

    def export(self, colors: List[PixelColor], metadata: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """Exporte en format GIMP"""
        lines = ["GIMP Palette"]

        if metadata:
            if 'name' in metadata:
                lines.append(f"Name: {metadata['name']}")

            if 'columns' in metadata:
                lines.append(f"Columns: {metadata['columns']}")

        lines.append("#")

        for color in colors:
            line = f"{color.r:3d} {color.g:3d} {color.b:3d}"
            if color.name:
                line += f"\t{color.name}"
            lines.append(line)

        return '\n'.join(lines)