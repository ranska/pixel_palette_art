# lib/palette/exporters/css_exporter.py

import re
from typing import List
from .base_exporter import BaseExporter
from ...pixel_color import PixelColor


class CSSExporter(BaseExporter):
    """Exporteur pour le format CSS custom properties."""

    def export(self, colors: List[PixelColor], **kwargs) -> str:
        """Exporte comme variables CSS custom properties."""
        include_names = kwargs.get('include_names', True)
        selector = kwargs.get('selector', ':root')

        lines = [f"{selector} {{"]
        for i, color in enumerate(colors):
            if include_names and color.name:
                var_name = self._sanitize_css_name(color.name)
            else:
                var_name = f"color-{i}"
            lines.append(f"  --{var_name}: {color.hex};")
        lines.append("}")

        return "\n".join(lines)

    @staticmethod
    def _sanitize_css_name(name: str) -> str:
        """Transforme un nom en identifiant CSS valide."""
        # Lowercase
        name = name.lower()
        # Espaces et underscores → tirets
        name = name.replace(' ', '-').replace('_', '-')
        # Suppression des caracteres non alphanumeriques (sauf tirets)
        name = re.sub(r'[^a-z0-9-]', '', name)
        # Suppression des tirets multiples
        name = re.sub(r'-+', '-', name)
        # Suppression des tirets en debut et fin
        name = name.strip('-')
        return name
