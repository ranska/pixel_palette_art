# lib/parsers/adobe_aco_parser.py

from .base_parser import BaseParser
from ..pixel_color import PixelColor

class AdobeAcoParser(BaseParser):
    """Parser pour les palettes Adobe ACO (binaire)."""

    def can_parse(self, content: str) -> bool:
        """Détecte si c'est une palette Adobe (binaire)"""
        if isinstance(content, bytes) and len(content) >= 2:
            return content[0] == 0x00 and content[1] == 0x01
        return False

    def parse(self, content: str) -> list:
        """Parse une palette Adobe ACO (binaire) - implémentation basique"""
        # Cette méthode nécessiterait une implémentation binaire plus complexe
        # Pour l'instant, retourne une liste vide
        return []