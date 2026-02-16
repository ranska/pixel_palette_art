# lib/parsers/adobe_aco_parser.py

import struct
from .base_parser import BaseParser
from ..pixel_color import PixelColor


class AdobeAcoParser(BaseParser):
    """Parser pour les palettes Adobe ACO (binaire).

    Format ACO v1 :
    - 2 octets : version (0x0001)
    - 2 octets : nombre de couleurs (big-endian uint16)
    - Par couleur : 2 octets color space + 4×2 octets canaux (big-endian uint16)
    Seul le color space 0 (RGB) est supporté, les autres sont ignorés.
    """

    # Taille d'un bloc couleur : 2 (color space) + 4×2 (canaux) = 10 octets
    _COLOR_BLOCK_SIZE = 10
    # Taille minimale : 2 (version) + 2 (count) = 4 octets
    _HEADER_SIZE = 4

    def can_parse(self, content: str) -> bool:
        """Détecte si c'est une palette Adobe ACO v1"""
        if isinstance(content, bytes) and len(content) >= 2:
            return content[0] == 0x00 and content[1] == 0x01
        return False

    def parse(self, content: str) -> list:
        """Parse une palette Adobe ACO binaire.

        Retourne les couleurs RGB trouvées. Les couleurs non-RGB sont ignorées.
        En cas de fichier tronqué, retourne les couleurs lues avant la troncature.
        """
        if not isinstance(content, bytes) or len(content) < self._HEADER_SIZE:
            return []

        num_colors = struct.unpack('>H', content[2:4])[0]
        colors = []
        offset = self._HEADER_SIZE

        for _ in range(num_colors):
            # Vérifier qu'on a assez d'octets pour lire un bloc couleur
            if offset + self._COLOR_BLOCK_SIZE > len(content):
                break

            color_space = struct.unpack('>H', content[offset:offset + 2])[0]
            w, x, y, z = struct.unpack('>HHHH', content[offset + 2:offset + 10])
            offset += self._COLOR_BLOCK_SIZE

            # Seul RGB (color space 0) est supporté
            if color_space == 0:
                r = round(w * 255 / 65535)
                g = round(x * 255 / 65535)
                b = round(y * 255 / 65535)
                colors.append(PixelColor(r, g, b))

        return colors
