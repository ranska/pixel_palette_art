# lib/palette/exporters/amiga_exporter.py

from typing import List
from .base_exporter import BaseExporter
from ...pixel_color import PixelColor


class AmigaExporter(BaseExporter):
    """Exporteur pour le format Amiga OCS/ECS (couleurs 12-bit)."""

    def export(self, colors: List[PixelColor], **kwargs) -> str:
        """Exporte en couleurs 12-bit pour Amiga 500/600."""
        output_format = kwargs.get('output_format', 'txt')
        include_names = kwargs.get('include_names', False)
        palette_name = kwargs.get('palette_name', 'Palette')

        if output_format == 'c':
            return self._export_c(colors, include_names, palette_name)
        return self._export_txt(colors, include_names)

    def _export_txt(self, colors: List[PixelColor], include_names: bool) -> str:
        """Export au format texte simple (#RGB)."""
        lines = []
        for color in colors:
            r = self.quantize_channel(color.r)
            g = self.quantize_channel(color.g)
            b = self.quantize_channel(color.b)
            line = f"#{r:01X}{g:01X}{b:01X}"
            if include_names and color.name:
                line += f"  /* {color.name} */"
            lines.append(line)
        return "\n".join(lines)

    def _export_c(self, colors: List[PixelColor], include_names: bool, palette_name: str) -> str:
        """Export au format C (tableau UWORD pour Amiga)."""
        lines = []
        lines.append(f"// Palette: {palette_name}")
        lines.append(f"// Colors: {len(colors)}")
        lines.append(f"#define PALETTE_SIZE {len(colors)}")
        lines.append("")
        lines.append("UWORD palette[] = {")

        for i, color in enumerate(colors):
            r = self.quantize_channel(color.r)
            g = self.quantize_channel(color.g)
            b = self.quantize_channel(color.b)
            value = f"0x0{r:01X}{g:01X}{b:01X}"
            is_last = (i == len(colors) - 1)

            if include_names and color.name:
                comment = f"  /* {color.name} */"
            else:
                comment = ""

            if is_last:
                lines.append(f"  {value}{comment}")
            else:
                lines.append(f"  {value},{comment}")

        lines.append("};")
        return "\n".join(lines)

    @staticmethod
    def quantize_channel(value: int) -> int:
        """Quantifie un canal 8-bit (0-255) en 4-bit (0-15)."""
        return round(value / 255 * 15)
