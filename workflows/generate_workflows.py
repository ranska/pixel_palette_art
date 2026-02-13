#!/usr/bin/env python3
"""
Générateur de workflows ComfyUI pour tester les nodes Pixel Palette Art.

Génère les fichiers JSON dans deux formats :
  - workflows/test/      → format UI (avec positions, liens visuels, notes)
  - workflows/test_api/  → format API (exécution directe via /prompt)

Chaque workflow connecte automatiquement un PreviewImage natif ComfyUI
après chaque node produisant une IMAGE, pour visualisation directe.

Usage :
    python workflows/generate_workflows.py
"""

import json
import os

# =============================================================================
# Types ComfyUI pour les connexions entre nodes
# =============================================================================

# Mapping type_name → type_id pour les liens dans le format UI
LINK_TYPES = {
    "PIXEL_COLOR": "PIXEL_COLOR",
    "PIXEL_PALETTE": "PIXEL_PALETTE",
    "IMAGE": "IMAGE",
    "STRING": "STRING",
    "INT": "INT",
    "FLOAT": "FLOAT",
}


# =============================================================================
# WorkflowBuilder : helper pour construire des workflows sans erreur d'IDs
# =============================================================================

class WorkflowBuilder:
    """Construit un workflow ComfyUI en gérant automatiquement les IDs."""

    # Couleurs pour les notes (ComfyUI utilise des noms)
    NOTE_COLOR_FR = "#232"
    NOTE_BGCOLOR_FR = "#353"
    NOTE_COLOR_EN = "#223"
    NOTE_BGCOLOR_EN = "#335"

    def __init__(self, title="Test Workflow"):
        self.title = title
        self._next_node_id = 1
        self._next_link_id = 1
        self._nodes = {}      # id → node_def
        self._links = []       # (link_id, src_id, src_slot, dst_id, dst_slot, type)

    def add_node(self, class_type, title, widgets=None, pos=(0, 0),
                 size=None, is_note=False, note_color=None, note_bgcolor=None):
        """Ajoute un node et retourne son ID."""
        node_id = str(self._next_node_id)
        self._next_node_id += 1

        node = {
            "id": node_id,
            "class_type": class_type,
            "title": title,
            "widgets": widgets or {},
            "pos": list(pos),
            "size": list(size) if size else None,
            "is_note": is_note,
            "note_color": note_color,
            "note_bgcolor": note_bgcolor,
        }
        self._nodes[node_id] = node
        return node_id

    def add_note_fr(self, text, pos=(0, 0), size=None):
        """Ajoute une note en français (verte)."""
        return self.add_node(
            "Note", "Note FR",
            widgets={"text": text},
            pos=pos,
            size=size or [350, 200],
            is_note=True,
            note_color=self.NOTE_COLOR_FR,
            note_bgcolor=self.NOTE_BGCOLOR_FR,
        )

    def add_note_en(self, text, pos=(0, 0), size=None):
        """Ajoute une note en anglais (bleue)."""
        return self.add_node(
            "Note", "Note EN",
            widgets={"text": text},
            pos=pos,
            size=size or [350, 200],
            is_note=True,
            note_color=self.NOTE_COLOR_EN,
            note_bgcolor=self.NOTE_BGCOLOR_EN,
        )

    def link(self, src_id, src_slot, dst_id, dst_slot, link_type):
        """Crée un lien entre deux nodes. Retourne le link_id."""
        link_id = self._next_link_id
        self._next_link_id += 1
        self._links.append((link_id, src_id, src_slot, dst_id, dst_slot, link_type))
        return link_id

    # --- Helpers pour les nodes courants ---

    def add_color_rgb(self, r, g, b, name="", pos=(0, 0)):
        """Ajoute un CreateColorFromRGBNode."""
        title = name if name else f"RGB({r},{g},{b})"
        return self.add_node(
            "CreateColorFromRGBNode", title,
            widgets={"red": r, "green": g, "blue": b, "color_name": name},
            pos=pos, size=[250, 170],
        )

    def add_gradient_palette(self, num_colors=8, color_space="rgb", pos=(0, 0)):
        """Ajoute un CreateGradientPaletteNode."""
        return self.add_node(
            "CreateGradientPaletteNode",
            f"Gradient {num_colors} ({color_space.upper()})",
            widgets={"num_colors": num_colors, "color_space": color_space},
            pos=pos, size=[280, 130],
        )

    def add_sort_palette(self, sort_by="hue", pos=(0, 0)):
        """Ajoute un SortPaletteNode."""
        return self.add_node(
            "SortPaletteNode", f"Sort ({sort_by})",
            widgets={"sort_by": sort_by},
            pos=pos, size=[250, 100],
        )

    def add_gradient_between(self, index_start=0, index_end=2,
                             color_space="rgb", pos=(0, 0)):
        """Ajoute un GradientBetweenNode."""
        return self.add_node(
            "GradientBetweenNode",
            f"Gradient Between [{index_start}→{index_end}]",
            widgets={
                "index_start": index_start,
                "index_end": index_end,
                "color_space": color_space,
            },
            pos=pos, size=[280, 130],
        )

    def add_palette_view(self, layout="grid", cell_size=32, columns=8,
                         show_hex=False, show_indices=False, show_names=False,
                         pos=(0, 0)):
        """Ajoute un PaletteViewNode."""
        return self.add_node(
            "PaletteViewNode", f"View ({layout})",
            widgets={
                "layout": layout,
                "cell_size": cell_size,
                "columns": columns,
                "show_names": show_names,
                "show_indices": show_indices,
                "show_hex": show_hex,
            },
            pos=pos, size=[280, 200],
        )

    def add_replace_color_at(self, index=0, pos=(0, 0)):
        """Ajoute un ReplaceColorAtNode."""
        return self.add_node(
            "ReplaceColorAtNode", f"Replace @{index}",
            widgets={"index": index},
            pos=pos, size=[250, 120],
        )

    def add_mix_colors(self, ratio=0.5, color_space="rgb", pos=(0, 0)):
        """Ajoute un MixColorsNode."""
        return self.add_node(
            "MixColorsNode", f"Mix ({color_space}, {ratio})",
            widgets={"ratio": ratio, "color_space": color_space},
            pos=pos, size=[250, 130],
        )

    def add_color_preview(self, show_text=True, text_format="hex", pos=(0, 0)):
        """Ajoute un ColorPreviewNode."""
        return self.add_node(
            "ColorPreviewNode", f"Preview ({text_format})",
            widgets={
                "width": 256, "height": 256,
                "show_text": show_text,
                "text_format": text_format,
                "text_color": "auto",
                "text_size": 24,
                "text_position": "center",
            },
            pos=pos, size=[280, 280],
        )

    def add_palette_formatter(self, format_type="hex", pos=(0, 0)):
        """Ajoute un PaletteFormatter."""
        return self.add_node(
            "PaletteFormatter", f"Format ({format_type})",
            widgets={
                "format_type": format_type,
                "separator": "\n",
                "include_header": True,
                "include_names": True,
            },
            pos=pos, size=[280, 160],
        )

    def add_preview_image(self, pos=(0, 0)):
        """Ajoute un PreviewImage (node natif ComfyUI)."""
        return self.add_node(
            "PreviewImage", "Preview",
            pos=pos, size=[250, 280],
        )

    def add_color_formatter(self, format_type="hex", pos=(0, 0)):
        """Ajoute un ColorFormatterNode."""
        return self.add_node(
            "ColorFormatterNode", f"Format ({format_type})",
            widgets={"format_type": format_type},
            pos=pos, size=[250, 120],
        )

    # --- Export formats ---

    def _build_node_inputs(self, node_id):
        """Construit la liste des inputs connectés pour un node donné."""
        inputs = []
        for (link_id, src_id, src_slot, dst_id, dst_slot, ltype) in self._links:
            if dst_id == node_id:
                inputs.append((dst_slot, link_id, src_id, src_slot, ltype))
        inputs.sort(key=lambda x: x[0])
        return inputs

    def _build_node_outputs(self, node_id):
        """Construit la liste des outputs connectés pour un node donné."""
        outputs = []
        for (link_id, src_id, src_slot, dst_id, dst_slot, ltype) in self._links:
            if src_id == node_id:
                outputs.append((src_slot, link_id, ltype))
        return outputs

    def _get_input_spec(self, class_type):
        """Retourne la spec des inputs/outputs pour chaque class_type."""
        specs = {
            "CreateColorFromRGBNode": {
                "inputs": [
                    # Widget-only inputs (red, green, blue, color_name)
                ],
                "outputs": [("PIXEL_COLOR", "color")],
            },
            "CreateGradientPaletteNode": {
                "inputs": [
                    ("PIXEL_COLOR", "color_start"),
                    ("PIXEL_COLOR", "color_end"),
                ],
                "outputs": [("PIXEL_PALETTE", "gradient_palette")],
            },
            "SortPaletteNode": {
                "inputs": [("PIXEL_PALETTE", "palette")],
                "outputs": [("PIXEL_PALETTE", "sorted_palette")],
            },
            "GradientBetweenNode": {
                "inputs": [("PIXEL_PALETTE", "palette")],
                "outputs": [("PIXEL_PALETTE", "gradient_palette")],
            },
            "PaletteViewNode": {
                "inputs": [("PIXEL_PALETTE", "palette")],
                "outputs": [("IMAGE", "image")],
            },
            "ReplaceColorAtNode": {
                "inputs": [
                    ("PIXEL_PALETTE", "palette"),
                    ("PIXEL_COLOR", "color"),
                ],
                "outputs": [("PIXEL_PALETTE", "modified_palette")],
            },
            "MixColorsNode": {
                "inputs": [
                    ("PIXEL_COLOR", "color_a"),
                    ("PIXEL_COLOR", "color_b"),
                ],
                "outputs": [("PIXEL_COLOR", "mixed_color")],
            },
            "ColorPreviewNode": {
                "inputs": [("PIXEL_COLOR", "color")],
                "outputs": [("IMAGE", "image")],
            },
            "ColorFormatterNode": {
                "inputs": [("PIXEL_COLOR", "color")],
                "outputs": [("STRING", "formatted_color")],
            },
            "PaletteFormatter": {
                "inputs": [("PIXEL_PALETTE", "palette")],
                "outputs": [("STRING", "formatted_text")],
            },
            "PreviewImage": {
                "inputs": [("IMAGE", "images")],
                "outputs": [],
            },
            "Note": {
                "inputs": [],
                "outputs": [],
            },
        }
        return specs.get(class_type, {"inputs": [], "outputs": []})

    def to_ui_json(self):
        """Exporte au format UI ComfyUI (LiteGraph)."""
        nodes = []
        for nid, node in self._nodes.items():
            spec = self._get_input_spec(node["class_type"])
            connected_inputs = self._build_node_inputs(nid)
            connected_outputs = self._build_node_outputs(nid)

            # Construire les inputs du node
            ui_inputs = []
            for i, (itype, iname) in enumerate(spec["inputs"]):
                link_id = None
                for (slot, lid, sid, sslot, ltype) in connected_inputs:
                    if slot == i:
                        link_id = lid
                        break
                ui_inputs.append({
                    "name": iname,
                    "type": itype,
                    "link": link_id,
                })

            # Construire les outputs du node
            ui_outputs = []
            for i, (otype, oname) in enumerate(spec["outputs"]):
                out_links = [lid for (slot, lid, ltype) in connected_outputs
                             if slot == i]
                ui_outputs.append({
                    "name": oname,
                    "type": otype,
                    "links": out_links if out_links else None,
                })

            ui_node = {
                "id": int(nid),
                "type": node["class_type"],
                "pos": node["pos"],
                "size": node["size"] or [250, 150],
                "flags": {},
                "order": int(nid) - 1,
                "mode": 0,
                "inputs": ui_inputs if ui_inputs else None,
                "outputs": ui_outputs if ui_outputs else None,
                "title": node["title"],
                "properties": {"Node name for S&R": node["class_type"]},
                "widgets_values": list(node["widgets"].values()),
            }

            if node.get("is_note"):
                ui_node["color"] = node.get("note_color", "")
                ui_node["bgcolor"] = node.get("note_bgcolor", "")

            # Nettoyer les None
            ui_node = {k: v for k, v in ui_node.items() if v is not None}

            nodes.append(ui_node)

        # Liens au format LiteGraph : [link_id, src_id, src_slot, dst_id, dst_slot, type]
        links = []
        for (link_id, src_id, src_slot, dst_id, dst_slot, ltype) in self._links:
            links.append([link_id, int(src_id), src_slot, int(dst_id), dst_slot, ltype])

        return {
            "last_node_id": self._next_node_id - 1,
            "last_link_id": self._next_link_id - 1,
            "nodes": nodes,
            "links": links,
            "groups": [],
            "config": {},
            "extra": {
                "ds": {"scale": 1, "offset": [0, 0]},
                "info": {"title": self.title},
            },
            "version": 0.4,
        }

    def to_api_json(self):
        """Exporte au format API ComfyUI (POST /prompt)."""
        api = {}
        for nid, node in self._nodes.items():
            if node["is_note"]:
                continue

            spec = self._get_input_spec(node["class_type"])
            connected_inputs = self._build_node_inputs(nid)

            inputs = dict(node["widgets"])

            # Ajouter les connexions comme références [src_id, src_slot]
            for i, (itype, iname) in enumerate(spec["inputs"]):
                for (slot, lid, sid, sslot, ltype) in connected_inputs:
                    if slot == i:
                        inputs[iname] = [str(sid), sslot]
                        break

            api[nid] = {
                "class_type": node["class_type"],
                "inputs": inputs,
                "_meta": {"title": node["title"]},
            }

        return api


# =============================================================================
# Fonctions de création de workflows
# =============================================================================

def make_notes(text_fr, text_en, nodes_used):
    """Formate les textes pour les notes FR et EN."""
    node_list = ", ".join(nodes_used)
    note_fr = (
        f"\U0001f1eb\U0001f1f7 FRAN\u00c7AIS\n"
        f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
        f"{text_fr}\n\n"
        f"\u26a1 Nodes utilis\u00e9s : {node_list}"
    )
    note_en = (
        f"\U0001f1ec\U0001f1e7 ENGLISH\n"
        f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
        f"{text_en}\n\n"
        f"\u26a1 Nodes used: {node_list}"
    )
    return note_fr, note_en


# --- Workflow 1 : test_sort_palette ---

def build_sort_palette():
    wb = WorkflowBuilder("Test — SortPaletteNode")

    note_fr, note_en = make_notes(
        "Tri d'une palette par teinte (hue) et par luminosit\u00e9 (brightness).\n"
        "Un d\u00e9grad\u00e9 de 8 couleurs est cr\u00e9\u00e9 entre rouge et bleu,\n"
        "puis tri\u00e9 selon deux crit\u00e8res diff\u00e9rents pour comparer le r\u00e9sultat.",
        "Sorting a palette by hue and by brightness.\n"
        "An 8-color gradient from red to blue is created,\n"
        "then sorted by two different criteria to compare results.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode",
         "SortPaletteNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 220))

    # Couleurs source
    c_red = wb.add_color_rgb(220, 30, 30, "Rouge", pos=(0, 480))
    c_blue = wb.add_color_rgb(30, 50, 220, "Bleu", pos=(0, 680))

    # Dégradé
    grad = wb.add_gradient_palette(8, "hsv", pos=(320, 560))
    wb.link(c_red, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_blue, 0, grad, 1, "PIXEL_COLOR")

    # Vue originale
    view_orig = wb.add_palette_view("horizontal", 40, 8, pos=(660, 460))
    wb.link(grad, 0, view_orig, 0, "PIXEL_PALETTE")
    pv_orig = wb.add_preview_image(pos=(1000, 380))
    wb.link(view_orig, 0, pv_orig, 0, "IMAGE")

    # Tri par hue
    sort_hue = wb.add_sort_palette("hue", pos=(660, 600))
    wb.link(grad, 0, sort_hue, 0, "PIXEL_PALETTE")
    view_hue = wb.add_palette_view("horizontal", 40, 8, pos=(980, 560))
    wb.link(sort_hue, 0, view_hue, 0, "PIXEL_PALETTE")
    pv_hue = wb.add_preview_image(pos=(1320, 480))
    wb.link(view_hue, 0, pv_hue, 0, "IMAGE")

    # Tri par brightness
    sort_bright = wb.add_sort_palette("brightness", pos=(660, 740))
    wb.link(grad, 0, sort_bright, 0, "PIXEL_PALETTE")
    view_bright = wb.add_palette_view("horizontal", 40, 8, pos=(980, 700))
    wb.link(sort_bright, 0, view_bright, 0, "PIXEL_PALETTE")
    pv_bright = wb.add_preview_image(pos=(1320, 620))
    wb.link(view_bright, 0, pv_bright, 0, "IMAGE")

    return wb


# --- Workflow 2 : test_gradient_between ---

def build_gradient_between():
    wb = WorkflowBuilder("Test — GradientBetweenNode")

    note_fr, note_en = make_notes(
        "Interpolation entre deux couleurs d'une palette existante.\n"
        "On cr\u00e9e un d\u00e9grad\u00e9 de 8 couleurs (rouge → bleu) puis on remplace\n"
        "les couleurs entre les indices 2 et 5 par un nouveau d\u00e9grad\u00e9 interpol\u00e9.\n"
        "Comparez la palette avant et apr\u00e8s l'op\u00e9ration.",
        "Interpolating between two colors in an existing palette.\n"
        "We create an 8-color gradient (red → blue), then replace\n"
        "colors between indices 2 and 5 with a new interpolated gradient.\n"
        "Compare the palette before and after the operation.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode",
         "GradientBetweenNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 230))

    # Couleurs
    c_red = wb.add_color_rgb(255, 50, 50, "Rouge", pos=(0, 500))
    c_blue = wb.add_color_rgb(50, 50, 255, "Bleu", pos=(0, 700))

    # Dégradé de base
    grad = wb.add_gradient_palette(8, "rgb", pos=(320, 580))
    wb.link(c_red, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_blue, 0, grad, 1, "PIXEL_COLOR")

    # Vue avant
    view_before = wb.add_palette_view(
        "horizontal", 48, 8, show_indices=True, pos=(660, 480))
    wb.link(grad, 0, view_before, 0, "PIXEL_PALETTE")
    pv_before = wb.add_preview_image(pos=(1000, 400))
    wb.link(view_before, 0, pv_before, 0, "IMAGE")

    # Gradient between
    gb = wb.add_gradient_between(2, 5, "rgb", pos=(660, 640))
    wb.link(grad, 0, gb, 0, "PIXEL_PALETTE")

    # Vue après
    view_after = wb.add_palette_view(
        "horizontal", 48, 8, show_indices=True, pos=(1000, 580))
    wb.link(gb, 0, view_after, 0, "PIXEL_PALETTE")
    pv_after = wb.add_preview_image(pos=(1340, 500))
    wb.link(view_after, 0, pv_after, 0, "IMAGE")

    return wb


# --- Workflow 3 : test_create_gradient_palette ---

def build_create_gradient_palette():
    wb = WorkflowBuilder("Test — CreateGradientPaletteNode")

    note_fr, note_en = make_notes(
        "Comparaison de d\u00e9grad\u00e9s cr\u00e9\u00e9s en RGB vs HSV.\n"
        "M\u00eames couleurs de d\u00e9part (rouge) et d'arriv\u00e9e (bleu),\n"
        "mais l'interpolation en HSV passe par les teintes interm\u00e9diaires\n"
        "(vert, cyan) tandis que RGB m\u00e9lange lin\u00e9airement.",
        "Comparison of gradients created in RGB vs HSV.\n"
        "Same start (red) and end (blue) colors,\n"
        "but HSV interpolation passes through intermediate hues\n"
        "(green, cyan) while RGB mixes linearly.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 230))

    # Couleurs
    c_red = wb.add_color_rgb(255, 0, 0, "Rouge", pos=(0, 500))
    c_blue = wb.add_color_rgb(0, 0, 255, "Bleu", pos=(0, 700))

    # Branche RGB
    grad_rgb = wb.add_gradient_palette(16, "rgb", pos=(320, 480))
    wb.link(c_red, 0, grad_rgb, 0, "PIXEL_COLOR")
    wb.link(c_blue, 0, grad_rgb, 1, "PIXEL_COLOR")

    view_rgb = wb.add_palette_view("horizontal", 36, 16, pos=(660, 460))
    wb.link(grad_rgb, 0, view_rgb, 0, "PIXEL_PALETTE")
    pv_rgb = wb.add_preview_image(pos=(1000, 380))
    wb.link(view_rgb, 0, pv_rgb, 0, "IMAGE")

    # Branche HSV
    grad_hsv = wb.add_gradient_palette(16, "hsv", pos=(320, 680))
    wb.link(c_red, 0, grad_hsv, 0, "PIXEL_COLOR")
    wb.link(c_blue, 0, grad_hsv, 1, "PIXEL_COLOR")

    view_hsv = wb.add_palette_view("horizontal", 36, 16, pos=(660, 660))
    wb.link(grad_hsv, 0, view_hsv, 0, "PIXEL_PALETTE")
    pv_hsv = wb.add_preview_image(pos=(1000, 580))
    wb.link(view_hsv, 0, pv_hsv, 0, "IMAGE")

    return wb


# --- Workflow 4 : test_palette_view ---

def build_palette_view():
    wb = WorkflowBuilder("Test — PaletteViewNode (3 layouts)")

    note_fr, note_en = make_notes(
        "D\u00e9monstration des 3 dispositions (layouts) de PaletteView :\n"
        "- grid : grille avec colonnes configurables\n"
        "- horizontal : bande horizontale\n"
        "- vertical : bande verticale\n"
        "Le mode grille active show_hex et show_indices pour montrer les options.",
        "Demonstration of all 3 PaletteView layouts:\n"
        "- grid: configurable column grid\n"
        "- horizontal: horizontal strip\n"
        "- vertical: vertical strip\n"
        "Grid mode has show_hex and show_indices enabled to showcase options.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 240))

    # Source
    c_start = wb.add_color_rgb(255, 100, 0, "Orange", pos=(0, 500))
    c_end = wb.add_color_rgb(0, 100, 255, "Bleu ciel", pos=(0, 700))
    grad = wb.add_gradient_palette(12, "hsv", pos=(320, 580))
    wb.link(c_start, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_end, 0, grad, 1, "PIXEL_COLOR")

    # Grid (avec hex + indices)
    v_grid = wb.add_palette_view(
        "grid", 48, 4, show_hex=True, show_indices=True, pos=(660, 460))
    wb.link(grad, 0, v_grid, 0, "PIXEL_PALETTE")
    pv_grid = wb.add_preview_image(pos=(1000, 380))
    wb.link(v_grid, 0, pv_grid, 0, "IMAGE")

    # Horizontal
    v_horiz = wb.add_palette_view("horizontal", 40, 12, pos=(660, 680))
    wb.link(grad, 0, v_horiz, 0, "PIXEL_PALETTE")
    pv_horiz = wb.add_preview_image(pos=(1000, 600))
    wb.link(v_horiz, 0, pv_horiz, 0, "IMAGE")

    # Vertical
    v_vert = wb.add_palette_view("vertical", 40, 1, pos=(1300, 460))
    wb.link(grad, 0, v_vert, 0, "PIXEL_PALETTE")
    pv_vert = wb.add_preview_image(pos=(1300, 680))
    wb.link(v_vert, 0, pv_vert, 0, "IMAGE")

    return wb


# --- Workflow 5 : test_replace_color_at ---

def build_replace_color_at():
    wb = WorkflowBuilder("Test — ReplaceColorAtNode")

    note_fr, note_en = make_notes(
        "Remplacement d'une couleur \u00e0 un index pr\u00e9cis dans une palette.\n"
        "Un d\u00e9grad\u00e9 rouge→bleu de 8 couleurs est cr\u00e9\u00e9, puis la couleur\n"
        "\u00e0 l'index 3 est remplac\u00e9e par du vert vif.\n"
        "Comparez les vues 'Avant' et 'Apr\u00e8s'.",
        "Replacing a color at a specific index in a palette.\n"
        "A red→blue gradient of 8 colors is created, then the color\n"
        "at index 3 is replaced with bright green.\n"
        "Compare the 'Before' and 'After' views.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode",
         "ReplaceColorAtNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 230))

    # Palette source
    c_red = wb.add_color_rgb(200, 30, 30, "Rouge", pos=(0, 500))
    c_blue = wb.add_color_rgb(30, 30, 200, "Bleu", pos=(0, 700))
    grad = wb.add_gradient_palette(8, "rgb", pos=(320, 580))
    wb.link(c_red, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_blue, 0, grad, 1, "PIXEL_COLOR")

    # Vue avant
    view_before = wb.add_palette_view(
        "horizontal", 48, 8, show_indices=True, pos=(660, 480))
    wb.link(grad, 0, view_before, 0, "PIXEL_PALETTE")
    pv_before = wb.add_preview_image(pos=(1000, 400))
    wb.link(view_before, 0, pv_before, 0, "IMAGE")

    # Couleur de remplacement
    c_green = wb.add_color_rgb(0, 255, 0, "Vert vif", pos=(320, 760))

    # Remplacement à l'index 3
    replace = wb.add_replace_color_at(3, pos=(660, 660))
    wb.link(grad, 0, replace, 0, "PIXEL_PALETTE")
    wb.link(c_green, 0, replace, 1, "PIXEL_COLOR")

    # Vue après
    view_after = wb.add_palette_view(
        "horizontal", 48, 8, show_indices=True, pos=(1000, 600))
    wb.link(replace, 0, view_after, 0, "PIXEL_PALETTE")
    pv_after = wb.add_preview_image(pos=(1340, 520))
    wb.link(view_after, 0, pv_after, 0, "IMAGE")

    return wb


# --- Workflow 6 : test_mix_colors ---

def build_mix_colors():
    wb = WorkflowBuilder("Test — MixColorsNode")

    note_fr, note_en = make_notes(
        "M\u00e9lange de deux couleurs avec ratio 50/50.\n"
        "Comparaison du m\u00e9lange en espace RGB vs HSV.\n"
        "Le m\u00e9lange RGB donne un violet sombre,\n"
        "le m\u00e9lange HSV passe par les teintes interm\u00e9diaires.",
        "Mixing two colors with 50/50 ratio.\n"
        "Comparison of mixing in RGB vs HSV color space.\n"
        "RGB mixing gives a dark violet,\n"
        "HSV mixing goes through intermediate hues.",
        ["CreateColorFromRGBNode", "MixColorsNode", "ColorPreviewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 220))

    # Couleurs source
    c_red = wb.add_color_rgb(255, 0, 0, "Rouge", pos=(0, 480))
    c_cyan = wb.add_color_rgb(0, 200, 255, "Cyan", pos=(0, 680))

    # Mix RGB
    mix_rgb = wb.add_mix_colors(0.5, "rgb", pos=(320, 480))
    wb.link(c_red, 0, mix_rgb, 0, "PIXEL_COLOR")
    wb.link(c_cyan, 0, mix_rgb, 1, "PIXEL_COLOR")

    preview_rgb = wb.add_color_preview(True, "hex", pos=(640, 440))
    wb.link(mix_rgb, 0, preview_rgb, 0, "PIXEL_COLOR")
    pv_rgb = wb.add_preview_image(pos=(980, 380))
    wb.link(preview_rgb, 0, pv_rgb, 0, "IMAGE")

    # Mix HSV
    mix_hsv = wb.add_mix_colors(0.5, "hsv", pos=(320, 680))
    wb.link(c_red, 0, mix_hsv, 0, "PIXEL_COLOR")
    wb.link(c_cyan, 0, mix_hsv, 1, "PIXEL_COLOR")

    preview_hsv = wb.add_color_preview(True, "hex", pos=(640, 660))
    wb.link(mix_hsv, 0, preview_hsv, 0, "PIXEL_COLOR")
    pv_hsv = wb.add_preview_image(pos=(980, 600))
    wb.link(preview_hsv, 0, pv_hsv, 0, "IMAGE")

    return wb


# --- Workflow 7 : test_color_preview ---

def build_color_preview():
    wb = WorkflowBuilder("Test — ColorPreviewNode")

    note_fr, note_en = make_notes(
        "Pr\u00e9visualisation d'une couleur avec affichage de sa valeur hex.\n"
        "Cr\u00e9e une couleur via CreateColorFromRGB puis g\u00e9n\u00e8re\n"
        "une image de pr\u00e9visualisation 256\u00d7256.",
        "Color preview displaying its hex value.\n"
        "Creates a color via CreateColorFromRGB then generates\n"
        "a 256\u00d7256 preview image.",
        ["CreateColorFromRGBNode", "ColorPreviewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 200))

    c = wb.add_color_rgb(64, 180, 130, "Vert menthe", pos=(0, 440))
    preview = wb.add_color_preview(True, "hex", pos=(320, 420))
    wb.link(c, 0, preview, 0, "PIXEL_COLOR")
    pv = wb.add_preview_image(pos=(660, 360))
    wb.link(preview, 0, pv, 0, "IMAGE")

    return wb


# --- Workflow 8 : test_palette_formatter ---

def build_palette_formatter():
    wb = WorkflowBuilder("Test — PaletteFormatter")

    note_fr, note_en = make_notes(
        "Export d'une palette en texte format\u00e9.\n"
        "Un d\u00e9grad\u00e9 de 6 couleurs est export\u00e9 au format hex\n"
        "avec en-t\u00eate et noms de couleurs.",
        "Exporting a palette as formatted text.\n"
        "A 6-color gradient is exported in hex format\n"
        "with header and color names.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode", "PaletteFormatter"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 200))

    c_start = wb.add_color_rgb(255, 200, 0, "Jaune", pos=(0, 440))
    c_end = wb.add_color_rgb(150, 0, 200, "Violet", pos=(0, 640))

    grad = wb.add_gradient_palette(6, "rgb", pos=(320, 520))
    wb.link(c_start, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_end, 0, grad, 1, "PIXEL_COLOR")

    fmt = wb.add_palette_formatter("hex", pos=(660, 500))
    wb.link(grad, 0, fmt, 0, "PIXEL_PALETTE")

    return wb


# --- Workflow 9 : test_comp_full_pipeline ---

def build_comp_full_pipeline():
    wb = WorkflowBuilder("Composition — Full Pipeline")

    note_fr, note_en = make_notes(
        "Pipeline complet : cr\u00e9ation → tri → interpolation → visualisation.\n"
        "1. Cr\u00e9ation d'un d\u00e9grad\u00e9 12 couleurs (orange → violet)\n"
        "2. Tri par luminosit\u00e9 (brightness)\n"
        "3. Interpolation (gradient between) entre indices 0 et 5\n"
        "4. Visualisation en grille avec hex + indices",
        "Full pipeline: creation → sort → interpolation → visualization.\n"
        "1. Create a 12-color gradient (orange → purple)\n"
        "2. Sort by brightness\n"
        "3. Gradient between interpolation at indices 0 and 5\n"
        "4. Grid view with hex + indices",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode",
         "SortPaletteNode", "GradientBetweenNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0), size=[380, 240])
    wb.add_note_en(note_en, pos=(0, 260), size=[380, 240])

    # Source
    c_orange = wb.add_color_rgb(255, 140, 0, "Orange", pos=(0, 540))
    c_purple = wb.add_color_rgb(130, 0, 200, "Violet", pos=(0, 740))

    # Gradient
    grad = wb.add_gradient_palette(12, "hsv", pos=(320, 620))
    wb.link(c_orange, 0, grad, 0, "PIXEL_COLOR")
    wb.link(c_purple, 0, grad, 1, "PIXEL_COLOR")

    # Sort
    sort_node = wb.add_sort_palette("brightness", pos=(660, 620))
    wb.link(grad, 0, sort_node, 0, "PIXEL_PALETTE")

    # Gradient between
    gb = wb.add_gradient_between(0, 5, "rgb", pos=(960, 620))
    wb.link(sort_node, 0, gb, 0, "PIXEL_PALETTE")

    # Vue finale
    view = wb.add_palette_view(
        "grid", 48, 6, show_hex=True, show_indices=True, pos=(1280, 560))
    wb.link(gb, 0, view, 0, "PIXEL_PALETTE")
    pv = wb.add_preview_image(pos=(1620, 480))
    wb.link(view, 0, pv, 0, "IMAGE")

    return wb


# --- Workflow 10 : test_comp_gradient_compare ---

def build_comp_gradient_compare():
    wb = WorkflowBuilder("Composition — RGB vs HSV Gradient Compare")

    note_fr, note_en = make_notes(
        "Comparaison c\u00f4te \u00e0 c\u00f4te de d\u00e9grad\u00e9s RGB et HSV.\n"
        "M\u00eames couleurs de d\u00e9part (rouge vif) et d'arriv\u00e9e (vert for\u00eat),\n"
        "le d\u00e9grad\u00e9 HSV produit des teintes plus vari\u00e9es\n"
        "car il parcourt le cercle chromatique.",
        "Side-by-side comparison of RGB and HSV gradients.\n"
        "Same start (bright red) and end (forest green) colors,\n"
        "the HSV gradient produces more varied hues\n"
        "as it traverses the color wheel.",
        ["CreateColorFromRGBNode", "CreateGradientPaletteNode", "PaletteViewNode"],
    )
    wb.add_note_fr(note_fr, pos=(0, 0))
    wb.add_note_en(note_en, pos=(0, 230))

    # Couleurs
    c_red = wb.add_color_rgb(230, 20, 20, "Rouge vif", pos=(0, 500))
    c_green = wb.add_color_rgb(0, 120, 40, "Vert for\u00eat", pos=(0, 700))

    # Branche RGB
    grad_rgb = wb.add_gradient_palette(12, "rgb", pos=(320, 480))
    wb.link(c_red, 0, grad_rgb, 0, "PIXEL_COLOR")
    wb.link(c_green, 0, grad_rgb, 1, "PIXEL_COLOR")

    view_rgb = wb.add_palette_view(
        "horizontal", 40, 12, show_hex=True, pos=(660, 460))
    wb.link(grad_rgb, 0, view_rgb, 0, "PIXEL_PALETTE")
    pv_rgb = wb.add_preview_image(pos=(1000, 380))
    wb.link(view_rgb, 0, pv_rgb, 0, "IMAGE")

    # Branche HSV
    grad_hsv = wb.add_gradient_palette(12, "hsv", pos=(320, 680))
    wb.link(c_red, 0, grad_hsv, 0, "PIXEL_COLOR")
    wb.link(c_green, 0, grad_hsv, 1, "PIXEL_COLOR")

    view_hsv = wb.add_palette_view(
        "horizontal", 40, 12, show_hex=True, pos=(660, 660))
    wb.link(grad_hsv, 0, view_hsv, 0, "PIXEL_PALETTE")
    pv_hsv = wb.add_preview_image(pos=(1000, 580))
    wb.link(view_hsv, 0, pv_hsv, 0, "IMAGE")

    return wb


# =============================================================================
# Registre des workflows et génération
# =============================================================================

WORKFLOWS = {
    "test_sort_palette": build_sort_palette,
    "test_gradient_between": build_gradient_between,
    "test_create_gradient_palette": build_create_gradient_palette,
    "test_palette_view": build_palette_view,
    "test_replace_color_at": build_replace_color_at,
    "test_mix_colors": build_mix_colors,
    "test_color_preview": build_color_preview,
    "test_palette_formatter": build_palette_formatter,
    "test_comp_full_pipeline": build_comp_full_pipeline,
    "test_comp_gradient_compare": build_comp_gradient_compare,
}


def generate_all():
    """Génère tous les workflows dans les deux formats."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(script_dir, "test")
    api_dir = os.path.join(script_dir, "test_api")

    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(api_dir, exist_ok=True)

    for name, builder_fn in WORKFLOWS.items():
        wb = builder_fn()

        # Format UI
        ui_path = os.path.join(test_dir, f"{name}.json")
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(wb.to_ui_json(), f, indent=2, ensure_ascii=False)
        print(f"  UI  → {os.path.relpath(ui_path, script_dir)}")

        # Format API
        api_path = os.path.join(api_dir, f"{name}.json")
        with open(api_path, "w", encoding="utf-8") as f:
            json.dump(wb.to_api_json(), f, indent=2, ensure_ascii=False)
        print(f"  API → {os.path.relpath(api_path, script_dir)}")

    total = len(WORKFLOWS) * 2
    print(f"\n{total} fichiers générés ({len(WORKFLOWS)} UI + {len(WORKFLOWS)} API)")


if __name__ == "__main__":
    print("Génération des workflows de test Pixel Palette Art\n")
    generate_all()
