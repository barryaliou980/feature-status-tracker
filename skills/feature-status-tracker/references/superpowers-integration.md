# Intégration avec Superpowers (obra/superpowers)

Ce skill est conçu pour s'exécuter dans Claude Code avec le plugin Superpowers installé. Superpowers fournit des skills spécialisés pour chaque étape technique du développement — ce skill orchestre, Superpowers exécute.

## Vérifier la présence de Superpowers

En début de Phase 0, chercher les skills Superpowers disponibles (par ex. lister les skills accessibles, ou chercher un dossier de plugins contenant leurs noms). Les skills Superpowers pertinents pour ce workflow :

- `using-git-worktrees`
- `test-driven-development`
- `requesting-code-review`
- `finishing-a-development-branch`
- `brainstorming` (optionnel, voir note plus bas)

## Mapping étape par étape

| Étape de ce skill | Skill Superpowers à invoquer | Ce que ça fait |
|---|---|---|
| Création de branche (Phase 3, étape 2) | `using-git-worktrees` | Crée un workspace isolé sur une nouvelle branche, lance le setup du projet, vérifie une baseline de tests propre avant de commencer à coder. |
| Développement (Phase 3, étape 3) | `test-driven-development` | Impose le cycle red-green-refactor : écrire un test qui échoue, code minimal pour le faire passer, refactor, commit. |
| Auto-relecture avant commit (Phase 3, étape 4) | `requesting-code-review` | Fait relire le travail contre les critères d'acceptation et la qualité du code, avant de considérer la feature terminée. |
| Clôture de branche + PR (Phase 3, étape 6) | `finishing-a-development-branch` | Vérifie les tests, propose merge / créer une PR / continuer / abandonner. **Toujours choisir l'option "créer une PR" et jamais "merger"** conformément à la consigne de l'utilisateur (PR locale vers la branche principale, pas de merge automatique). |

### Note sur `brainstorming`

Superpowers inclut un skill `brainstorming` qui affine une idée floue par des questions avant tout code — c'est conceptuellement proche de la Phase 1 de ce skill-ci. Ne pas invoquer les deux en double sur la même feature : la Phase 1 de `feature-status-tracker` remplace `brainstorming` pour ce workflow précis, puisque la clarification part déjà d'un tableau structuré. Si `brainstorming` s'active spontanément pendant la Phase 3 (ex: ambiguïté redécouverte en cours de dev), le laisser faire ponctuellement plutôt que de le bloquer — mais ça doit rester l'exception, pas la norme, sinon la boucle autonome perd son autonomie.

## Fallback si Superpowers n'est pas installé

Ne jamais bloquer le workflow si Superpowers est absent — appliquer manuellement l'équivalent :

1. **Branche** : `git checkout -b feature/<slug>` depuis la branche principale locale à jour (`git pull` d'abord si un remote existe).
2. **TDD manuel** : écrire un test qui échoue, coder le minimum pour le faire passer, refactorer, puis passer à l'acceptance criteria suivant.
3. **Auto-relecture** : avant de commit, relire son propre diff (`git diff`) contre la colonne `Clarifications` et signaler explicitement si un point n'est pas couvert plutôt que de commit silencieusement.
4. **Clôture** : `git push -u origin feature/<slug>`, puis `gh pr create --base <branche-principale> --fill` si le CLI `gh` est disponible et authentifié. Si `gh` n'est pas disponible, ne pas essayer de deviner une URL — indiquer clairement dans le rapport final que la branche est poussée mais que la PR doit être ouverte manuellement, avec la commande exacte à lancer.

Dans les deux cas (avec ou sans Superpowers), la règle métier de l'utilisateur reste fixe : **jamais de merge automatique**, toujours une PR ouverte contre la branche principale locale, en attente de revue humaine.
