# feature-status-tracker

Skill Claude Code qui transforme un simple tableau Markdown de fonctionnalités en pipeline de développement autonome : Claude clarifie chaque feature avec toi, puis développe seul, une branche Git par feature, jusqu'à ce que tout le tableau soit terminé.

Conçu pour s'appuyer sur [Superpowers](https://github.com/obra/superpowers) (git worktrees, TDD, revue de code, clôture de branche) — avec un fallback manuel si Superpowers n'est pas installé.

---

## Qu'est-ce que ça fait ?

Tu donnes à Claude un fichier Markdown du genre :

```markdown
| Feature | Description | Statut |
|---|---|---|
| Auth OAuth multi-compte | Connecter plusieurs comptes sociaux par workspace | à faire |
| Export PDF du dashboard | Export du KPI dashboard en PDF | à faire |
```

Le skill se déroule ensuite en 4 phases, dans cet ordre strict :

1. **Clarification** — Claude parcourt chaque ligne `à faire` et te pose des questions ciblées (scope, cas limites, dépendances, critère de "c'est fini"). Les réponses sont écrites directement dans le fichier, dans une colonne `Clarifications`. **Aucune ligne de code n'est écrite pendant cette phase.**
2. **Portail de confirmation** — une fois tout le tableau clarifié, Claude te fait un résumé et attend ton feu vert explicite avant de commencer à coder.
3. **Développement autonome** — pour chaque feature, dans l'ordre du tableau : création d'une branche `feature/<slug>`, développement (TDD si Superpowers est là), auto-relecture, commit, push, **Pull Request locale vers ta branche principale (jamais de merge automatique)**, puis mise à jour du statut à `done` dans le tableau. Claude enchaîne seul sur la feature suivante sans repasser par toi.
4. **Rapport final** — résumé des branches/PR créées, et liste des features bloquées (le cas échéant) avec la raison, pour que tu tranches.

Si une feature bloque en cours de route (dépendance manquante, ambiguïté technique découverte trop tard...), elle est marquée `bloquée` avec la raison, et Claude continue sur la suivante plutôt que d'arrêter tout le run.

### Ce que ce skill ne fait pas

- Il ne merge jamais automatiquement une branche dans la branche principale — c'est toujours une PR ouverte, en attente de ta revue.
- Il ne code jamais avant que la clarification de **toutes** les features du tableau soit terminée.
- Il n'invente pas de critères d'acceptation : si une réponse manque pour développer correctement, il te la demande plutôt que de supposer.

---

## Comment l'installer

Le skill est un simple dossier avec un `SKILL.md` — pas de dépendance à installer.

### Option A — Skill perso, disponible dans tous tes projets

```bash
git clone <url-de-ce-repo> ~/.claude/skills/feature-status-tracker
```

### Option B — Skill limité à un seul projet

Clone-le directement dans `.claude/skills/` à la racine du repo concerné (Viraflow, Guinuty, SilyTrack...) plutôt que dans `~/.claude/skills/` :

```bash
cd /chemin/vers/ton-projet
git clone <url-de-ce-repo> .claude/skills/feature-status-tracker
```

### Option C — Copier manuellement (sans git)

Télécharge/dézippe le contenu du repo, puis copie le dossier `feature-status-tracker/` tel quel dans `~/.claude/skills/` ou `.claude/skills/`. Le `SKILL.md` doit être **directement** à l'intérieur du dossier (`~/.claude/skills/feature-status-tracker/SKILL.md`), pas plus profond.

### Après installation

- Si tu ajoutes le skill pendant une session Claude Code déjà ouverte, il est pris en compte immédiatement (pas besoin de relancer), sauf si tu viens de créer le dossier `skills/` lui-même pour la première fois — dans ce cas, redémarre la session.
- Recommandé mais optionnel : installe aussi [Superpowers](https://github.com/obra/superpowers) (`/plugin marketplace add obra/superpowers-marketplace` puis `/plugin install superpowers@superpowers-marketplace`). Le skill fonctionne sans, mais avec Superpowers il délègue automatiquement la gestion des worktrees, le TDD, la revue de code et la clôture de branche à des skills spécialisés et éprouvés.

---

## Comment l'utiliser

### 1. Prépare ton tableau

Crée un fichier Markdown (ex: `FEATURES.md`) à la racine de ton projet avec au minimum les colonnes `Feature`, `Description`, `Statut`. Le skill enrichit lui-même le fichier avec les colonnes `Clarifications`, `Branche`, `PR` si elles n'existent pas encore.

### 2. Lance la clarification

Dans Claude Code, ouvre une session dans ton projet et dis simplement quelque chose comme :

> Voici mon tableau de features dans FEATURES.md, peux-tu clarifier chaque ligne avec moi puis les développer une par une ?

Claude va détecter le skill automatiquement (pas besoin de le nommer explicitement) et démarrer la boucle de clarification, feature par feature.

### 3. Réponds aux questions

Claude te posera des questions adaptées à chaque feature (UI, API, données, infra...). Réponds normalement — pas besoin de format particulier.

### 4. Donne le feu vert

Une fois toutes les features clarifiées, Claude te présente un résumé et attend une confirmation explicite, du genre :

> Toutes les features sont clarifiées. Je peux démarrer le développement autonome — confirme pour que je commence.

Réponds simplement "go", "vas-y", ou équivalent.

### 5. Laisse-le travailler

Claude enchaîne seul : branche → dev → tests → commit → PR → `done` → feature suivante, jusqu'à la fin du tableau. Tu peux revenir vérifier l'avancement en consultant directement le fichier `FEATURES.md` (colonne `Statut`) ou tes branches/PR sur GitHub.

### 6. Reprendre une session interrompue

Le fichier tableau est la source de vérité persistante. Si tu fermes Claude Code en plein milieu, tu peux relancer une nouvelle session plus tard avec le même prompt — les features déjà `done` ou `clarifiée` ne sont pas re-traitées depuis le début, seules celles encore `à faire` (ou restées `en cours` à cause d'une interruption) reprennent.

---

## Structure du skill

```
feature-status-tracker/
├── SKILL.md                              # Instructions principales (les 4 phases)
├── references/
│   ├── table-format.md                   # Format exact du tableau, colonnes, statuts
│   ├── clarification-questions.md        # Checklist de questions par type de feature
│   └── superpowers-integration.md        # Mapping vers les skills Superpowers + fallback manuel
└── README.md                             # Ce fichier
```

## Licence

MIT — libre d'utilisation, de modification et de partage.
