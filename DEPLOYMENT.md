# 🚀 Guide de Déploiement - Mon Cacao

Ce guide vous aidera à déployer l'application Mon Cacao sur différents environnements.

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip installé
- Accès à un serveur web (pour le déploiement production)
- Navigateur web moderne

## 🔧 Déploiement Local

### Étape 1: Préparation

```bash
# Cloner ou télécharger le projet
cd mon-cacao

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 2: Vérifier le modèle

```bash
# Vérifier que le modèle existe
ls backend/model_productivite_xgb.pkl

# Si le modèle n'existe pas, l'entraîner
cd backend
python train_model.py
cd ..
```

### Étape 3: Lancer le serveur backend

```bash
# Depuis la racine du projet
python backend/api_server.py
```

Le serveur démarre sur `http://localhost:5000`

### Étape 4: Ouvrir le frontend

**Option A: Ouvrir directement**
- Ouvrez `frontend/index.html` dans votre navigateur

**Option B: Serveur local**
```bash
cd frontend
python -m http.server 8000
# Ouvrez http://localhost:8000/index.html
```

## 🌐 Déploiement Production

### Option 1: Serveur Dédié (Linux)

#### Installation

```bash
# Mettre à jour le système
sudo apt update
sudo apt upgrade -y

# Installer Python et pip
sudo apt install python3 python3-pip python3-venv -y

# Cloner le projet
git clone https://github.com/votre-username/mon-cacao.git
cd mon-cacao

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

#### Configuration avec Gunicorn

```bash
# Installer Gunicorn
pip install gunicorn

# Créer un fichier de configuration
cat > gunicorn_config.py << EOF
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
EOF

# Lancer avec Gunicorn
gunicorn -c gunicorn_config.py backend.api_server:app
```

#### Service Systemd (Démarrage automatique)

```bash
# Créer le service
sudo nano /etc/systemd/system/mon-cacao.service
```

Contenu du fichier :

```ini
[Unit]
Description=Mon Cacao API Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/chemin/vers/mon-cacao
Environment="PATH=/chemin/vers/mon-cacao/venv/bin"
ExecStart=/chemin/vers/mon-cacao/venv/bin/gunicorn -c gunicorn_config.py backend.api_server:app

[Install]
WantedBy=multi-user.target
```

```bash
# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable mon-cacao
sudo systemctl start mon-cacao

# Vérifier le statut
sudo systemctl status mon-cacao
```

#### Configuration Nginx (Reverse Proxy)

```bash
# Installer Nginx
sudo apt install nginx -y

# Créer la configuration
sudo nano /etc/nginx/sites-available/mon-cacao
```

Contenu :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    # Frontend
    location / {
        root /chemin/vers/mon-cacao/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/mon-cacao /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Heroku

#### Préparation

```bash
# Installer Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Se connecter
heroku login

# Créer l'application
heroku create mon-cacao-app

# Créer Procfile
echo "web: gunicorn backend.api_server:app" > Procfile

# Déployer
git push heroku main
```

### Option 3: Docker (À venir)

Un fichier `Dockerfile` sera ajouté dans une future version.

## 🔒 Sécurité

### Recommandations

1. **Variables d'environnement** : Utilisez des variables d'environnement pour les secrets
2. **HTTPS** : Configurez SSL/TLS pour la production
3. **Firewall** : Limitez l'accès aux ports nécessaires
4. **Mises à jour** : Maintenez les dépendances à jour
5. **Backup** : Sauvegardez régulièrement la base de données

### Configuration HTTPS avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique
sudo certbot renew --dry-run
```

## 📊 Monitoring

### Logs

```bash
# Logs du service
sudo journalctl -u mon-cacao -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance

- Utilisez un outil de monitoring comme Prometheus ou Grafana
- Surveillez l'utilisation CPU et mémoire
- Surveillez les temps de réponse de l'API

## 🔄 Mise à Jour

```bash
# Arrêter le service
sudo systemctl stop mon-cacao

# Mettre à jour le code
git pull origin main

# Réinstaller les dépendances si nécessaire
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Redémarrer le service
sudo systemctl start mon-cacao
```

## 🐛 Dépannage

### Le service ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u mon-cacao -n 50

# Vérifier les permissions
ls -la /chemin/vers/mon-cacao

# Vérifier le chemin Python
which python3
```

### L'API ne répond pas

```bash
# Vérifier que le service est actif
sudo systemctl status mon-cacao

# Vérifier les ports
sudo netstat -tlnp | grep 5000

# Tester l'API
curl http://localhost:5000/health
```

### Problèmes de CORS

- Vérifiez que `flask-cors` est installé
- Vérifiez la configuration CORS dans `backend/api_server.py`

## 📞 Support

Pour toute question ou problème de déploiement :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Vérifiez les logs d'erreur

---

*Dernière mise à jour : Décembre 2024*

