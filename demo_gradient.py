#!/usr/bin/env python3
"""
Démonstration de la nouvelle méthode create_gradient de PixelPalette
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from lib.pixel_palette import PixelPalette

def demo_rgb_gradient():
    """Démontre un dégradé RGB"""
    print("=== Dégradé RGB ===")

    # Créer une palette avec 5 couleurs
    palette = PixelPalette()
    palette.add_color(255, 0, 0, "Rouge")      # index 0
    palette.add_color(128, 128, 128, "Gris1")  # index 1 - à modifier
    palette.add_color(128, 128, 128, "Gris2")  # index 2 - à modifier
    palette.add_color(128, 128, 128, "Gris3")  # index 3 - à modifier
    palette.add_color(0, 255, 0, "Vert")       # index 4

    print("Avant dégradé:")
    for i, color in enumerate(palette.colors):
        print(f"  {i}: {color}")

    # Créer un dégradé entre index 0 et 4
    palette.create_gradient(0, 4, "rgb")

    print("\nAprès dégradé RGB:")
    for i, color in enumerate(palette.colors):
        print(f"  {i}: {color}")

def demo_hsv_gradient():
    """Démontre un dégradé HSV"""
    print("\n=== Dégradé HSV ===")

    # Créer une palette avec des couleurs pour HSV
    palette = PixelPalette()
    palette.add_color(255, 0, 0, "Rouge")      # index 0 - Hue: 0°
    palette.add_color(128, 128, 128, "Gris1")  # index 1 - à modifier
    palette.add_color(128, 128, 128, "Gris2")  # index 2 - à modifier
    palette.add_color(0, 255, 0, "Vert")       # index 3 - Hue: 120°

    print("Avant dégradé:")
    for i, color in enumerate(palette.colors):
        print(f"  {i}: {color}")

    # Créer un dégradé HSV
    palette.create_gradient(0, 3, "hsv")

    print("\nAprès dégradé HSV:")
    for i, color in enumerate(palette.colors):
        print(f"  {i}: {color}")

def demo_error_cases():
    """Démontre les cas d'erreur"""
    print("\n=== Cas d'erreur ===")

    # Cas 1: Pas assez de couleurs entre les index
    palette1 = PixelPalette()
    palette1.add_color(255, 0, 0, "Rouge")
    palette1.add_color(0, 255, 0, "Vert")

    try:
        palette1.create_gradient(0, 1, "rgb")
    except ValueError as e:
        print(f"Erreur attendue (pas assez de couleurs): {e}")

    # Cas 2: index1 >= index2
    palette2 = PixelPalette()
    palette2.add_color(255, 0, 0, "Rouge")
    palette2.add_color(128, 128, 128, "Gris")
    palette2.add_color(0, 255, 0, "Vert")

    try:
        palette2.create_gradient(2, 0, "rgb")
    except ValueError as e:
        print(f"Erreur attendue (index1 >= index2): {e}")

if __name__ == "__main__":
    demo_rgb_gradient()
    demo_hsv_gradient()
    demo_error_cases()

    print("\n=== Démonstration terminée ===")
    print("La méthode create_gradient permet de créer des dégradés fluides")
    print("entre deux couleurs existantes dans la palette en modifiant")
    print("les couleurs intermédiaires sans en créer de nouvelles.")