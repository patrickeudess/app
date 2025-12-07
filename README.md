# 🌱 Mon Cacao - Application d'Analyse et Prédiction de Productivité

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Une application web complète pour l'analyse et la prédiction de la productivité du cacao, intégrant des fonctionnalités d'IA, d'analyse de données et de score écologique.**

[🚀 Démarrage Rapide](#-démarrage-rapide) • [📋 Fonctionnalités](#-fonctionnalités-principales) • [🛠️ Installation](#-installation) • [📖 Documentation](#-documentation)

</div>

---

## 📸 Aperçu

Mon Cacao est une application web progressive (PWA) conçue pour aider les producteurs de cacao et les professionnels du secteur à optimiser leur production grâce à l'intelligence artificielle et à l'analyse de données.

### 🎯 Objectifs

- ✅ Prédire la productivité du cacao avec un modèle XGBoost
- ✅ Analyser les revenus et la rentabilité
- ✅ Évaluer l'impact environnemental (score écologique)
- ✅ Fournir des conseils personnalisés via un assistant IA
- ✅ Gérer plusieurs producteurs (pour les professionnels)

---

## 🚀 Démarrage Rapide

### Option 1 : Téléchargement Direct (Recommandé pour Visualisation)

1. **Téléchargez le projet**
   - Sur GitHub, cliquez sur **"Code"** > **"Download ZIP"**
   - Extrayez le fichier ZIP dans un dossier de votre choix
   - Ou utilisez git clone :
   ```bash
   git clone https://github.com/votre-username/mon-cacao.git
   ```

2. **Ouvrez directement dans le navigateur**
   - Naviguez vers le dossier `frontend/`
   - **Double-cliquez** sur `index.html`
   - L'application s'ouvre dans votre navigateur ! 🎉

> ⚠️ **Note** : Pour les fonctionnalités complètes (prédictions IA), vous devrez lancer le serveur backend (voir [Installation complète](#-installation-complète)).
> 
> 📥 **Guide détaillé** : Consultez [GUIDE_TELECHARGEMENT.md](GUIDE_TELECHARGEMENT.md) pour des instructions pas à pas.

### Option 2 : Installation Complète

Voir la section [Installation](#-installation-complète) ci-dessous.

---

## 📋 Fonctionnalités Principales

### 👥 Gestion Multi-utilisateurs

| Type d'utilisateur | Fonctionnalités |
|-------------------|-----------------|
| **🌾 Producteur** | • Prédictions de production<br>• Enregistrement de données<br>• Historique personnel<br>• Conseils personnalisés |
| **🏢 Professionnel** | • Dashboard complet<br>• Gestion de plusieurs producteurs<br>• Analyses agrégées<br>• Génération de rapports |

### 🤖 Intelligence Artificielle

- **Modèle XGBoost** pour prédire la productivité
- **Assistant IA** pour conseils personnalisés
- **Recommandations** basées sur les données
- **Mode simulation** si l'API n'est pas disponible

### 📊 Visualisations et Analyses

- Graphiques interactifs (Chart.js)
- Analyses de tendances
- Comparaisons régionales
- Projections financières

### 🌿 Score Écologique

- Évaluation de l'impact environnemental
- Indicateurs de durabilité
- Recommandations d'amélioration

### 📱 Progressive Web App (PWA)

- Fonctionne hors ligne
- Installable sur mobile
- Interface responsive
- Service Worker intégré

---

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.8+** - Langage principal
- **Flask** - Framework web
- **XGBoost** - Modèle de machine learning
- **SQLite** - Base de données
- **Scikit-learn, Pandas, NumPy** - Traitement de données

### Frontend
- **HTML5, CSS3, JavaScript (ES6+)** - Technologies web
- **Chart.js** - Visualisations
- **Font Awesome** - Icônes
- **Service Workers** - PWA

---

## 📦 Installation Complète

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

### Étapes d'Installation

#### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/mon-cacao.git
cd mon-cacao
```

#### 2. Créer un environnement virtuel (recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 4. Vérifier le modèle ML

Assurez-vous que le fichier `backend/model_productivite_xgb.pkl` existe. Si ce n'est pas le cas :

```bash
cd backend
python train_model.py
cd ..
```

#### 5. Lancer le serveur backend

```bash
python backend/api_server.py
```

Le serveur démarre sur `http://localhost:5000`

#### 6. Ouvrir l'application

**Option A - Directement :**
- Ouvrez `frontend/index.html` dans votre navigateur

**Option B - Serveur local :**
```bash
cd frontend
python -m http.server 8000
# Ouvrez http://localhost:8000/index.html
```

---

## 📁 Structure du Projet

```
mon-cacao/
├── 📂 backend/                    # Code backend Python
│   ├── api_server.py              # Serveur Flask principal
│   ├── cacao1.py                  # Logique métier principale
│   ├── auth_system.py             # Système d'authentification
│   ├── train_model.py             # Script d'entraînement du modèle
│   ├── model_productivite_xgb.pkl # Modèle XGBoost entraîné
│   └── data.sqlite                # Base de données SQLite
│
├── 📂 frontend/                   # Interface utilisateur
│   ├── index.html                 # Page d'accueil
│   ├── dashboard-professionnel.html
│   ├── prediction.html            # Prédictions IA
│   ├── score-ecologique.html     # Score écologique
│   ├── analyse.html               # Analyses détaillées
│   ├── 📂 css/                    # Styles CSS
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   └── ...
│   └── 📂 js/                     # Scripts JavaScript
│       ├── script.js
│       ├── dashboard.js
│       └── ...
│
├── 📂 tests/                      # Tests unitaires
│   ├── test_api.py
│   ├── test_auth_system.py
│   └── ...
│
├── 📂 scripts/                    # Scripts utilitaires
│   └── ...
│
├── 📂 docs/                       # Documentation
│   ├── installation.md
│   ├── user_guide.md
│   └── ...
│
├── requirements.txt               # Dépendances Python
├── .gitignore                     # Fichiers ignorés par Git
├── LICENSE                        # Licence du projet
└── README.md                      # Ce fichier
```

---

## 🎯 Utilisation

### Pour les Producteurs

1. Ouvrez `frontend/index.html`
2. Sélectionnez "Producteur"
3. Explorez les fonctionnalités :
   - **Estimation** : Prédisez votre productivité
   - **Enregistrer** : Sauvegardez vos données
   - **Mes enregistrements** : Consultez l'historique
   - **Étude** : Visualisez vos données
   - **Aide intelligent** : Obtenez des conseils

### Pour les Professionnels

1. Ouvrez `frontend/index.html`
2. Sélectionnez "Professionnel/Entité/Structure/Coopérative"
3. Dans le dashboard :
   - Cliquez sur "Ajouter un producteur"
   - Remplissez le formulaire
   - Copiez le code producteur généré
   - Partagez ce code avec le producteur
4. Consultez les données agrégées de vos producteurs

---

## 🔧 Configuration

### Variables d'Environnement (Optionnel)

Créez un fichier `.env` à la racine :

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Configuration de la Base de Données

La base de données SQLite est créée automatiquement au premier lancement dans `backend/data.sqlite`.

---

## 🧪 Tests

```bash
# Lancer tous les tests
python -m pytest tests/

# Test spécifique
python tests/test_api.py
```

---

## 📖 Documentation

- **[GUIDE_TELECHARGEMENT.md](GUIDE_TELECHARGEMENT.md)** - 📥 Guide complet de téléchargement et visualisation
- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage rapide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guide de déploiement
- **[docs/](docs/)** - Documentation détaillée
  - `installation.md` - Guide d'installation
  - `user_guide.md` - Guide utilisateur
  - `INTEGRATION_XGBOOST.md` - Documentation ML

---

## 🐛 Dépannage

### Le modèle ne se charge pas

```bash
cd backend
python train_model.py
```

### L'API ne répond pas

- Vérifiez que le serveur est lancé : `python backend/api_server.py`
- Vérifiez le port 5000 (peut être occupé)
- Consultez les logs dans la console

### Erreur de dépendances

```bash
pip install --upgrade -r requirements.txt
```

### Problèmes de CORS

Assurez-vous que `flask-cors` est installé et configuré dans `api_server.py`.

---

## 🚀 Déploiement

Voir [DEPLOYMENT.md](DEPLOYMENT.md) pour les instructions complètes de déploiement.

### Options de Déploiement

- **Heroku** : Déploiement cloud simple
- **Docker** : Conteneurisation
- **VPS** : Serveur dédié
- **GitHub Pages** : Frontend statique (sans backend)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

- **Votre Nom** - *Développement initial* - [VotreGitHub](https://github.com/votre-username)

---

## 🙏 Remerciements

- Tous les contributeurs qui ont aidé à améliorer ce projet
- La communauté open source pour les outils utilisés
- Les producteurs de cacao pour leur feedback

---

## 📞 Support

Pour toute question ou problème :

- 📧 Email : votre-email@example.com
- 🐛 Issues : [GitHub Issues](https://github.com/votre-username/mon-cacao/issues)
- 📖 Documentation : [docs/](docs/)

---

<div align="center">

**Fait avec ❤️ pour les producteurs de cacao**

⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile !

</div>
