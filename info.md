# Présentation Détaillée du Projet d'Échecs en Python

## 1. Architecture Globale et Technologies
- **Langage de Programmation :** Python.
- **Framework Principal :** FastAPI.
- **Gestion de Base de Données :** Strapi.
- **Modélisation des Données :** Pydantic.

## 2. Arborescence et Détails des Fichiers

### Dossier Racine
- `main.py` : Point d'entrée de l'application, initialise et lance le serveur FastAPI.

### Dossier `api`
- `games_api.py` : API pour la gestion des jeux. Contient des routes pour créer, récupérer et gérer les parties d'échecs.
- `players_api.py` : API pour la gestion des joueurs. Inclut des routes pour l'inscription des joueurs et la récupération de leurs informations.

### Dossier `chess_app`
- `chess_engine.py` : Contient la logique du moteur d'échecs, gérant le plateau et les mouvements.

### Dossier `custom_errors`
- `custom_errors.py` : Définit des exceptions personnalisées pour une meilleure gestion des erreurs dans l'application.

### Dossier `database_services`
- `strapi_services.py` : Fournit des fonctions pour interagir avec la base de données Strapi, comme la récupération et le stockage des données des joueurs et des jeux.

### Dossier `routes`
- `__init__.py` : Fichier d'initialisation pour le module de routes.

### Dossier `schemas`
- `chess_schemas.py` : Définit des schémas Pydantic pour la validation des données entrantes dans les APIs.

### Dossier `services`
- `game_services.py` : Services liés à la logique des jeux d'échecs.
- `player_services.py` : Services pour la gestion des informations des joueurs.

### Dossier `strapi_db`
- `config/database.js` : Configuration de la base de données Strapi.
- Dossiers `src/api/game` et `src/api/player` : Contiennent des fichiers pour la définition, le contrôle, les routes et les services des entités de jeu et de joueur dans Strapi.

## 3. Fonctionnalités Clés
- Création et gestion de parties d'échecs en ligne.
- Inscription et gestion des joueurs.
- Interaction avec une base de données.
- Validation des données avec Pydantic.

## 4. Objectifs et But du Projet
- Fournir une plateforme en ligne pour jouer aux échecs.
- Utiliser FastAPI et Strapi pour une gestion efficace des données.

## 5. Futurs Développements Potentiels
- Intégration avec des APIs externes.
- Ajout de fonctionnalités d'apprentissage automatique.

## Liens Utiles
- [Lien vers le dépôt GitHub](https://github.com/mpruvot/python_chess_app/tree/strapi_init)
