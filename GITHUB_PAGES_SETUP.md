# 🚀 Configuration GitHub Pages - Mon Cacao

Ce guide explique comment configurer votre projet pour qu'il s'affiche correctement sur GitHub Pages.

---

## ⚠️ Problème Identifié

Sur GitHub Pages, si votre dépôt s'appelle `mon-cacao`, l'URL sera :
```
https://votre-username.github.io/mon-cacao/
```

Les chemins relatifs comme `css/style.css` ne fonctionneront pas correctement car ils cherchent à la racine du site, pas dans le sous-dossier.

---

## ✅ Solutions

### Solution 1 : Utiliser la Racine du Dépôt (Recommandé)

**Configurez GitHub Pages pour servir depuis la racine du dépôt :**

1. Allez dans **Settings** de votre dépôt GitHub
2. Allez dans **Pages** (dans le menu de gauche)
3. Sous **Source**, sélectionnez :
   - **Branch** : `main` (ou `master`)
   - **Folder** : `/ (root)` ou `/frontend` selon votre structure
4. Cliquez sur **Save**

**Si vous choisissez `/frontend` :**
- Votre URL sera : `https://votre-username.github.io/mon-cacao/`
- Les fichiers dans `frontend/` seront servis à la racine
- Les chemins relatifs fonctionneront correctement

### Solution 2 : Ajuster les Chemins (Si nécessaire)

Si vous devez garder la structure actuelle, vous pouvez utiliser une base URL dans vos fichiers HTML.

---

## 📁 Structure Recommandée pour GitHub Pages

### Option A : Frontend à la Racine (Recommandé)

```
mon-cacao/
├── index.html          ← Déplacé depuis frontend/
├── css/
├── js/
├── *.html
├── backend/            ← Code Python (non servi par GitHub Pages)
└── docs/               ← Documentation
```

### Option B : Frontend dans un Sous-dossier

```
mon-cacao/
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
├── backend/
└── docs/
```

**Configuration GitHub Pages :** Source = `/frontend`

---

## 🔧 Fichiers de Configuration

### 1. Fichier `.nojekyll`

✅ **Créé** : Ce fichier désactive Jekyll sur GitHub Pages et permet d'utiliser tous les fichiers.

### 2. Fichier `404.html` (Optionnel)

Créez un fichier `404.html` dans `frontend/` pour rediriger vers `index.html` :

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirection...</title>
    <meta http-equiv="refresh" content="0; url=./index.html">
</head>
<body>
    <p>Redirection en cours... <a href="./index.html">Cliquez ici</a></p>
</body>
</html>
```

---

## 📝 Étapes de Configuration

### Étape 1 : Vérifier la Structure

Assurez-vous que votre structure est correcte :

```
mon-cacao/
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── *.html
├── .nojekyll          ← Important !
└── README.md
```

### Étape 2 : Configurer GitHub Pages

1. **Allez sur GitHub** → Votre dépôt
2. **Settings** → **Pages**
3. **Source** : Sélectionnez `main` et `/frontend`
4. **Save**

### Étape 3 : Attendre le Déploiement

- GitHub Pages prend quelques minutes pour déployer
- L'URL sera : `https://votre-username.github.io/mon-cacao/`

### Étape 4 : Vérifier

Ouvrez l'URL et vérifiez que :
- ✅ Les styles CSS s'affichent
- ✅ Les scripts JavaScript fonctionnent
- ✅ Les images s'affichent
- ✅ La navigation fonctionne

---

## 🔍 Dépannage

### Problème : Les CSS ne se chargent pas

**Solution :**
- Vérifiez que les chemins sont relatifs : `css/style.css` (pas `/css/style.css`)
- Vérifiez que le fichier `.nojekyll` est présent
- Vérifiez la configuration GitHub Pages (dossier source)

### Problème : Les pages ne se chargent pas

**Solution :**
- Vérifiez que tous les fichiers HTML sont dans le bon dossier
- Vérifiez que les liens sont relatifs : `soumettre.html` (pas `/soumettre.html`)

### Problème : Les scripts ne fonctionnent pas

**Solution :**
- Vérifiez la console du navigateur (F12) pour les erreurs
- Vérifiez que les chemins JS sont relatifs : `js/script.js`
- Vérifiez que les CDN externes sont accessibles

---

## 📋 Checklist

Avant de publier sur GitHub Pages :

- [ ] ✅ Fichier `.nojekyll` présent à la racine
- [ ] ✅ Structure des dossiers correcte
- [ ] ✅ Tous les chemins sont relatifs (pas de `/` au début)
- [ ] ✅ Configuration GitHub Pages définie
- [ ] ✅ Tous les fichiers frontend sont présents
- [ ] ✅ Testé localement avant de publier

---

## 🎯 Configuration Recommandée

**Pour une meilleure expérience :**

1. **Source GitHub Pages** : `/frontend`
2. **URL finale** : `https://votre-username.github.io/mon-cacao/`
3. **Chemins** : Tous relatifs (sans `/` au début)
4. **Fichier `.nojekyll`** : Présent à la racine

---

<div align="center">

**✅ Votre application sera accessible sur GitHub Pages !**

*Dernière mise à jour : Décembre 2024*

</div>

