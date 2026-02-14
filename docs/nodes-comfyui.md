# Référence des nodes ComfyUI

## Vue d'ensemble

L'extension fournit 8 nodes organisés en catégories. Chaque node est un **adaptateur fin** qui délègue la logique a `lib/`.

Les nodes définissent le contrat ComfyUI :
- `INPUT_TYPES` : paramètres d'entrée (required/optional)
- `RETURN_TYPES` / `RETURN_NAMES` : sorties
- `FUNCTION` : nom de la méthode de traitement
- `CATEGORY` : placement dans le menu ComfyUI

## Types custom

| Type | Classe Python | Description |
|------|---------------|-------------|
| `PIXEL_COLOR` | `PixelColor` | Couleur avec r, g, b, name, color_space |
| `PIXEL_PALETTE` | `PixelPalette` | Palette de couleurs avec metadata |

## Nodes

### GimpPaletteLoader

**Fichier** : `nodes/gimp_palette_loader_node.py`
**Catégorie** : `pixel_art/io`

Charge un fichier palette (.gpl, .pal, .aco) depuis le dossier `input/` de ComfyUI.

| Entrée | Type | Description |
|--------|------|-------------|
| palette_file | STRING | Nom du fichier (sélecteur) |

| Sortie | Type |
|--------|------|
| palette | PIXEL_PALETTE |

**Particularités** :
- Lecture multi-encodage (UTF-8, Latin-1, CP1252)
- Détection automatique du format via ParserRegistry
- `IS_CHANGED` pour la gestion du cache ComfyUI

### CreateColorFromRGB

**Fichier** : `nodes/create_color_from_rgb_node.py`
**Catégorie** : `pixel_art/colors`

Crée une couleur a partir de valeurs RGB.

| Entrée | Type | Défaut | Plage |
|--------|------|--------|-------|
| red | INT | 0 | 0-255 |
| green | INT | 0 | 0-255 |
| blue | INT | 0 | 0-255 |
| color_name | STRING | "" | - |

| Sortie | Type |
|--------|------|
| color | PIXEL_COLOR |

### MixColors

**Fichier** : `nodes/mix_colors_node.py`
**Catégorie** : `pixel_art/colors`

Mélange deux couleurs avec ratio et choix d'espace colorimétrique.

| Entrée | Type | Défaut |
|--------|------|--------|
| color_a | PIXEL_COLOR | - |
| color_b | PIXEL_COLOR | - |
| ratio | FLOAT | 0.5 (0.0-1.0) |
| color_space | STRING | "rgb" (choix: "rgb", "hsv") |

| Sortie | Type |
|--------|------|
| color | PIXEL_COLOR |

**Logique** : utilise `ColorSpaceContext` pour mélanger dans l'espace choisi :
```python
with base.using_color_space(color_space):
    mixed = base.mix_with(color_b, ratio)
```

### ReplaceColorAt

**Fichier** : `nodes/palette/replace_color_at_node.py`
**Catégorie** : `pixel_art/palette`

Remplace la couleur a un index donné dans une palette.

| Entrée | Type | Défaut | Plage |
|--------|------|--------|-------|
| palette | PIXEL_PALETTE | - | - |
| color | PIXEL_COLOR | - | - |
| index | INT | 0 | 0-255 |

| Sortie | Type |
|--------|------|
| palette | PIXEL_PALETTE |

**Particularités** :
- Crée une **copie profonde** de la palette (pas de mutation de l'original)
- Valide les bornes de l'index
- Import dynamique via `importlib` pour compatibilité

### ColorFormatter

**Fichier** : `nodes/color_formatter_node.py`
**Catégorie** : `pixel_art/output`

Exporte une couleur individuelle en format texte.

| Entrée | Type | Défaut |
|--------|------|--------|
| color | PIXEL_COLOR | - |
| format_type | STRING | "hex" |
| alpha_value | FLOAT | 1.0 (optionnel) |
| css_var_name | STRING | "color" (optionnel) |
| gimp_index | INT | 0 (optionnel) |

Formats disponibles : `hex`, `hex_alpha`, `rgb`, `rgba`, `tuple`, `tuple_alpha`, `hsl`, `css`, `gimp`

| Sortie | Type |
|--------|------|
| formatted | STRING |

Délègue a `PixelColor.exporter` (instance de `RGBExporter`).

### PaletteFormatter

**Fichier** : `nodes/palette_formatter_node.py`
**Catégorie** : `pixel_art/output`

Exporte une palette entiere en format texte.

| Entrée | Type | Défaut |
|--------|------|--------|
| palette | PIXEL_PALETTE | - |
| format_type | STRING | "rgb" (choix: "rgb", "hex", "raw", "gimp") |
| separator | STRING | "\n" |
| include_header | BOOLEAN | True |
| include_names | BOOLEAN | True |

| Sortie | Type |
|--------|------|
| formatted | STRING |

Délègue a `PixelPalette.to_formatted_string()`.

### ColorPreview

**Fichier** : `nodes/color_preview_node.py`
**Catégorie** : `pixel_art/output`

Génère une image de prévisualisation d'une couleur.

| Entrée | Type | Défaut |
|--------|------|--------|
| color | PIXEL_COLOR | - |
| width | INT | 256 |
| height | INT | 256 |
| show_text | BOOLEAN | True (optionnel) |
| text_format | STRING | "hex" (optionnel) |
| text_color | STRING | "auto" (optionnel) |
| text_size | INT | 24 (optionnel) |
| text_position | STRING | "center" (optionnel) |
| background_color | STRING | "none" (optionnel) |

| Sortie | Type |
|--------|------|
| image | IMAGE (tensor ComfyUI) |

**Particularités** :
- Couleur du texte automatique (noir/blanc selon luminance du fond)
- Conversion PIL Image -> Torch tensor pour ComfyUI

### PixelPaletteExtractor

**Fichier** : `nodes/pixel_palette_extractor_node.py`
**Catégorie** : `image/color`

Extrait les couleurs uniques d'une image et génère une grille visuelle.

| Entrée | Type | Défaut |
|--------|------|--------|
| image | IMAGE | - |
| palette_width | INT | 512 |
| color_size | INT | 32 |
| show_indices | BOOLEAN | True |
| font_size | INT | 10 |

| Sortie | Type |
|--------|------|
| palette_image | IMAGE (tensor ComfyUI) |

**Algorithme d'extraction** (3 niveaux de fallback) :
1. Conversion palette adaptative PIL
2. Quantification directe
3. Analyse pixel par pixel des couleurs uniques

## Pipeline de conversion d'image

Les nodes qui manipulent des images suivent ce pipeline :

```
ComfyUI Tensor (4D: batch, height, width, channels, float 0-1)
    ↓ torch.cpu().numpy() * 255 → uint8
PIL Image (RGB ou RGBA)
    ↓ [traitement: dessin, texte, extraction]
PIL Image
    ↓ np.array() / 255.0 → float32
    ↓ torch.from_numpy().unsqueeze(0)
ComfyUI Tensor (4D output)
```

## Enregistrement des nodes

Le fichier `__init__.py` racine déclare tous les nodes aupres de ComfyUI :

```python
NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader":      GimpPaletteLoaderNode,
    "PaletteFormatter":       PaletteFormatterNode,
    "PixelPaletteExtractor":  PixelPaletteExtractorNode,
    "CreateColorFromRGBNode": CreateColorFromRGBNode,
    "ColorFormatterNode":     ColorFormatterNode,
    "ColorPreviewNode":       ColorPreviewNode,
    "MixColorsNode":          MixColorsNode,
    "ReplaceColorAtNode":     ReplaceColorAtNode,
}
```

`ReplaceColorAtNode` est importé dynamiquement via `importlib` pour gérer les problemes de chemin d'import imbriqué.

## Créer un nouveau node

1. Créer le fichier dans `nodes/` (ou `nodes/<sous-dossier>/`)
2. Implémenter le contrat ComfyUI :

```python
class MonNouveauNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE",),
                "option": (["choix1", "choix2"],),
            },
            "optional": {
                "param": ("STRING", {"default": "valeur"}),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("palette",)
    FUNCTION = "process"
    CATEGORY = "pixel_art/palette"

    def process(self, palette, option, param="valeur"):
        # Déléguer a lib/ pour la logique
        # Retourner un tuple
        return (result,)
```

3. Importer dans `nodes/__init__.py`
4. Enregistrer dans `__init__.py` racine (NODE_CLASS_MAPPINGS + NODE_DISPLAY_NAME_MAPPINGS)
5. La logique métier va dans `lib/`, le node ne fait que l'appeler
