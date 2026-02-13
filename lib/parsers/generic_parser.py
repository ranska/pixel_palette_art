# lib/parsers/generic_parser.py

import re
from typing import List, Optional
from .base_parser import BaseParser
from ..pixel_color import PixelColor

class GenericParser(BaseParser):
    """Parser générique pour différents formats de couleurs."""

    def can_parse(self, content: str) -> bool:
        """Le parser générique peut toujours essayer de parser."""
        return True

    def parse(self, content: str) -> List[PixelColor]:
        """Parse un format générique (hex, rgb, etc.)."""
        lines = content.strip().split('\n')
        colors = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            color = self._parse_color_line(line)
            if color:
                colors.append(color)

        return colors

    def _parse_color_line(self, line: str) -> Optional[PixelColor]:
        """Parse une ligne de couleur dans différents formats."""
        line = line.strip()

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