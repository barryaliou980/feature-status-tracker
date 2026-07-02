# Checklist de questions de clarification par type de feature

Ne pose que les questions pertinentes pour la feature en cours — cette liste est un menu, pas un script à réciter intégralement. L'objectif de chaque question est d'aboutir à des **critères d'acceptation écrits, testables**, pas juste de "discuter".

## Questions génériques (presque toujours utiles)

- Quel est le comportement attendu côté utilisateur final, en une phrase ?
- Y a-t-il un cas limite ou une erreur qu'il faut absolument gérer (ex: donnée manquante, timeout, doublon) ?
- Cette feature dépend-elle d'une autre feature du tableau qui doit être terminée avant ?
- Quel est le critère qui permet de dire "c'est fini" (ex: un test précis, un scénario manuel à vérifier) ?

## Si la feature touche l'UI/UX

- Écran ou composant existant à modifier, ou nouvel écran ?
- Comportement responsive/mobile à prévoir ou hors scope ?
- État de chargement / erreur à afficher explicitement ?

## Si la feature touche une API / le backend

- Nouvelle route ou modification d'une route existante ? Quel verbe HTTP et quel payload attendu ?
- Authentification/permissions requises sur cette route ?
- Format de réponse attendu (structure JSON) ?

## Si la feature touche les données / la base

- Migration de schéma nécessaire ? Sur quelle table ?
- Impact sur des données existantes (migration de données, pas juste de schéma) ?
- Contraintes d'unicité, index, ou relations à ajouter ?

## Si la feature touche l'infra / le multi-tenant

- Comportement identique pour tous les tenants ou paramétrable par workspace ?
- Impact sur la routing/domaine custom si applicable ?

## Après les réponses

Toujours reformuler en 2-4 lignes concises et les écrire dans la colonne `Clarifications` du tableau, sous forme de critères d'acceptation actionnables plutôt que de recopier la conversation verbatim. C'est ce texte-là, et uniquement lui, qui servira de spec pendant la Phase 3 — il doit donc être suffisamment précis pour développer sans redemander à l'utilisateur.
