# 📥 Guide de Téléchargement et Visualisation - Mon Cacao

Ce guide vous explique comment télécharger et visualiser rapidement le projet **Mon Cacao** depuis GitHub.

---

## 🚀 Méthode 1 : Téléchargement Direct (Le Plus Simple)

### Étape 1 : Télécharger le Projet

1. **Sur GitHub**, allez sur la page du dépôt
2. Cliquez sur le bouton vert **"Code"** en haut à droite
3. Sélectionnez **"Download ZIP"**
4. Extrayez le fichier ZIP dans un dossier de votre choix

### Étape 2 : Ouvrir et Visualiser

**Option A - Visualisation Simple (Sans Backend) :**

1. Naviguez dans le dossier extrait
2. Ouvrez le dossier `frontend`
3. **Double-cliquez** sur `index.html`
4. L'application s'ouvre dans votre navigateur ! 🎉

> ✅ **Avantages** : Fonctionne immédiatement, pas d'installation nécessaire
> 
> ⚠️ **Limitations** : Les prédictions IA nécessitent le backend (voir Méthode 2)

**Option B - Visualisation Complète (Avec Backend) :**

Suivez la [Méthode 2](#-méthode-2--installation-complète-avec-git) ci-dessous.

---

## 🔧 Méthode 2 : Installation Complète (Avec Git)

### Étape 1 : Cloner le Dépôt

Ouvrez un terminal (PowerShell, CMD, ou Terminal) et exécutez :

```bash
git clone https://github.com/VOTRE-USERNAME/mon-cacao.git
cd mon-cacao
```

> 💡 **Note** : Remplacez `VOTRE-USERNAME` par votre nom d'utilisateur GitHub ou l'URL complète du dépôt.

### Étape 2 : Installer les Dépendances Python

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 3 : Vérifier le Modèle ML

Assurez-vous que le fichier `backend/model_productivite_xgb.pkl` existe.

Si le fichier n'existe pas, créez-le :

```bash
cd backend
python train_model.py
cd ..
```

### Étape 4 : Lancer le Serveur Backend

```bash
python backend/api_server.py
```

✅ Le serveur démarre sur `http://localhost:5000`

### Étape 5 : Ouvrir l'Application

**Option 1 - Directement :**
- Ouvrez `frontend/index.html` dans votre navigateur

**Option 2 - Avec Serveur Local :**
```bash
cd frontend
python -m http.server 8000
```
Puis ouvrez `http://localhost:8000/index.html` dans votre navigateur.

---

## 📁 Structure des Fichiers Importants

Après téléchargement, voici les fichiers clés à connaître :

```
mon-cacao/
│
├── 📂 frontend/              ← DÉMARRER ICI pour visualisation simple
│   ├── index.html            ← Page principale (ouvrir ce fichier)
│   ├── dashboard.html
│   ├── prediction.html
│   ├── score-ecologique.html
│   ├── 📂 css/               ← Styles
│   └── 📂 js/                ← Scripts JavaScript
│
├── 📂 backend/               ← Nécessaire pour les prédictions IA
│   ├── api_server.py         ← Serveur Flask
│   ├── model_productivite_xgb.pkl  ← Modèle ML
│   └── data.sqlite           ← Base de données
│
├── requirements.txt          ← Dépendances Python
├── README.md                ← Documentation complète
└── QUICKSTART.md            ← Guide de démarrage rapide
```

---

## 🎯 Visualisation Rapide (5 minutes)

### Pour Visualiser l'Interface Seulement :

1. ✅ Téléchargez le ZIP depuis GitHub
2. ✅ Extrayez le fichier
3. ✅ Ouvrez `frontend/index.html` dans votre navigateur
4. ✅ Explorez l'interface !

### Pour Tester les Fonctionnalités Complètes :

1. ✅ Suivez la [Méthode 2](#-méthode-2--installation-complète-avec-git)
2. ✅ Installez Python et les dépendances
3. ✅ Lancez le serveur backend
4. ✅ Ouvrez `frontend/index.html`

---

## ⚠️ Dépannage

### Problème : "Le fichier ne s'ouvre pas correctement"

**Solution :**
- Utilisez un serveur local au lieu d'ouvrir directement le fichier
- Dans le dossier `frontend`, exécutez : `python -m http.server 8000`
- Ouvrez `http://localhost:8000/index.html`

### Problème : "Les prédictions ne fonctionnent pas"

**Solution :**
- Vérifiez que le serveur backend est lancé : `python backend/api_server.py`
- Vérifiez que le modèle existe : `backend/model_productivite_xgb.pkl`
- Si le modèle n'existe pas, créez-le : `cd backend && python train_model.py`

### Problème : "Erreur de dépendances Python"

**Solution :**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problème : "Port 5000 déjà utilisé"

**Solution :**
- Modifiez le port dans `backend/api_server.py`
- Ou arrêtez le processus utilisant le port 5000

---

## 📱 Tester sur Mobile

### Option 1 : Via Réseau Local

1. Trouvez l'adresse IP de votre ordinateur :
   - **Windows** : `ipconfig` (cherchez "IPv4 Address")
   - **Linux/Mac** : `ifconfig` ou `ip addr`

2. Sur votre mobile (même réseau WiFi), ouvrez :
   ```
   http://VOTRE_IP:8000/index.html
   ```

### Option 2 : Via ngrok (Accès Externe)

1. Installez ngrok : https://ngrok.com/download
2. Lancez le serveur local : `python -m http.server 8000`
3. Dans un autre terminal : `ngrok http 8000`
4. Utilisez l'URL fournie par ngrok sur votre mobile

---

## ✅ Checklist de Vérification

Avant de commencer, vérifiez que vous avez :

- [ ] **Pour visualisation simple** :
  - [ ] Navigateur web moderne (Chrome, Firefox, Edge)
  - [ ] Fichier ZIP téléchargé et extrait
  - [ ] Fichier `frontend/index.html` accessible

- [ ] **Pour fonctionnalités complètes** :
  - [ ] Python 3.8+ installé
  - [ ] pip installé
  - [ ] Dépendances installées (`pip install -r requirements.txt`)
  - [ ] Modèle ML présent (`backend/model_productivite_xgb.pkl`)
  - [ ] Serveur backend lancé (`python backend/api_server.py`)

---

## 🎓 Ressources Supplémentaires

- **[README.md](README.md)** - Documentation complète du projet
- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage rapide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guide de déploiement
- **[docs/](docs/)** - Documentation détaillée

---

## 💡 Astuces

1. **Mode Développeur** : Ouvrez les outils de développement (F12) pour voir les erreurs
2. **Cache du Navigateur** : Appuyez sur `Ctrl+F5` pour forcer le rechargement
3. **Console** : Vérifiez la console du navigateur pour les messages d'erreur
4. **Service Worker** : Si vous avez des problèmes de cache, désactivez le Service Worker dans les DevTools

---

## 📞 Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. Consultez la section [Dépannage](#-dépannage) ci-dessus
2. Vérifiez les [Issues GitHub](https://github.com/VOTRE-USERNAME/mon-cacao/issues)
3. Consultez la [Documentation complète](README.md)

---

<div align="center">

**🎉 Bon téléchargement et bonne visualisation !**

*Dernière mise à jour : Décembre 2024*

</div>


