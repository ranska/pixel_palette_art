# spec/pixel_palette_spec.py
from mamba import description, context, it, before
from expects import expect, be_empty, have_length, equal, be_true, be_false, contain, start_with, end_with
import sys
import os

# Ajout du chemin parent pour importer la lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette, PixelColor

#
with description('PixelPalette') as self:
    with context('Création et initialisation'):
        with it('crée une palette vide par défaut'):
            palette = PixelPalette()
            expect(palette.colors).to(be_empty)
            expect(palette.color_count).to(equal(0))
            expect(palette.is_empty).to(be_true)
            expect(palette.format_type).to(equal('unknown'))
        with it('crée une palette avec du contenu'):
            content = "GIMP Palette\nName: Test\n255 0 0 Rouge\n0 255 0 Vert"
            palette = PixelPalette(raw_content=content, source_filename="test.gpl")

            expect(palette.raw_content).to(equal(content))
            expect(palette.source_filename).to(equal("test.gpl"))
            expect(palette.colors).not_to(be_empty)

    with context('Parsing GIMP format'):

        with before.each:
            self.gimp_content = """GIMP Palette
Name: Ma Palette de Test
Columns: 4
#
255   0   0	Rouge
  0 255   0	Vert
  0   0 255	Bleu
128 128 128	Gris
"""
            self.palette = PixelPalette(raw_content=self.gimp_content, source_filename="test.gpl")
        
        with it('détecte le format GIMP'):
            expect(self.palette.format_type).to(equal('gimp'))
        
        with it('parse les métadonnées'):
            expect(self.palette.metadata.get('name')).to(equal('Ma Palette de Test'))
            expect(self.palette.metadata.get('columns')).to(equal(4))
            expect(self.palette.metadata.get('format')).to(equal('GIMP Palette'))
        
        with it('parse les couleurs correctement'):
            expect(self.palette.colors).to(have_length(4))
            
            # Première couleur
            rouge = self.palette.colors[0]
            expect(rouge.r).to(equal(255))
            expect(rouge.g).to(equal(0))
            expect(rouge.b).to(equal(0))
            expect(rouge.name).to(equal('Rouge'))
            expect(rouge.hex).to(equal('#ff0000'))
        
        with it('ignore les commentaires et lignes vides'):
            content_avec_commentaires = """GIMP Palette
Name: Test
#
# Ceci est un commentaire
255 0 0 Rouge

# Autre commentaire
0 255 0 Vert
"""
            palette = PixelPalette(raw_content=content_avec_commentaires)
            expect(palette.colors).to(have_length(2))
    
    with context('Parsing formats génériques'):
        
        with it('parse le format hexadécimal'):
            hex_content = """#ff0000 Rouge
#00ff00 Vert
#0000ff Bleu
ff8000
"""
            palette = PixelPalette(raw_content=hex_content)
            expect(palette.format_type).to(equal('generic'))
            expect(palette.colors).to(have_length(4))
            
            rouge = palette.colors[0]
            expect(rouge.r).to(equal(255))
            expect(rouge.name).to(equal('Rouge'))
            
            # Couleur sans nom
            orange = palette.colors[3]
            expect(orange.r).to(equal(255))
            expect(orange.g).to(equal(128))
            expect(orange.b).to(equal(0))
            expect(orange.name).to(equal(''))
        
        with it('parse le format RGB'):
            rgb_content = """rgb(255,0,0) Rouge
255, 255, 0 Jaune
128 64 192 Violet
"""
            palette = PixelPalette(raw_content=rgb_content)
            expect(palette.colors).to(have_length(3))
            
            rouge = palette.colors[0]
            expect(rouge.rgb_tuple).to(equal((255, 0, 0)))
            expect(rouge.name).to(equal('Rouge'))
    
    with context('Classe PixelColor'):
        
        with it('valide les valeurs RGB'):
            # Valeurs normales
            color = PixelColor(255, 128, 0, "Orange")
            expect(color.r).to(equal(255))
            expect(color.g).to(equal(128))
            expect(color.b).to(equal(0))
            
            # Valeurs hors limites
            color_clamped = PixelColor(300, -10, 256, "Test")
            expect(color_clamped.r).to(equal(255))  # Max 255
            expect(color_clamped.g).to(equal(0))    # Min 0
            expect(color_clamped.b).to(equal(255))  # Max 255
        
        with it('calcule les propriétés correctement'):
            color = PixelColor(255, 128, 0, "Orange")
            
            expect(color.hex).to(equal('#ff8000'))
            expect(color.rgb_tuple).to(equal((255, 128, 0)))
            expect(color.rgb_normalized).to(equal((1.0, 0.5019607843137255, 0.0)))
        
        with it('calcule la distance entre couleurs'):
            rouge = PixelColor(255, 0, 0)
            vert = PixelColor(0, 255, 0)
            rouge_proche = PixelColor(250, 5, 5)
            
            distance_rouge_vert = rouge.distance_to(vert)
            distance_rouge_proche = rouge.distance_to(rouge_proche)
            
            expect(distance_rouge_vert).to(equal(360.6242068697262))  # sqrt(255² + 255²)
            expect(distance_rouge_proche).to(equal(7.0710678118654755))  # sqrt(5² + 5² + 5²)
    
    with context('Méthodes utilitaires'):
        
        with before.each:
            self.palette = PixelPalette()
            self.palette.add_color(255, 0, 0, "Rouge")
            self.palette.add_color(0, 255, 0, "Vert")
            self.palette.add_color(255, 0, 0, "Rouge Dupliqué")  # Couleur identique
        
        with it('ajoute des couleurs'):
            expect(self.palette.colors).to(have_length(3))
            expect(self.palette.colors[0].name).to(equal("Rouge"))
        
        with it('supprime des couleurs'):
            success = self.palette.remove_color(1)  # Supprimer le vert
            expect(success).to(be_true)
            expect(self.palette.colors).to(have_length(2))
            expect(self.palette.colors[1].name).to(equal("Rouge Dupliqué"))
            
            # Index invalide
            failure = self.palette.remove_color(10)
            expect(failure).to(be_false)
        
        with it('trouve la couleur la plus proche'):
            target = PixelColor(250, 10, 10)  # Proche du rouge
            closest, index = self.palette.find_closest_color(target)
            
            expect(closest.name).to(equal("Rouge"))
            expect(index).to(equal(0))
        
        with it('retourne les couleurs uniques'):
            unique = self.palette.get_unique_colors()
            expect(unique).to(have_length(2))  # Rouge et Vert (pas de dupliqué)
    
    with context('Formatage de sortie'):
        
        with before.each:
            content = """GIMP Palette
Name: Test Formatting
255 0 0 Rouge
0 255 0 Vert
0 0 255 Bleu
"""
            self.palette = PixelPalette(raw_content=content)
        
        with it('formate en RGB'):
            result = self.palette.to_formatted_string(format_type="rgb")
            print(f"DEBUG RGB: '{result}'")  # Debug
            
            expect(result).not_to(be_empty)
            expect(result).to(contain("# Palette: Test Formatting"))
            expect(result).to(contain("# Couleurs: 3"))
            expect(result).to(contain("rgb(255, 0, 0) # Rouge"))
            expect(result).to(contain("rgb(0, 255, 0) # Vert"))
            expect(result).to(contain("rgb(0, 0, 255) # Bleu"))
        
        with it('formate en hexadécimal'):
            result = self.palette.to_formatted_string(format_type="hex")
            print(f"DEBUG HEX: '{result}'")  # Debug
            
            expect(result).not_to(be_empty)
            expect(result).to(contain("#ff0000 # Rouge"))
            expect(result).to(contain("#00ff00 # Vert"))
            expect(result).to(contain("#0000ff # Bleu"))
        
        with it('formate en raw'):
            result = self.palette.to_formatted_string(format_type="raw")
            print(f"DEBUG RAW: '{result}'")  # Debug
            
            expect(result).not_to(be_empty)
            expect(result).to(contain("255 0 0 Rouge"))
            expect(result).to(contain("0 255 0 Vert"))
            expect(result).to(contain("0 0 0 Bleu"))  # Attendre l'erreur pour debug
        
        with it('formate sans en-tête'):
            result = self.palette.to_formatted_string(format_type="rgb", include_header=False)
            
            expect(result).not_to(be_empty)
            expect(result).not_to(contain("# Palette:"))
            expect(result).to(contain("rgb(255, 0, 0) # Rouge"))
        
        with it('formate sans noms'):
            result = self.palette.to_formatted_string(format_type="hex", include_names=False)
            
            expect(result).not_to(be_empty)
            expect(result).to(contain("#ff0000"))
            expect(result).not_to(contain("# Rouge"))
        
        with it('utilise des séparateurs personnalisés'):
            result = self.palette.to_formatted_string(format_type="hex", separator=" | ")
            
            expect(result).to(contain(" | "))
        
        with it('gère les palettes vides'):
            empty_palette = PixelPalette()
            result = empty_palette.to_formatted_string()
            
            expect(result).to(equal("# Palette vide"))
    
    with context('Export formats'):
        
        with before.each:
            self.palette = PixelPalette()
            self.palette.metadata['name'] = "Ma Palette"
            self.palette.metadata['columns'] = 2
            self.palette.add_color(255, 0, 0, "Rouge")
            self.palette.add_color(0, 255, 0, "Vert")
        
        with it('exporte en format GIMP'):
            result = self.palette.to_gimp_format()
            
            expect(result).to(start_with("GIMP Palette"))
            expect(result).to(contain("Name: Ma Palette"))
            expect(result).to(contain("Columns: 2"))
            expect(result).to(contain("255   0   0\tRouge"))
            expect(result).to(contain("  0 255   0\tVert"))
        
        with it('exporte en liste hex'):
            result = self.palette.to_hex_list()
            
            expect(result).to(equal(["#ff0000", "#00ff00"]))
        
        with it('exporte en tuples RGB'):
            result = self.palette.to_rgb_tuples()
            
            expect(result).to(equal([(255, 0, 0), (0, 255, 0)]))
    
    with context('Propriétés et comportement'):
        
        with it('implémente les propriétés correctement'):
            palette = PixelPalette(source_filename="test.gpl")
            palette.metadata['name'] = "Test"
            palette.add_color(255, 0, 0)
            
            expect(palette.name).to(equal("Test"))
            expect(palette.color_count).to(equal(1))
            expect(palette.is_empty).to(be_false)
            expect(palette.is_valid).to(be_true)
        
        with it('supporte l\'itération'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")
            
            colors = [color for color in palette]
            expect(colors).to(have_length(2))
            expect(colors[0].name).to(equal("Rouge"))
        
        with it('supporte l\'indexation'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")
            
            expect(palette[0].name).to(equal("Rouge"))
            expect(palette[1].name).to(equal("Vert"))
            expect(len(palette)).to(equal(2))
    
    with context('Gestion d\'erreurs'):
        
        with it('gère le contenu invalide'):
            invalid_content = "Ceci n'est pas une palette valide"
            palette = PixelPalette(raw_content=invalid_content)
            
            expect(palette.format_type).to(equal('generic'))
            expect(palette.colors).to(be_empty)  # Aucune couleur parsée
        
        with it('gère les lignes malformées'):
            malformed_content = """GIMP Palette
255 0 Rouge manque une valeur
abc def ghi Pas des nombres
128 128 128 Gris valide
"""
            palette = PixelPalette(raw_content=malformed_content)
            expect(palette.colors).to(have_length(1))  # Seule la ligne valide
            expect(palette.colors[0].name).to(equal("Gris valide"))
        
        with it('trouve la couleur proche sur palette vide lève une erreur'):
            empty_palette = PixelPalette()
            target = PixelColor(255, 0, 0)
            
            def find_closest():
                return empty_palette.find_closest_color(target)
            
            expect(find_closest).to(raise_error(ValueError, "Palette vide"))
