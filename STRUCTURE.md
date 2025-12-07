# 📁 Structure du Projet - Mon Cacao

Ce document décrit la structure complète du projet pour faciliter la navigation et la compréhension.

## 📂 Arborescence Complète

```
mon-cacao/
│
├── 📄 README.md                    # Documentation principale
├── 📄 QUICKSTART.md                # Guide de démarrage rapide
├── 📄 DEPLOYMENT.md                # Guide de déploiement
├── 📄 STRUCTURE.md                 # Ce fichier
├── 📄 LICENSE                      # Licence du projet
├── 📄 requirements.txt             # Dépendances Python
├── 📄 .gitignore                   # Fichiers ignorés par Git
│
├── 📂 backend/                     # Code backend Python
│   ├── api_server.py              # Serveur Flask principal
│   ├── cacao1.py                   # Logique métier principale
│   ├── cacao1_backup.py           # Backup de la logique métier
│   ├── auth_system.py             # Système d'authentification
│   ├── login_interface.py         # Interface de connexion
│   ├── train_model.py             # Script d'entraînement du modèle
│   ├── model_productivite_xgb.pkl # Modèle XGBoost entraîné
│   └── data.sqlite                # Base de données SQLite
│
├── 📂 frontend/                    # Interface utilisateur
│   ├── 📄 index.html              # Page d'accueil / sélection type utilisateur
│   ├── 📄 user-type-selection.html # Sélection du type d'utilisateur
│   │
│   ├── 📄 Pages Producteur:
│   ├── 📄 prediction.html         # Prédictions IA
│   ├── 📄 score-ecologique.html   # Score écologique
│   ├── 📄 analyse.html            # Analyses détaillées
│   ├── 📄 soumettre.html          # Soumission de données
│   ├── 📄 historique.html         # Historique des données
│   ├── 📄 assistant.html          # Assistant IA
│   ├── 📄 conseils.html           # Conseils personnalisés
│   ├── 📄 revenue.html            # Analyse des revenus
│   ├── 📄 production.html         # Suivi de production
│   ├── 📄 revenus.html            # Gestion des revenus
│   │
│   ├── 📄 Pages Professionnel:
│   ├── 📄 dashboard-professionnel.html # Dashboard professionnel
│   ├── 📄 producteur-details.html      # Détails d'un producteur
│   │
│   ├── 📄 dashboard.html          # Ancien dashboard (legacy)
│   │
│   ├── 📂 css/                    # Styles CSS
│   │   ├── style.css              # Styles principaux (le plus important)
│   │   ├── modern-banner.css      # Styles de bannière
│   │   ├── dashboard.css          # Styles du dashboard
│   │   ├── home.css               # Styles de la page d'accueil
│   │   └── revenue.css            # Styles des revenus
│   │
│   ├── 📂 js/                     # Scripts JavaScript
│   │   ├── script.js              # Scripts principaux (le plus important)
│   │   ├── dashboard.js           # Scripts du dashboard
│   │   ├── home.js                # Scripts de la page d'accueil
│   │   ├── modern-banner.js       # Scripts de bannière
│   │   └── revenue.js             # Scripts des revenus
│   │
│   ├── 📄 navigation.js           # Navigation (fichier racine frontend)
│   ├── 📄 README.md               # Documentation frontend
│   └── 📄 STRUCTURE_FRONTEND.md   # Structure du frontend
│
├── 📂 tests/                      # Tests unitaires et d'intégration
│   ├── test_api.py                # Tests de l'API
│   ├── test_auth_system.py        # Tests d'authentification
│   ├── test_*.py                  # Autres tests
│   └── ...
│
├── 📂 scripts/                    # Scripts utilitaires
│   ├── ameliorer_*.py             # Scripts d'amélioration
│   ├── optimiser_*.py             # Scripts d'optimisation
│   ├── generer_*.py               # Scripts de génération
│   ├── verifier_*.py              # Scripts de vérification
│   └── ...
│
└── 📂 docs/                       # Documentation
    ├── installation.md            # Guide d'installation
    ├── user_guide.md              # Guide utilisateur
    ├── *.md                       # Autres documentations
    └── ...
```

## 📋 Description des Dossiers

### `/backend`
Contient tout le code backend Python :
- **api_server.py** : Point d'entrée principal, serveur Flask
- **cacao1.py** : Logique métier et calculs
- **auth_system.py** : Gestion de l'authentification
- **train_model.py** : Entraînement du modèle ML
- **model_productivite_xgb.pkl** : Modèle XGBoost pré-entraîné
- **data.sqlite** : Base de données SQLite

### `/frontend`
Contient toute l'interface utilisateur :
- **HTML** : Pages web principales
- **css/** : Styles et thèmes
- **js/** : Logique JavaScript côté client
- **index.html** : Point d'entrée de l'application

### `/tests`
Contient tous les tests :
- Tests unitaires
- Tests d'intégration
- Tests de l'API
- Tests d'authentification

### `/scripts`
Contient les scripts utilitaires :
- Scripts d'amélioration
- Scripts d'optimisation
- Scripts de maintenance
- Scripts de migration

### `/docs`
Contient toute la documentation :
- Guides d'installation
- Guides utilisateur
- Documentation technique
- Notes de développement

## 🔍 Fichiers Clés

### Fichiers de Configuration
- **requirements.txt** : Dépendances Python
- **.gitignore** : Fichiers ignorés par Git
- **LICENSE** : Licence du projet

### Fichiers de Documentation
- **README.md** : Documentation principale
- **QUICKSTART.md** : Guide de démarrage rapide
- **DEPLOYMENT.md** : Guide de déploiement
- **STRUCTURE.md** : Ce fichier

### Fichiers Backend Principaux
- **backend/api_server.py** : Serveur Flask
- **backend/cacao1.py** : Logique métier
- **backend/model_productivite_xgb.pkl** : Modèle ML

### Fichiers Frontend Principaux
- **frontend/index.html** : Page d'accueil
- **frontend/css/style.css** : Styles principaux
- **frontend/js/script.js** : Scripts principaux

## 🎯 Points d'Entrée

### Pour Démarrer l'Application
1. **Backend** : `python backend/api_server.py`
2. **Frontend** : Ouvrir `frontend/index.html`

### Pour les Tests
- `python -m pytest tests/`
- `python tests/test_api.py`

### Pour l'Entraînement du Modèle
- `python backend/train_model.py`

## 📊 Flux de Données

```
Utilisateur
    ↓
frontend/index.html
    ↓
frontend/js/script.js
    ↓
API REST (backend/api_server.py)
    ↓
backend/cacao1.py (logique métier)
    ↓
backend/model_productivite_xgb.pkl (ML)
    ↓
backend/data.sqlite (base de données)
```

## 🔄 Workflow de Développement

1. **Modifier le code** dans `/backend` ou `/frontend`
2. **Tester** avec les fichiers dans `/tests`
3. **Documenter** dans `/docs` si nécessaire
4. **Commit** avec Git
5. **Déployer** selon `DEPLOYMENT.md`

## 📝 Notes Importantes

- Le fichier **frontend/css/style.css** est le fichier CSS principal et doit être chargé en dernier
- Le fichier **frontend/js/script.js** contient les fonctions JavaScript principales
- Le modèle ML doit être présent dans `/backend` pour que l'API fonctionne
- Les données sont stockées dans `localStorage` du navigateur (côté client)
- La base de données SQLite est utilisée pour l'authentification (côté serveur)

## 🚀 Prochaines Étapes

Pour commencer à utiliser le projet :
1. Lisez [QUICKSTART.md](QUICKSTART.md)
2. Consultez [README.md](README.md) pour plus de détails
3. Explorez le code dans `/backend` et `/frontend`
4. Consultez [DEPLOYMENT.md](DEPLOYMENT.md) pour le déploiement

---

*Dernière mise à jour : Décembre 2024*

