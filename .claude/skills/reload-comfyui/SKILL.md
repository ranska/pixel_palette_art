---
name: reload-comfyui
description: Redemarrer ComfyUI et recharger un workflow dans le navigateur
disable-model-invocation: true
argument-hint: "[workflow_name]"
---

# Reload ComfyUI + workflow

Redemarrer le serveur ComfyUI et recharger un workflow de test dans le navigateur Playwright.

Argument optionnel : nom du workflow (sans extension), ex: `test_sort_palette`.
Si pas d'argument, recharger le dernier workflow visible dans l'onglet ComfyUI.

## Etapes

### 1. Trouver le pane tmux ComfyUI

```bash
tmux list-panes -a -F "#{session_name}:#{window_index}.#{pane_index} #{pane_current_command}"
```

Chercher le pane dont la commande est `Python` ou `python` dans la session `comfyui`.
Le pane attendu est `comfyui:0.0`.

### 2. Arreter ComfyUI

Envoyer Ctrl-C au pane et attendre l'arret :

```bash
tmux send-keys -t comfyui:0.0 C-c
sleep 2
```

Verifier dans la capture du pane que le serveur est bien arrete (`Stopped server` ou prompt shell visible).

### 3. Relancer ComfyUI

```bash
tmux send-keys -t comfyui:0.0 'python main.py --force-fp16' Enter
```

Attendre que le serveur soit pret en verifiant les logs (~5s) :

```bash
sleep 5
tmux capture-pane -t comfyui:0.0 -p | tail -5
```

Confirmer que `To see the GUI go to: http://127.0.0.1:8188` apparait.
Si pas pret, attendre encore 3s et reverifier.

### 4. Recharger le workflow dans le navigateur

- Naviguer vers `http://127.0.0.1:8188`
- Attendre 3 secondes que l'UI se charge completement
- Si un argument `$ARGUMENTS` est fourni :
  - Ouvrir le menu "Flux de travail" > "Ouvrir"
  - Uploader le fichier : `workflows/test/$ARGUMENTS.json`
- Fermer toute alerte ou dialog qui apparait (aux_id, missing nodes, etc.)
- Prendre un screenshot pour confirmer le chargement

### 5. Confirmer

Afficher un resume :
- ComfyUI redemarre OK/KO
- Workflow charge : nom du workflow
- Screenshot pris
