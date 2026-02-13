# lib/palette/palette_renderer.py
"""
Rendu visuel d'une palette de couleurs en image PIL.
Supporte les layouts grille, horizontal et vertical
avec affichage optionnel des noms, indices et valeurs hex.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional


class PaletteRenderer:
    """
    Génère une image PIL à partir d'une palette de couleurs
    """

    def __init__(self, palette):
        self.palette = palette

    def render(self, layout="grid", cell_size=32, columns=8,
               show_names=False, show_indices=False, show_hex=False) -> Image.Image:
        """
        Génère l'image de la palette

        Args:
            layout: "grid", "horizontal" ou "vertical"
            cell_size: Taille d'une cellule en pixels
            columns: Nombre de colonnes (mode grid uniquement)
            show_names: Afficher les noms des couleurs
            show_indices: Afficher les indices
            show_hex: Afficher la valeur hexadécimale

        Returns:
            Image PIL RGB
        """
        if self.palette.is_empty:
            return self._render_empty(cell_size)

        if layout == "horizontal":
            return self._render_horizontal(cell_size, show_names, show_indices, show_hex)
        elif layout == "vertical":
            return self._render_vertical(cell_size, show_names, show_indices, show_hex)
        else:
            return self._render_grid(cell_size, columns, show_names, show_indices, show_hex)

    def _render_grid(self, cell_size, columns, show_names, show_indices, show_hex):
        """Rendu en grille avec N colonnes"""
        count = self.palette.color_count
        columns = min(columns, count)
        rows = (count + columns - 1) // columns

        text_height = self._text_area_height(show_names, show_indices, show_hex)
        total_cell_height = cell_size + text_height

        width = columns * cell_size
        height = rows * total_cell_height

        img = Image.new('RGB', (width, height), (32, 32, 32))
        draw = ImageDraw.Draw(img)
        font = self._get_font()

        for i, color in enumerate(self.palette.colors):
            col = i % columns
            row = i // columns
            x = col * cell_size
            y = row * total_cell_height

            # Rectangle de couleur
            draw.rectangle(
                [(x, y), (x + cell_size - 1, y + cell_size - 1)],
                fill=(color.r, color.g, color.b)
            )

            # Texte sous la cellule
            if text_height > 0:
                self._draw_cell_text(
                    draw, font, color, i,
                    x, y + cell_size, cell_size,
                    show_names, show_indices, show_hex
                )

        return img

    def _render_horizontal(self, cell_size, show_names, show_indices, show_hex):
        """Rendu en bande horizontale"""
        count = self.palette.color_count

        text_height = self._text_area_height(show_names, show_indices, show_hex)
        total_cell_height = cell_size + text_height

        width = count * cell_size
        height = total_cell_height

        img = Image.new('RGB', (width, height), (32, 32, 32))
        draw = ImageDraw.Draw(img)
        font = self._get_font()

        for i, color in enumerate(self.palette.colors):
            x = i * cell_size
            draw.rectangle(
                [(x, 0), (x + cell_size - 1, cell_size - 1)],
                fill=(color.r, color.g, color.b)
            )

            if text_height > 0:
                self._draw_cell_text(
                    draw, font, color, i,
                    x, cell_size, cell_size,
                    show_names, show_indices, show_hex
                )

        return img

    def _render_vertical(self, cell_size, show_names, show_indices, show_hex):
        """Rendu en bande verticale"""
        count = self.palette.color_count

        has_text = show_names or show_indices or show_hex
        text_width = 120 if has_text else 0

        width = cell_size + text_width
        height = count * cell_size

        img = Image.new('RGB', (width, height), (32, 32, 32))
        draw = ImageDraw.Draw(img)
        font = self._get_font()

        for i, color in enumerate(self.palette.colors):
            y = i * cell_size
            draw.rectangle(
                [(0, y), (cell_size - 1, y + cell_size - 1)],
                fill=(color.r, color.g, color.b)
            )

            if has_text:
                text_parts = self._build_text_parts(color, i, show_names, show_indices, show_hex)
                label = " ".join(text_parts)
                text_color = (200, 200, 200)
                draw.text((cell_size + 4, y + 2), label, fill=text_color, font=font)

        return img

    def _render_empty(self, cell_size):
        """Image placeholder pour palette vide"""
        img = Image.new('RGB', (cell_size * 2, cell_size), (32, 32, 32))
        draw = ImageDraw.Draw(img)
        font = self._get_font()
        draw.text((4, 4), "vide", fill=(128, 128, 128), font=font)
        return img

    def _text_area_height(self, show_names, show_indices, show_hex):
        """Calcule la hauteur de la zone de texte sous chaque cellule"""
        lines = 0
        if show_indices or show_hex:
            lines += 1
        if show_names:
            lines += 1
        return lines * 14 if lines > 0 else 0

    def _build_text_parts(self, color, index, show_names, show_indices, show_hex):
        """Construit les parties de texte pour une cellule"""
        parts = []
        if show_indices:
            parts.append(f"[{index}]")
        if show_hex:
            parts.append(color.hex)
        if show_names and color.name:
            parts.append(color.name)
        return parts

    def _draw_cell_text(self, draw, font, color, index, x, y, cell_width,
                        show_names, show_indices, show_hex):
        """Dessine le texte sous une cellule de couleur"""
        text_color = (200, 200, 200)
        line_y = y + 1

        # Ligne 1: index et/ou hex
        if show_indices or show_hex:
            parts = []
            if show_indices:
                parts.append(f"[{index}]")
            if show_hex:
                parts.append(color.hex)
            label = " ".join(parts)
            draw.text((x + 2, line_y), label, fill=text_color, font=font)
            line_y += 14

        # Ligne 2: nom
        if show_names and color.name:
            draw.text((x + 2, line_y), color.name[:8], fill=text_color, font=font)

    def _get_font(self):
        """Retourne une police adaptée"""
        return ImageFont.load_default(size=10)
