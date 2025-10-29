# 🏢 Epic Events CRM – Backend Sécurisé (CLI)

## Description

**Epic Events CRM** est une application **de gestion client (CRM)** développée pour l’entreprise **Epic Events**, qui organise des événements pour ses clients.  
Ce CRM permet de **centraliser les données des clients, contrats et événements**, tout en **respectant le principe du moindre privilège** selon le rôle du collaborateur.

L’application fonctionne **en ligne de commande (CLI)**, avec une architecture modulaire et une gestion des permissions robuste.

---

## Fonctionnalités principales

### Authentification (JWT)

- Connexion sécurisée avec token **JWT** (via la commande `auth login`).
- Le token est stocké localement dans un fichier `.token`.
- Déconnexion avec suppression du token (`auth logout`).

### Gestion des rôles et permissions

Trois rôles existent dans le système :
| Rôle | Accès principal |
|------|------------------|
| **Gestion** | Admin général – peut créer, lire, modifier, supprimer collaborateurs, contrats, clients, événements et rôles. |
| **Commercial** | Peut créer et gérer ses propres clients, contrats et événements. |
| **Support** | Peut lire et modifier uniquement les événements dont il est responsable. |

Les permissions sont définies dans `permissions.py`.

---

## Structure des données

### **Collaborateur**

- `id`, `nom`, `email`, `mot_de_passe (hashé)`
- `role_id` (clé étrangère vers `Role`)

### **Client**

- `id`, `nom_complet`, `email`, `telephone`, `entreprise`
- `date_creation`, `derniere_mise_a_jour`
- `contact_commercial_id` (collaborateur référent)

### **Contrat**

- `id`, `client_id`, `contact_commercial_id`
- `montant_total`, `montant_restant`
- `statut_contrat` (signé ou non)
- `date_creation`

### **Événement**

- `id`, `contrat_id`, `client_id`
- `date_debut`, `date_fin`, `lieu`
- `participants`, `attendues`
- `notes`, `support_contact_id`

---

## Technologies utilisées

| Composant                 | Technologie              |
| ------------------------- | ------------------------ |
| Langage principal         | Python 3.9+              |
| ORM                       | SQLAlchemy               |
| Interface CLI             | Typer                    |
| Journalisation            | Sentry                   |
| Sécurité                  | JWT + werkzeug (hashage) |
| Affichage console         | Rich                     |
| Variables d’environnement | python-dotenv            |

---

## Sécurité

- **JWT** pour l’authentification et la session.
- **Hashage des mots de passe** avec `werkzeug.security`.
- **Validation stricte** des emails, montants, dates et relations.
- **Principe du moindre privilège** appliqué via `DEFAULT_PERMISSIONS`.
- **Journalisation des erreurs et actions critiques** avec Sentry.
- **Protection contre les injections SQL** grâce à SQLAlchemy.

---

## Commandes principales (CLI)

CLI global du CRM

**auth** Commandes pour l'authentification
**db** Commandes pour gérer les données

### Authentification

**login** Commande CLI pour se connecter et obtenir un token JWT.
**logout** Déconnecte l'utilisateur en supprimant le token local.

```bash
python -m app.cli auth login --email "user@example.com" --mot-de-passe "MotDePasse"
python -m app.cli auth logout
```

### Gérer les données

#### Lecture

**read-collaborateurs** Affiche tous les collaborateurs enregistrés dans la base de données.
**read-clients** Affiche tous les clients enregistrés dans la base de données.
**read-contrats** Affiche tous les contrats enregistrés dans la base de données.
**read-evenements** Affiche tous les événements enregistrés dans la base de données.

```bash
python -m app.cli db read-clients
python -m app.cli db read-contrats
python -m app.cli db read-evenements
python -m app.cli db read-collaborateurs
python -m app.cli db read-roles
```

#### Ajout

**add-client** Ajoute un nouveau client dans la base de données.
**add-collaborateur** Ajoute un collaborateur avec mot de passe haché.
**add-contrat** Ajoute un nouveau contrat dans la base de données.
**add-evenement** Ajoute un nouvel événement dans la base de données.
**add-role** Ajoute un nouveau rôle dans la base de données.

```bash
python -m app.cli db add-client "Marie Dupont" marie.dupont@email.com "0601020304" --entreprise "Dupont Consulting"
python -m app.cli db add-collaborateur "Paul Martin" paul.martin@epic.com --role-id 2
python -m app.cli db add-contrat 5000 2000 False 1
python -m app.cli db add-evenement "2025-12-01 10:00" "2025-12-01 18:00" "Paris" 100 120 --notes "Journée annuelle" --contrat-id 3
python -m app.cli db add-role "administrateur"
```

#### Mise à jour

**update-client** Modifie un client existant dans la base de données.
**update-collaborateur** Modifie un collaborateur existant dans la base de données.
**update-contrat** Modifie un contrat existant dans la base de données.
**update-evenement** Modifie un événement existant dans la base de données.
**update-role** Modifie un rôle existant dans la base de données.

```bash
python -m app.cli db update-client 1 --telephone "0611223344" --entreprise "Nouvelle Société"
python -m app.cli db update-collaborateur 2 --nom "Paul M. Martin" --email "paul.martin@newmail.com"
python -m app.cli db update-contrat 3 --montant-restant 0 --statut-contrat True
python -m app.cli db update-evenement 4 --lieu "Lyon" --participants 80 --notes "Changement de lieu"
python -m app.cli db update-role 2 --role "support technique"
```

#### Suppression

**delete-client** Supprime un client de la base de données.
**delete-collaborateur** Supprime un collaborateur de la base de données.
**delete-contrat** Supprime un contrat de la base de données.
**delete-evenement** Supprime un événement de la base de données.
**delete-role** Supprime un rôle de la base de données.

```bash
python -m app.cli db delete-client 1
python -m app.cli db delete-collaborateur 2
python -m app.cli db delete-contrat 3
python -m app.cli db delete-evenement 4
python -m app.cli db delete-role 5
```

#### Filtrage

**filter-evenements** Filtre les événements selon : - --sans-support : événements sans support associé - (automatique) support : uniquement ses propres événements
**filter-contrats** Filtre les contrats selon le statut. Exemple : - --non-signe : contrats non signés - --non-payes : contrats avec montant restant > 0

Événements sans support :

```bash
python -m app.cli db filter-evenements --sans-support
```

Si tu es un collaborateur avec le rôle support, la commande sans argument te montre tes propres événements :

```bash
python -m app.cli db filter-evenements
```

Filtrer les contrats

Contrats non signés :

```bash
python -m app.cli db filter-contrats --non-signe
```

Contrats non payés (montant restant > 0) :

```bash
python -m app.cli db filter-contrats --non-payes
```

Contrats non signés et non payés :

```bash
python -m app.cli db filter-contrats --non-signe --non-payes
```

## Installation

### Cloner le dépôt

```bash
git clone https://github.com/Caroleloop/oc_python_12_developpez_une_architecture_back-end_securisee.git
cd epic-events-crm
```

### Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate # (ou .venv\\Scripts\\activate sous Windows)
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Configurer les variables d’environnement

Créer un fichier .env à la racine :

```bash
SECRET_KEY=ta_clé_ultra_secrète
DATABASE_URL=postgresql://user:password@localhost/epic_events
SENTRY_DSN=https://ton_dsn_sentry
```

### Initialiser la base

```bash
python -m app db init
```

## Règles métier

| Action                                  | Rôle autorisé        | Conditions                                     |
| --------------------------------------- | -------------------- | ---------------------------------------------- |
| Créer un client                         | Commercial           | Devient automatiquement son contact commercial |
| Modifier un client                      | Commercial           | Doit être le commercial associé                |
| Créer un contrat                        | Gestion              | —                                              |
| Modifier un contrat                     | Gestion / Commercial | Commercial uniquement pour ses clients         |
| Créer un événement                      | Commercial           | Seulement si le contrat est signé              |
| Modifier un événement                   | Gestion / Support    | Support seulement pour ses propres événements  |
| Créer/supprimer collaborateurs ou rôles | Gestion              | —                                              |

## Journalisation & Observabilité

- Tous les événements critiques (connexion, création de contrat, erreurs…) sont envoyés à Sentry.

- Les actions de création et modification sont loggées avec des messages formatés.

- L’affichage est enrichi avec Rich pour une lisibilité optimale.
