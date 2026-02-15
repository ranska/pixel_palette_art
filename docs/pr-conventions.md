# Conventions pour les Pull Requests

## Git Flow

### Workflow obligatoire

Toutes les PR doivent cibler **develop**. Jamais master directement.

```bash
# 1. Partir de develop a jour
git checkout develop
git pull origin develop

# 2. Creer une branche feature
git checkout -b feature/<nom-descriptif>

# 3. Travailler, commiter
# ... commits ...

# 4. Pousser la branche
git push -u origin feature/<nom-descriptif>

# 5. Creer la PR vers develop
gh pr create --base develop --title "..."

# 6. Apres merge, nettoyer
git checkout develop
git pull origin develop
git branch -d feature/<nom-descriptif>
```

### Releases

Les releases se font en mergeant develop → master et en taguant :

```bash
git checkout master
git merge develop
git tag v0.x.x
git push origin master --tags
```

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
- [ ] Branche feature creee depuis develop a jour
- [ ] PR cible develop (pas master)

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
