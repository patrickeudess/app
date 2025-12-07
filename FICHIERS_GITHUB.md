# 📦 Fichiers à Télécharger sur GitHub - Mon Cacao

Ce document liste **TOUS les fichiers essentiels** à inclure dans votre dépôt GitHub pour que l'application fonctionne complètement.

---

## ✅ FICHIERS OBLIGATOIRES (Doivent être sur GitHub)

### 📄 Documentation (Racine du projet)

Ces fichiers sont **ESSENTIELS** pour que les utilisateurs comprennent et utilisent le projet :

```
✅ README.md                    # Documentation principale (affichée sur GitHub)
✅ QUICKSTART.md                # Guide de démarrage rapide
✅ GUIDE_TELECHARGEMENT.md      # Guide de téléchargement détaillé
✅ DEPLOYMENT.md                # Guide de déploiement
✅ CONTRIBUTING.md              # Guide de contribution
✅ CHANGELOG.md                 # Historique des versions
✅ LICENSE                      # Licence du projet
✅ requirements.txt             # Dépendances Python (ESSENTIEL)
✅ .gitignore                   # Fichiers à exclure (ESSENTIEL)
✅ COMMENT_TELECHARGER.txt      # Instructions rapides
```

### 📂 Frontend (Tous les fichiers)

**TOUS les fichiers du dossier `frontend/` doivent être inclus** :

#### Pages HTML (26 fichiers)
```
✅ frontend/index.html
✅ frontend/user-type-selection.html
✅ frontend/auth.html
✅ frontend/dashboard.html
✅ frontend/dashboard-professionnel.html
✅ frontend/prediction.html
✅ frontend/soumettre.html
✅ frontend/historique.html
✅ frontend/analyse.html
✅ frontend/assistant.html
✅ frontend/conseils.html
✅ frontend/score-ecologique.html
✅ frontend/revenue.html
✅ frontend/revenus.html
✅ frontend/production.html
✅ frontend/mes-producteurs.html
✅ frontend/estimation-production.html
✅ frontend/analyse-conseils.html
✅ frontend/statistiques.html
✅ frontend/graphiques.html
✅ frontend/rapports.html
✅ frontend/messagerie.html
✅ frontend/cartographie.html
✅ frontend/gamification.html
✅ frontend/producteur-details.html
✅ frontend/offline.html
```

#### Fichiers CSS (5 fichiers)
```
✅ frontend/css/style.css              # ESSENTIEL - Styles principaux
✅ frontend/css/modern-banner.css      # Styles de bannière
✅ frontend/css/dashboard.css          # Styles dashboard
✅ frontend/css/home.css               # Styles page d'accueil
✅ frontend/css/revenue.css            # Styles revenus
```

#### Fichiers JavaScript (11 fichiers)
```
✅ frontend/js/script.js               # ESSENTIEL - Scripts principaux
✅ frontend/js/auth.js                 # ESSENTIEL - Authentification
✅ frontend/js/database-sync.js        # Synchronisation base de données
✅ frontend/js/modern-banner.js        # Bannière moderne
✅ frontend/js/dashboard.js            # Dashboard
✅ frontend/js/home.js                 # Page d'accueil
✅ frontend/js/revenue.js              # Revenus
✅ frontend/js/weather.js              # Météo
✅ frontend/js/notifications.js        # Notifications
✅ frontend/navigation.js              # Navigation (racine frontend)
✅ frontend/sw.js                      # ESSENTIEL - Service Worker (PWA)
```

#### Autres fichiers Frontend
```
✅ frontend/manifest.json              # Manifest PWA
✅ frontend/README.md                  # Documentation frontend (optionnel)
✅ frontend/STRUCTURE_FRONTEND.md       # Structure frontend (optionnel)
```

### 📂 Backend (Code Python)

**TOUS les fichiers Python du dossier `backend/` doivent être inclus** :

```
✅ backend/api_server.py               # ESSENTIEL - Serveur Flask principal
✅ backend/cacao1.py                  # ESSENTIEL - Logique métier
✅ backend/auth_system.py              # ESSENTIEL - Système d'authentification
✅ backend/database.py                 # ESSENTIEL - Gestion base de données
✅ backend/train_model.py              # ESSENTIEL - Entraînement modèle ML
✅ backend/pdf_generator.py            # Génération de rapports PDF
✅ backend/login_interface.py          # Interface de connexion
```

#### Modèle Machine Learning

```
✅ backend/model_productivite_xgb.pkl  # ESSENTIEL - Modèle XGBoost
```

> ⚠️ **ATTENTION** : Si le fichier `.pkl` fait plus de 100MB, utilisez Git LFS ou hébergez-le séparément.

### 📂 Documentation (docs/)

**Tous les fichiers de documentation** (optionnel mais recommandé) :

```
✅ docs/installation.md
✅ docs/user_guide.md
✅ docs/INTEGRATION_XGBOOST.md
✅ docs/SCORE_ECOLOGIQUE_DOCUMENTATION.md
✅ ... (tous les autres fichiers .md dans docs/)
```

### 📂 Tests (tests/)

**Tous les fichiers de tests** (optionnel mais recommandé) :

```
✅ tests/test_api.py
✅ tests/test_auth_system.py
✅ ... (tous les autres fichiers de test)
```

### 📂 Scripts (scripts/)

**Tous les scripts utilitaires** (optionnel) :

```
✅ scripts/*.py
```

### 📂 Configuration GitHub (.github/)

**Templates GitHub** (recommandé) :

```
✅ .github/ISSUE_TEMPLATE/bug_report.md
✅ .github/ISSUE_TEMPLATE/feature_request.md
✅ .github/ISSUE_TEMPLATE/config.yml
```

---

## ❌ FICHIERS À EXCLURE (Ne pas mettre sur GitHub)

Ces fichiers sont **AUTOMATIQUEMENT exclus** par `.gitignore` :

### Bases de données
```
❌ backend/data.sqlite              # Créée automatiquement
❌ backend/*.db                      # Bases de données
❌ *.sqlite                          # Toutes les bases SQLite
```

### Cache et fichiers temporaires
```
❌ __pycache__/                     # Cache Python
❌ *.pyc, *.pyo                     # Fichiers compilés Python
❌ *.log                            # Fichiers de log
❌ *.tmp, *.temp, *.bak             # Fichiers temporaires
```

### Environnements virtuels
```
❌ venv/                            # Environnement virtuel Python
❌ .venv/                           # Environnement virtuel
❌ env/                             # Environnement virtuel
```

### Fichiers système
```
❌ .DS_Store                         # macOS
❌ Thumbs.db                        # Windows
❌ .vscode/                         # Configuration IDE
❌ .idea/                           # Configuration IDE
```

### Fichiers sensibles
```
❌ .env                             # Variables d'environnement
❌ config.local.py                  # Configuration locale
```

---

## 📋 Checklist Complète

### ✅ À Inclure (Obligatoire)

- [ ] **Documentation** : README.md, QUICKSTART.md, GUIDE_TELECHARGEMENT.md, etc.
- [ ] **Configuration** : .gitignore, requirements.txt, LICENSE
- [ ] **Frontend complet** : Tous les fichiers HTML, CSS, JS dans `frontend/`
- [ ] **Backend complet** : Tous les fichiers Python dans `backend/`
- [ ] **Modèle ML** : `backend/model_productivite_xgb.pkl` (si < 100MB)
- [ ] **Documentation** : Tous les fichiers dans `docs/` (optionnel)
- [ ] **Tests** : Tous les fichiers dans `tests/` (optionnel)
- [ ] **Scripts** : Tous les fichiers dans `scripts/` (optionnel)
- [ ] **GitHub** : Templates dans `.github/` (recommandé)

### ❌ À Exclure (Automatique)

- [x] Bases de données (data.sqlite, *.db)
- [x] Cache Python (__pycache__/, *.pyc)
- [x] Environnements virtuels (venv/, .venv/)
- [x] Fichiers de log (*.log)
- [x] Fichiers temporaires (*.tmp, *.bak)
- [x] Fichiers système (.DS_Store, Thumbs.db)
- [x] Configuration IDE (.vscode/, .idea/)
- [x] Variables d'environnement (.env)

---

## 🎯 Structure Minimale Requise

Pour que l'application fonctionne, vous devez **AU MINIMUM** inclure :

```
mon-cacao/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── frontend/
│   ├── index.html
│   ├── *.html (toutes les pages)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   └── auth.js
│   └── sw.js
│
└── backend/
    ├── api_server.py
    ├── cacao1.py
    ├── auth_system.py
    ├── database.py
    ├── train_model.py
    └── model_productivite_xgb.pkl
```

---

## 📊 Taille des Fichiers

### Fichiers Petits (< 1MB)
- ✅ Tous les fichiers HTML, CSS, JS
- ✅ Tous les fichiers Python
- ✅ Tous les fichiers de documentation

### Fichiers Moyens (1-10MB)
- ⚠️ `backend/model_productivite_xgb.pkl` (généralement 5-50MB)

### Fichiers Volumineux (> 100MB)
- ❌ Si le modèle ML fait plus de 100MB, utilisez **Git LFS** :
  ```bash
  git lfs install
  git lfs track "*.pkl"
  git add .gitattributes
  git add backend/model_productivite_xgb.pkl
  ```

---

## 🚀 Commandes Git pour Vérifier

### Vérifier ce qui sera inclus

```bash
# Voir tous les fichiers qui seront commités
git add .
git status

# Voir les fichiers ignorés
git status --ignored
```

### Ajouter tous les fichiers nécessaires

```bash
# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Vérifier ce qui sera commité
git status

# Commit
git commit -m "Initial commit - Mon Cacao Application"

# Push vers GitHub
git push origin main
```

---

## ✅ Vérification Finale

Avant de publier sur GitHub, vérifiez que :

1. ✅ **README.md** est présent et complet
2. ✅ **requirements.txt** est présent
3. ✅ **Tous les fichiers frontend/** sont inclus
4. ✅ **Tous les fichiers backend/*.py** sont inclus
5. ✅ **Le modèle ML** est inclus (ou accessible)
6. ✅ **.gitignore** est présent et correct
7. ✅ **Aucun fichier sensible** n'est inclus (.env, mots de passe, etc.)
8. ✅ **Aucune base de données** n'est incluse (data.sqlite)

---

## 📝 Résumé

### Fichiers Essentiels (Minimum)
- ✅ Documentation : README.md, requirements.txt, .gitignore
- ✅ Frontend : Tous les fichiers dans `frontend/`
- ✅ Backend : Tous les fichiers Python dans `backend/`
- ✅ Modèle ML : `backend/model_productivite_xgb.pkl`

### Fichiers Recommandés
- ✅ Documentation complète (docs/)
- ✅ Tests (tests/)
- ✅ Scripts (scripts/)
- ✅ Templates GitHub (.github/)

### Fichiers à Exclure
- ❌ Bases de données (*.sqlite, *.db)
- ❌ Cache (__pycache__/, *.pyc)
- ❌ Environnements virtuels (venv/)
- ❌ Fichiers temporaires (*.log, *.tmp)
- ❌ Fichiers sensibles (.env)

---

<div align="center">

**📦 Tous ces fichiers sont nécessaires pour que l'application fonctionne complètement !**

*Dernière mise à jour : Décembre 2024*

</div>

