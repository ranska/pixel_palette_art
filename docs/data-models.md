# Modeles de données

## PixelColor

**Fichier** : `lib/pixel_color.py`

Dataclass représentant une couleur individuelle avec ses métadonnées.

### Attributs

| Attribut | Type | Défaut | Description |
|----------|------|--------|-------------|
| r | int | requis | Canal rouge (0-255, clampé dans `__post_init__`) |
| g | int | requis | Canal vert (0-255) |
| b | int | requis | Canal bleu (0-255) |
| name | str | "" | Nom optionnel de la couleur |
| color_space | str | "rgb" | Espace colorimétrique actif pour le mélange |

### Propriétés

```python
color = PixelColor(255, 128, 0, "Orange")

color.hex            # "#ff8000"
color.rgb_tuple      # (255, 128, 0)
color.rgb_normalized # (1.0, 0.502, 0.0)
color.exporter       # Instance RGBExporter (lazy-loaded)
```

### Méthodes

#### mix_with(color, ratio=0.5) -> PixelColor

Mélange **en place** avec une autre couleur. Utilise le mixer de l'espace colorimétrique actuel.

```python
red = PixelColor(255, 0, 0)
blue = PixelColor(0, 0, 255)
red.mix_with(blue, 0.5)  # red est maintenant (127, 0, 127)
```

**Attention** : cette méthode **modifie** l'instance. Utiliser `create_copy()` avant si on veut préserver l'original.

#### create_copy() -> PixelColor

Copie profonde de la couleur (tous les attributs).

```python
original = PixelColor(255, 0, 0, "Rouge", "hsv")
copy = original.create_copy()
# copy.r == 255, copy.name == "Rouge", copy.color_space == "hsv"
```

#### distance_to(other) -> float

Distance euclidienne en espace RGB. Utilisée pour trouver la couleur la plus proche.

```python
red = PixelColor(255, 0, 0)
orange = PixelColor(255, 128, 0)
red.distance_to(orange)  # ~128.0
```

#### using_color_space(new_space) -> ColorSpaceContext

Context manager pour changer temporairement l'espace colorimétrique.

```python
color = PixelColor(255, 0, 0)  # color_space = "rgb"

with color.using_color_space("hsv"):
    color.mix_with(other, 0.5)  # mélange en HSV
# color_space restauré a "rgb"
```

#### to_hex() -> str

Format hexadécimal majuscule : `"#FF8040"`

#### Exporter (via propriété `exporter`)

```python
color.exporter.to_hex()               # "#FF8000"
color.exporter.to_hex_alpha(0.5)       # "#FF800080"
color.exporter.to_rgb_string()         # "rgb(255, 128, 0)"
color.exporter.to_rgba_string(0.5)     # "rgba(255, 128, 0, 0.5)"
color.exporter.to_rgb_tuple()          # "(255, 128, 0)"
color.exporter.to_rgba_tuple(128)      # "(255, 128, 0, 128)"
color.exporter.to_hsl_string()         # "hsl(30, 100%, 50%)"
color.exporter.to_css_var("primary")   # "--primary: #FF8000;"
color.exporter.to_gimp_palette_line(0) # "255 128   0\tOrange"
```

### Validation

`__post_init__` clampe les valeurs RGB entre 0 et 255 :

```python
color = PixelColor(300, -10, 128)
# color.r == 255, color.g == 0, color.b == 128
```

---

## PixelPalette

**Fichier** : `lib/pixel_palette.py`

Classe pour gérer une collection de couleurs avec métadonnées et opérations de manipulation.

### Attributs

| Attribut | Type | Défaut | Description |
|----------|------|--------|-------------|
| name | str | "Untitled Palette" | Nom de la palette |
| colors | List[PixelColor] | [] | Liste des couleurs |
| raw_content | str | "" | Contenu brut (pour parsing automatique) |
| source_filename | Optional[str] | None | Fichier source |
| metadata | Dict[str, Any] | {} | Métadonnées libres |
| format_type | str | "unknown" | Format détecté après parsing |

**Note** : le `__init__` actuel est simplifié et initialise seulement `colors = []`. Le `@dataclass` et `__init__` coexistent (le `__init__` explicite a priorité).

### Protocole séquence

PixelPalette implémente le protocole séquence Python :

```python
palette = PixelPalette()
palette.add_color(255, 0, 0, "Rouge")
palette.add_color(0, 255, 0, "Vert")

len(palette)        # 2
palette[0]          # PixelColor(255, 0, 0, "Rouge")
for color in palette:
    print(color)    # Itération
```

### Propriétés

```python
palette.is_empty     # True si aucune couleur
palette.color_count  # Nombre de couleurs
palette.is_valid     # Toujours True (une palette vide est valide)
```

### Méthodes de manipulation

#### add_color(r, g, b, name="")

```python
palette.add_color(255, 0, 0, "Rouge")
```

#### remove_color(index) -> bool

Supprime par index. Retourne `True` si suppression réussie.

```python
palette.remove_color(0)  # True
palette.remove_color(99) # False (hors limites)
```

#### find_closest_color(target) -> (PixelColor, int)

Recherche linéaire par distance euclidienne RGB.

```python
target = PixelColor(250, 10, 10)
closest, index = palette.find_closest_color(target)
```

#### get_unique_colors() -> List[PixelColor]

Déduplique les couleurs par tuple RGB.

#### sort_by_hue()

Tri en place par teinte HSV (utilise `colorsys`).

#### sort_by_brightness()

Tri en place par luminosité perceptuelle : `0.299*R + 0.587*G + 0.114*B`

#### create_gradient(index1, index2, color_space="rgb")

Interpole les couleurs **entre** deux index existants.

```python
palette = PixelPalette()
palette.add_color(255, 0, 0, "Rouge")     # 0
palette.add_color(0, 0, 0, "Placeholder") # 1
palette.add_color(0, 0, 0, "Placeholder") # 2
palette.add_color(0, 0, 255, "Bleu")      # 3

palette.create_gradient(0, 3, "rgb")
# palette[1] et palette[2] sont maintenant des couleurs interpolées
```

**Contraintes** :
- `index1 < index2`
- Au moins une couleur entre les deux index
- Leve `ValueError` ou `IndexError` si invalide

### Factory methods

#### create_monochrome(color, count, name=None) -> PixelPalette

Crée une palette avec `count` copies d'une même couleur.

```python
red = PixelColor(255, 0, 0, "Rouge")
mono = PixelPalette.create_monochrome(red, 5)
# 5 copies indépendantes de Rouge
```

### Méthodes d'export

#### to_formatted_string(format_type, separator, include_header, include_names) -> str

Export complet avec en-tête optionnel. Utilise `PaletteExporter` en interne.

```python
palette.to_formatted_string("hex", separator="\n", include_header=True)
# "# Palette: Mon palette\n# Couleurs: 3\n...\n#FF0000\n#00FF00\n#0000FF"
```

#### to_list(format_type, include_names) -> List[str]

Liste de strings formatées.

```python
palette.to_list("hex")  # ["#FF0000", "#00FF00", "#0000FF"]
```

#### to_rgb_tuples() -> List[Tuple[int, int, int]]

```python
palette.to_rgb_tuples()  # [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
```

### Parsing automatique

Si `raw_content` est fourni, `__post_init__` lance le parsing via `ParserRegistry` :

```python
content = "GIMP Palette\nName: Test\n#\n255   0   0\tRouge"
palette = PixelPalette(raw_content=content)
# palette.colors contient les couleurs parsées
# palette.format_type == "gimp"
```

Les parsers sont essayés dans l'ordre d'enregistrement. Le premier qui retourne `can_parse() == True` est utilisé.

---

## Relations entre modeles

```
PixelPalette
  └── colors: List[PixelColor]
        ├── .exporter -> RGBExporter (export individuel)
        └── .mix_with() -> ColorSpaceRegistry -> Mixer

PixelPalette
  ├── .to_formatted_string() -> PaletteExporter -> ExporterRegistry -> Exporter
  └── ._parse_content() -> ParserRegistry -> Parser -> List[PixelColor]
```
