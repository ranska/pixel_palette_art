# Conventions pour les Pull Requests

## Structure du message

Chaque PR doit contenir deux sections, une en francais et une en anglais,
identifiees par les emojis drapeaux en en-tete :

```markdown
## :fr: Resume

Description en francais...

## :gb: Summary

Description in english...
```

## Contenu attendu

### Titre
- Court (< 70 caracteres)
- En francais, descriptif de l'objectif principal
- Exemples :
  - `Fix imports nodes palette/ et text_size police`
  - `Ajout numerotation workflows et CI`

### Corps (chaque section FR et EN)
- **Quoi** : lister les changements concrets
- **Pourquoi** : expliquer le probleme resolu ou la fonctionnalite ajoutee
- **Comment** : details techniques si pertinent (choix d'architecture, trade-offs)
- **Tests** : comment verifier que ca marche

### Checklist avant de soumettre
- [ ] Tests mamba au vert (`mamba spec/ --enable-coverage --format=documentation`)
- [ ] Pas de secrets ou fichiers temporaires dans le diff
- [ ] Message de commit propre (pas de reference IA)
- [ ] Branche a jour avec develop

## Exemple complet

```markdown
## :fr: Resume

- Correction du chargement des nodes palette/ qui utilisaient importlib
  au lieu d'imports relatifs, causant des echecs isinstance()
- Ajout de PreviewImage dans tous les workflows de test

## :gb: Summary

- Fixed palette node loading that used importlib instead of relative
  imports, causing isinstance() failures at runtime
- Added PreviewImage nodes to all test workflows
```
