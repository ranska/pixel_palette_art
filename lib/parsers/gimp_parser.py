# lib/parsers/gimp_parser.py

import re
from typing import List, Optional, Dict, Any
from lib.parsers.base_parser import BaseParser
from lib.pixel_color import PixelColor

class GimpParser(BaseParser):
    """Parser pour les palettes GIMP (.gpl)."""

    def can_parse(self, content: str) -> bool:
        """Détecte si c'est une palette GIMP."""
        lines = content.strip().split('\n')
        return len(lines) > 0 and lines[0].strip().startswith('GIMP Palette')

    def parse(self, content: str) -> List[PixelColor]:
        """Parse une palette GIMP (.gpl)."""
        lines = content.strip().split('\n')

        if not lines:
            return []

        # Header
        header = lines[0].strip()
        if not header.startswith('GIMP Palette'):
            return []

        colors = []

        for i, line in enumerate(lines[1:], 1):
            line = line.strip()

            # Ignorer les lignes vides et commentaires
            if not line or line.startswith('#'):
                continue

            # Métadonnées de la palette (ignorées pour l'instant)
            if line.startswith('Name:') or line.startswith('Columns:'):
                continue

            # Parse des couleurs
            color = self._parse_color_line(line)
            if color:
                colors.append(color)

        return colors

    def _parse_color_line(self, line: str) -> Optional[PixelColor]:
        """Parse une ligne de couleur dans différents formats."""
        line = line.strip()

        # Format GIMP: "R G B Name"
        gimp_match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)(?:\s+(.+))?$', line)
        if gimp_match:
            r, g, b = map(int, gimp_match.groups()[:3])
            name = gimp_match.group(4) or ""
            return PixelColor(r, g, b, name.strip())

        return None