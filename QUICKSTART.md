# ⚡ Démarrage Rapide - Mon Cacao

Guide rapide pour démarrer l'application en 5 minutes.

## 🚀 Installation Express

### 1. Prérequis
- Python 3.8+ installé
- Navigateur web moderne

### 2. Installation

```bash
# Cloner ou télécharger le projet
cd mon-cacao

# Créer l'environnement virtuel (optionnel mais recommandé)
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Lancer l'application

**Terminal 1 - Backend:**
```bash
python backend/api_server.py
```
✅ Le serveur démarre sur `http://localhost:5000`

**Terminal 2 - Frontend (optionnel):**
```bash
cd frontend
python -m http.server 8000
```

### 4. Ouvrir dans le navigateur

**Option A (Recommandé):**
- Ouvrez directement `frontend/index.html` dans votre navigateur

**Option B:**
- Ouvrez `http://localhost:8000/index.html` si vous utilisez le serveur local

## 🎯 Première Utilisation

### Pour les Producteurs

1. Ouvrez `frontend/index.html`
2. Cliquez sur "Producteur"
3. Explorez les fonctionnalités :
   - **Prédictions** : Estimez votre productivité
   - **Soumettre** : Enregistrez vos données
   - **Historique** : Consultez vos données

### Pour les Professionnels

1. Ouvrez `frontend/index.html`
2. Cliquez sur "Professionnel/Entité/Structure/Coopérative"
3. Dans le dashboard :
   - Cliquez sur "Ajouter un producteur"
   - Remplissez le formulaire
   - Copiez le code producteur généré
   - Partagez ce code avec le producteur
4. Consultez les données de vos producteurs

## ⚠️ Dépannage Rapide

### Le modèle ne se charge pas
```bash
cd backend
python train_model.py
```

### L'API ne répond pas
- Vérifiez que le serveur est lancé : `python backend/api_server.py`
- Vérifiez le port 5000 (peut être occupé)

### Erreur de dépendances
```bash
pip install --upgrade -r requirements.txt
```

## 📱 Test sur Mobile

1. Trouvez l'adresse IP de votre ordinateur :
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` ou `ip addr`
2. Sur votre mobile, ouvrez : `http://VOTRE_IP:5000`
3. Ou utilisez un outil comme ngrok pour un accès externe

## 🔗 URLs Importantes

- **Frontend**: `frontend/index.html` ou `http://localhost:8000/index.html`
- **API Backend**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`

## 📚 Documentation Complète

- [README.md](README.md) - Documentation complète
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement
- [docs/](docs/) - Documentation détaillée

## ✅ Checklist de Vérification

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Modèle présent (`backend/model_productivite_xgb.pkl`)
- [ ] Serveur backend lancé (`python backend/api_server.py`)
- [ ] Frontend accessible (`frontend/index.html`)

## 🎉 C'est Prêt !

Vous pouvez maintenant utiliser l'application Mon Cacao !

Pour toute question, consultez le [README.md](README.md) complet.

---

*Dernière mise à jour : Décembre 2024*

