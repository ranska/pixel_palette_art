# spec/mamba_config.py
"""
Configuration pour les tests mamba
"""

# Exemple de fichiers de test GIMP pour les specs
SAMPLE_GIMP_PALETTE = """GIMP Palette
Name: Test Palette
Columns: 4
#
# Couleurs primaires
255   0   0	Rouge
  0 255   0	Vert
  0   0 255	Bleu
#
# Couleurs secondaires
255 255   0	Jaune
255   0 255	Magenta
  0 255 255	Cyan
#
# Nuances de gris
  0   0   0	Noir
128 128 128	Gris
255 255 255	Blanc
"""

SAMPLE_HEX_PALETTE = """# Palette Hexadécimale
#FF0000 Rouge
#00FF00 Vert
#0000FF Bleu
#FFFF00 Jaune
#FF00FF Magenta
#00FFFF Cyan
#000000 Noir
#808080 Gris
#FFFFFF Blanc
"""

SAMPLE_RGB_PALETTE = """rgb(255,0,0) Rouge
rgb(0,255,0) Vert
rgb(0,0,255) Bleu
255,255,0 Jaune
255,0,255 Magenta
0,255,255 Cyan"""

MALFORMED_PALETTE = """GIMP Palette
255 0 Rouge incomplet
abc def ghi Pas des nombres
128 128 128 256 Trop de valeurs
128 128 128 Gris Valide
not a color line at all
"""

# Fichiers d'exemple pour tests d'intégration
PALETTES_SAMPLES = {
    'gimp': SAMPLE_GIMP_PALETTE,
    'hex': SAMPLE_HEX_PALETTE,
    'rgb': SAMPLE_RGB_PALETTE,
    'malformed': MALFORMED_PALETTE
}
