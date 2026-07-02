# Format du tableau de features

## Colonnes minimales attendues en entrée

| Feature | Description | Statut |
|---|---|---|
| Auth OAuth multi-compte | Permettre de connecter plusieurs comptes sociaux par workspace | à faire |
| Export PDF du dashboard | Export du KPI dashboard en PDF | à faire |

Si l'utilisateur fournit un tableau avec seulement ces 3 colonnes (ou même juste `Feature` + `Statut`), le skill doit **enrichir le fichier lui-même** en ajoutant les colonnes manquantes ci-dessous, en éditant le fichier Markdown directement (ne pas juste les garder en mémoire — elles doivent survivre à une interruption/reprise de session).

## Colonnes complètes après enrichissement

| Feature | Description | Statut | Clarifications | Branche | PR |
|---|---|---|---|---|---|
| Auth OAuth multi-compte | Permettre de connecter plusieurs comptes sociaux par workspace | done | Scope: TikTok+Instagram uniquement pour v1. Un compte = un token, refresh auto. Erreur si token expiré → notif in-app. | feature/auth-oauth-multi-compte | #42 |
| Export PDF du dashboard | Export du KPI dashboard en PDF | clarifiée | Format A4 portrait, logo workspace en header, données des 30 derniers jours uniquement | | |

## Statuts valides

- `à faire` — pas encore clarifiée, pas encore développée.
- `clarifiée` — questions répondues, critères d'acceptation écrits, prête à être développée en Phase 3.
- `en cours` — en cours de développement (état transitoire pendant la Phase 3, ne devrait jamais rester dans cet état à la fin d'un run sauf interruption).
- `done` — branche créée, code écrit et testé, PR ouverte.
- `bloquée` — le développement a rencontré un obstacle réel ; voir la colonne `Clarifications` pour la raison.

## Règles de parsing

- Le nom de la colonne peut varier légèrement (`Statut`/`Status`, `Feature`/`Fonctionnalité`) — matcher de façon tolérante sur la position/le sens plutôt que sur le nom exact, mais **conserver le nom de colonne original** du fichier de l'utilisateur en le réécrivant.
- Une ligne sans valeur dans `Statut` est traitée comme `à faire`.
- Le slug de branche (colonne `Branche`) doit être dérivé du nom de la feature : minuscules, sans accents, espaces → tirets, pas de caractères spéciaux. Exemple : "Export PDF du dashboard" → `feature/export-pdf-du-dashboard`.
- Toujours réécrire le fichier tableau complet à chaque mise à jour de statut (pas d'append en dehors du tableau) pour qu'il reste la source de vérité unique, lisible en un coup d'œil.
