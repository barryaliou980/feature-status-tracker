---
name: feature-status-tracker
description: >
  Pilote un cycle complet de dev à partir d'un tableau Markdown de features (| Feature |
  Description | Statut | ...). Utilise ce skill dès qu'un tableau de fonctionnalités à
  développer est fourni/référencé, ou qu'on parle de "feature status", "backlog", "roadmap
  à implémenter", "clarifier puis développer seul chaque feature". Deux phases obligatoires —
  1) clarification interactive feature par feature, aucun code avant que TOUT le tableau soit
  clarifié ; 2) exécution autonome : une feature à la fois, branche Git dédiée, dev, tests,
  commit, PR locale vers la branche principale, statut "done", puis enchaîne seul sur la
  suivante jusqu'à la fin du tableau. S'appuie sur le framework Superpowers (obra/superpowers)
  pour chaque étape technique (git worktrees, TDD, revue de code, clôture de branche) —
  vérifie sa présence avant la phase 2. Se déclenche même sans le mot "skill" : coller un
  tableau de features avec une colonne statut suffit.
---

# Feature Status Tracker

Pilote de bout en bout : tableau de features → clarification → développement autonome branche par branche, en s'appuyant sur les skills Superpowers pour chaque étape technique.

## Vue d'ensemble du workflow

```
Phase 0 : Vérification des prérequis (Superpowers, repo git propre)
Phase 1 : Parsing du tableau + Clarification (interactif, feature par feature)
Phase 2 : Portail de confirmation ("GO" de l'utilisateur)
Phase 3 : Boucle autonome (1 feature = 1 branche = 1 PR = 1 ligne "done")
Phase 4 : Rapport final
```

**Règle d'or : ne jamais commencer à coder tant que toutes les features ne sont pas clarifiées.** La clarification et le développement sont deux phases strictement séparées.

---

## Phase 0 — Prérequis

1. Vérifier qu'on est dans un dépôt git propre : `git status`. Si des changements non commités traînent, le signaler à l'utilisateur avant de continuer.
2. Vérifier la présence de Superpowers : chercher `.claude/plugins` ou un dossier de skills contenant `using-git-worktrees`, `test-driven-development`, `requesting-code-review`, `finishing-a-development-branch` (via la commande de recherche de skills disponible, ou `find` sur `~/.claude`).
   - **Si Superpowers est présent** : ce skill délègue explicitement à ces skills Superpowers pendant la Phase 3 (voir `references/superpowers-integration.md`). Ne pas réimplémenter en parallèle une logique de TDD ou de gestion de worktree — invoquer le skill Superpowers correspondant.
   - **Si Superpowers est absent** : le signaler une fois à l'utilisateur ("Superpowers n'est pas détecté, je vais utiliser un workflow git/TDD manuel équivalent") puis continuer avec le fallback décrit dans `references/superpowers-integration.md`. Ne pas bloquer le workflow pour autant.
3. Identifier ou demander le chemin du fichier tableau (ex: `FEATURES.md`, `roadmap.md`) s'il n'est pas déjà fourni dans la conversation.

## Phase 1 — Parser le tableau et clarifier

### Format attendu du tableau

Voir `references/table-format.md` pour le détail complet. En résumé, colonnes minimales :

| Feature | Description | Statut | Clarifications | Branche | PR |
|---|---|---|---|---|---|

- Si le tableau fourni n'a pas les colonnes `Clarifications`, `Branche`, `PR`, les ajouter toi-même en éditant le fichier (elles servent de mémoire persistante entre les sessions).
- Statuts possibles : `à faire`, `clarifiée`, `en cours`, `done`, `bloquée`.

### Boucle de clarification (une feature à la fois)

Pour chaque ligne dont le statut est `à faire` (pas encore clarifiée) :

1. Annoncer brièvement quelle feature tu traites (nom + description existante).
2. Poser des questions ciblées pour lever les ambiguïtés — voir la checklist dans `references/clarification-questions.md`. Ne pas tout demander mécaniquement : ne poser que les questions pertinentes pour CETTE feature (une feature UI n'a pas les mêmes questions qu'une feature API interne).
3. Utiliser le format de questions à choix (via l'outil de questions à l'utilisateur si disponible dans l'environnement, sinon des questions numérotées claires) pour aller vite — mais rester ouvert à des réponses en texte libre.
4. Une fois les réponses obtenues, résumer en 2-4 lignes les critères d'acceptation retenus et les écrire dans la colonne `Clarifications` de la ligne correspondante (fichier Markdown mis à jour directement).
5. Passer le statut de la ligne à `clarifiée`.
6. Passer à la feature suivante **sans t'arrêter pour valider** — seule la fin de la clarification de TOUTES les features déclenche un point d'arrêt (Phase 2).

Si une feature est déjà marquée `done` ou `bloquée` en entrant dans le skill, la sauter (ne pas re-clarifier, ne pas re-développer).

## Phase 2 — Portail de confirmation

Une fois toutes les lignes passées à `clarifiée` (ou `done`/`bloquée` préexistantes) :

1. Afficher un résumé compact du tableau final (feature → résumé des critères d'acceptation en une ligne).
2. Demander explicitement confirmation avant de lancer le développement autonome, par exemple : *"Toutes les features sont clarifiées. Je peux démarrer le développement autonome (1 branche par feature, PR locale à la fin de chacune). Je te laisse travailler seul jusqu'à la fin du tableau — confirme pour que je démarre."*
3. Ne jamais démarrer la Phase 3 sans ce feu vert explicite.

## Phase 3 — Boucle de développement autonome

Une fois le feu vert donné, **ne plus repasser par l'utilisateur entre les features** (sauf blocage réel — voir gestion des erreurs). Pour chaque feature dans l'ordre du tableau dont le statut est `clarifiée` :

1. **Marquer** la ligne `en cours` dans le fichier tableau.
2. **Créer la branche** dédiée à cette feature. Nom de branche : `feature/<slug-de-la-feature>` (kebab-case, sans accents). Utiliser le skill Superpowers `using-git-worktrees` s'il est disponible pour isoler le workspace ; sinon `git checkout -b feature/<slug>` depuis la branche principale locale à jour.
3. **Développer** en t'appuyant sur les critères d'acceptation de la colonne `Clarifications`. Utiliser le skill Superpowers `test-driven-development` (cycle red-green-refactor) s'il est disponible ; sinon appliquer manuellement : test qui échoue → code minimal → test qui passe → refactor.
4. **Faire relire ton propre travail** avec le skill Superpowers `requesting-code-review` s'il est disponible avant de commit, pour attraper les problèmes évidents.
5. **Commit** avec un message conventionnel (`feat: <résumé de la feature>`, corps optionnel listant les critères d'acceptation couverts).
6. **Clôturer la branche** : utiliser le skill Superpowers `finishing-a-development-branch` s'il est disponible pour ouvrir la PR ; sinon `git push -u origin feature/<slug>` puis `gh pr create --base <branche-principale-locale> --fill` (si `gh` est installé) ou, à défaut, indiquer clairement dans le rapport que la branche est prête et poussée mais qu'il n'a pas pu ouvrir la PR automatiquement. **Ne jamais merger automatiquement** — la PR reste ouverte pour revue humaine.
7. **Mettre à jour le tableau** : statut → `done`, remplir les colonnes `Branche` et `PR` (lien ou identifiant).
8. **Revenir à la branche principale locale** avant de passer à la feature suivante (`git checkout <branche-principale>`).
9. Passer automatiquement à la feature suivante avec statut `clarifiée`, sans attendre de confirmation.

### Gestion des erreurs / blocages

- Si une feature ne peut pas être terminée (dépendance manquante, ambiguïté technique découverte en cours de dev, tests impossibles à faire passer après plusieurs tentatives raisonnables) : marquer la ligne `bloquée`, écrire la raison dans `Clarifications`, committer le travail partiel sur sa branche dédiée si pertinent, puis **continuer avec la feature suivante** plutôt que d'arrêter tout le run.
- Ne jamais laisser le dépôt sur une branche de feature à la fin d'un cycle — toujours revenir à la branche principale locale entre deux features.

## Phase 4 — Rapport final

Quand toutes les lignes sont `done` ou `bloquée`, produire un résumé texte (pas de widget, format structuré simple) :
- Nombre de features terminées / bloquées.
- Liste des branches créées et PR ouvertes (avec lien si disponible).
- Liste des features bloquées avec la raison, pour que l'utilisateur tranche.

---

## Fichiers de référence

- `references/table-format.md` — Format exact du tableau, exemple complet, règles de parsing.
- `references/clarification-questions.md` — Checklist de questions par type de feature (UI, API, données, infra).
- `references/superpowers-integration.md` — Mapping précis entre chaque étape de ce skill et le skill Superpowers correspondant, + fallback si Superpowers n'est pas installé.
