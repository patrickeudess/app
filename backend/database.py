"""
Système de base de données pour Mon Cacao
Remplace localStorage par une vraie base de données SQLite
"""
import sqlite3
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import pyotp
import qrcode
from io import BytesIO
import base64

DB_PATH = os.path.join(os.path.dirname(__file__), "mon_cacao.db")

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Créer une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialiser toutes les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table des utilisateurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('producteur', 'professionnel')),
                region TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                two_factor_secret TEXT,
                two_factor_enabled INTEGER DEFAULT 0,
                reset_token TEXT,
                reset_token_expires TIMESTAMP
            )
        ''')
        
        # Table des producteurs (créés par les professionnels)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS producers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professional_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                region TEXT,
                phone TEXT,
                email TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professional_id) REFERENCES users(id)
            )
        ''')
        
        # Table des soumissions de données
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producer_id INTEGER,
                user_id INTEGER,
                age_verger REAL,
                agroforest TEXT,
                engrais TEXT,
                fumier TEXT,
                maladie TEXT,
                herbicide TEXT,
                insecticide TEXT,
                fongicide TEXT,
                cout_prod REAL,
                prix_vente REAL,
                production_reelle REAL,
                revenu_total REAL,
                region TEXT,
                pluviometrie TEXT,
                temperature REAL,
                humidite REAL,
                date_soumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                synced INTEGER DEFAULT 1,
                FOREIGN KEY (producer_id) REFERENCES producers(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des conseils donnés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advice_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producer_id INTEGER,
                user_id INTEGER,
                advice_text TEXT NOT NULL,
                category TEXT,
                advice_type TEXT,
                source TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producer_id) REFERENCES producers(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des badges et gamification
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                badge_type TEXT NOT NULL,
                badge_name TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des points et classements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                total_points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des messages (messagerie interne)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                subject TEXT,
                content TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
        ''')
        
        # Table des localisations (pour cartographie)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producer_id INTEGER,
                user_id INTEGER,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                address TEXT,
                region TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producer_id) REFERENCES producers(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Table des données météo (cache)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                temperature REAL,
                humidity REAL,
                precipitation REAL,
                forecast_data TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========== GESTION DES UTILISATEURS ==========
    
    def create_user(self, username, password, user_type, email=None, phone=None, region=None):
        """Créer un nouvel utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, phone, password_hash, user_type, region)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, phone, password_hash, user_type, region))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # Initialiser les points pour la gamification
            cursor.execute('''
                INSERT INTO user_points (user_id, total_points, level)
                VALUES (?, 0, 1)
            ''', (user_id,))
            conn.commit()
            
            conn.close()
            return {'success': True, 'user_id': user_id}
        except sqlite3.IntegrityError as e:
            conn.close()
            return {'success': False, 'error': 'Utilisateur déjà existant'}
        except Exception as e:
            conn.close()
            return {'success': False, 'error': str(e)}
    
    def authenticate_user(self, identifier, password):
        """Authentifier un utilisateur (par email, phone ou username)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE (email = ? OR phone = ? OR username = ?) AND is_active = 1
        ''', (identifier, identifier, identifier))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            # Mettre à jour la dernière connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user['id'],))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'user_type': user['user_type'],
                    'region': user['region'],
                    'two_factor_enabled': bool(user['two_factor_enabled'])
                }
            }
        
        return {'success': False, 'error': 'Identifiants invalides'}
    
    def enable_2fa(self, user_id):
        """Activer l'authentification à deux facteurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Générer un secret pour TOTP
        secret = pyotp.random_base32()
        
        cursor.execute('''
            UPDATE users 
            SET two_factor_secret = ?, two_factor_enabled = 1
            WHERE id = ?
        ''', (secret, user_id))
        
        conn.commit()
        conn.close()
        
        # Générer le QR code
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(
            name=f"user_{user_id}",
            issuer_name="Mon Cacao"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'success': True,
            'secret': secret,
            'qr_code': f'data:image/png;base64,{img_str}'
        }
    
    def verify_2fa(self, user_id, token):
        """Vérifier le code 2FA"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT two_factor_secret FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not user['two_factor_secret']:
            return {'success': False, 'error': '2FA non activé'}
        
        totp = pyotp.TOTP(user['two_factor_secret'])
        if totp.verify(token, valid_window=1):
            return {'success': True}
        
        return {'success': False, 'error': 'Code invalide'}
    
    def generate_reset_token(self, identifier):
        """Générer un token de réinitialisation de mot de passe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM users 
            WHERE email = ? OR phone = ? OR username = ?
        ''', (identifier, identifier, identifier))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return {'success': False, 'error': 'Utilisateur non trouvé'}
        
        # Générer un token sécurisé
        token = secrets.token_urlsafe(32)
        expires = datetime.now().timestamp() + 3600  # 1 heure
        
        cursor.execute('''
            UPDATE users 
            SET reset_token = ?, reset_token_expires = ?
            WHERE id = ?
        ''', (token, expires, user['id']))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'token': token, 'user_id': user['id']}
    
    def reset_password(self, token, new_password):
        """Réinitialiser le mot de passe avec un token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM users 
            WHERE reset_token = ? AND reset_token_expires > ?
        ''', (token, datetime.now().timestamp()))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return {'success': False, 'error': 'Token invalide ou expiré'}
        
        password_hash = generate_password_hash(new_password)
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL
            WHERE id = ?
        ''', (password_hash, user['id']))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    # ========== GESTION DES PRODUCTEURS ==========
    
    def create_producer(self, professional_id, name, region, phone=None, email=None, notes=None):
        """Créer un nouveau producteur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Générer un code unique
        timestamp = int(datetime.now().timestamp())
        random_part = secrets.token_hex(3).upper()
        code = f"PROD-{timestamp}-{random_part}"
        
        try:
            cursor.execute('''
                INSERT INTO producers (professional_id, name, code, region, phone, email, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (professional_id, name, code, region, phone, email, notes))
            
            producer_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {'success': True, 'producer_id': producer_id, 'code': code}
        except Exception as e:
            conn.close()
            return {'success': False, 'error': str(e)}
    
    def get_producers_by_professional(self, professional_id):
        """Récupérer tous les producteurs d'un professionnel"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM producers WHERE professional_id = ? ORDER BY created_at DESC
        ''', (professional_id,))
        
        producers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return producers
    
    # ========== GESTION DES SOUMISSIONS ==========
    
    def save_submission(self, user_id, producer_id=None, submission_data=None):
        """Sauvegarder une soumission de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO submissions (
                producer_id, user_id, age_verger, agroforest, engrais, fumier,
                maladie, herbicide, insecticide, fongicide, cout_prod, prix_vente,
                production_reelle, revenu_total, region, pluviometrie, temperature, humidite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            producer_id, user_id,
            submission_data.get('age_verger'),
            submission_data.get('agroforest'),
            submission_data.get('engrais'),
            submission_data.get('fumier'),
            submission_data.get('maladie'),
            submission_data.get('herbicide'),
            submission_data.get('insecticide'),
            submission_data.get('fongicide'),
            submission_data.get('cout_prod'),
            submission_data.get('prix_vente'),
            submission_data.get('production_reelle'),
            submission_data.get('revenu_total'),
            submission_data.get('region'),
            submission_data.get('pluviometrie'),
            submission_data.get('temperature'),
            submission_data.get('humidite')
        ))
        
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'submission_id': submission_id}
    
    def get_submissions(self, user_id=None, producer_id=None, limit=100):
        """Récupérer les soumissions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if producer_id:
            cursor.execute('''
                SELECT * FROM submissions 
                WHERE producer_id = ? 
                ORDER BY date_soumission DESC 
                LIMIT ?
            ''', (producer_id, limit))
        elif user_id:
            cursor.execute('''
                SELECT * FROM submissions 
                WHERE user_id = ? 
                ORDER BY date_soumission DESC 
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM submissions 
                ORDER BY date_soumission DESC 
                LIMIT ?
            ''', (limit,))
        
        submissions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return submissions
    
    # ========== GESTION DES CONSEILS ==========
    
    def save_advice(self, producer_id, user_id, advice_text, category, advice_type, source):
        """Sauvegarder un conseil donné"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO advice_tracking (producer_id, user_id, advice_text, category, advice_type, source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producer_id, user_id, advice_text, category, advice_type, source))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_advice_stats(self, professional_id=None):
        """Récupérer les statistiques des conseils"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if professional_id:
            # Récupérer les producteurs du professionnel
            cursor.execute('SELECT id FROM producers WHERE professional_id = ?', (professional_id,))
            producer_ids = [row['id'] for row in cursor.fetchall()]
            
            if not producer_ids:
                conn.close()
                return {'by_category': {}, 'by_type': {}, 'by_source': {}, 'total': 0}
            
            placeholders = ','.join('?' * len(producer_ids))
            cursor.execute(f'''
                SELECT category, advice_type, source, COUNT(*) as count
                FROM advice_tracking
                WHERE producer_id IN ({placeholders})
                GROUP BY category, advice_type, source
            ''', producer_ids)
        else:
            cursor.execute('''
                SELECT category, advice_type, source, COUNT(*) as count
                FROM advice_tracking
                GROUP BY category, advice_type, source
            ''')
        
        stats = {'by_category': {}, 'by_type': {}, 'by_source': {}, 'total': 0}
        
        for row in cursor.fetchall():
            stats['by_category'][row['category']] = stats['by_category'].get(row['category'], 0) + row['count']
            stats['by_type'][row['advice_type']] = stats['by_type'].get(row['advice_type'], 0) + row['count']
            stats['by_source'][row['source']] = stats['by_source'].get(row['source'], 0) + row['count']
            stats['total'] += row['count']
        
        conn.close()
        return stats
    
    # ========== GESTION DES NOTIFICATIONS ==========
    
    def create_notification(self, user_id, title, message, notification_type='info'):
        """Créer une notification"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, message, notification_type))
        
        notification_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'notification_id': notification_id}
    
    def get_notifications(self, user_id, unread_only=False, limit=50):
        """Récupérer les notifications d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if unread_only:
            cursor.execute('''
                SELECT * FROM notifications 
                WHERE user_id = ? AND read = 0
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM notifications 
                WHERE user_id = ?
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
        
        notifications = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return notifications
    
    def mark_notification_read(self, notification_id, user_id):
        """Marquer une notification comme lue"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET read = 1 
            WHERE id = ? AND user_id = ?
        ''', (notification_id, user_id))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    # ========== GAMIFICATION ==========
    
    def add_points(self, user_id, points, reason=''):
        """Ajouter des points à un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO user_points (user_id, total_points, level)
            VALUES (?, 0, 1)
        ''', (user_id,))
        
        cursor.execute('''
            UPDATE user_points 
            SET total_points = total_points + ?, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (points, user_id))
        
        # Calculer le niveau (1 point = 1 niveau, max 100)
        cursor.execute('''
            UPDATE user_points 
            SET level = MIN(100, CAST(total_points / 10 AS INTEGER) + 1)
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def award_badge(self, user_id, badge_type, badge_name):
        """Attribuer un badge à un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Vérifier si le badge existe déjà
        cursor.execute('''
            SELECT id FROM badges 
            WHERE user_id = ? AND badge_type = ? AND badge_name = ?
        ''', (user_id, badge_type, badge_name))
        
        if cursor.fetchone():
            conn.close()
            return {'success': False, 'error': 'Badge déjà obtenu'}
        
        cursor.execute('''
            INSERT INTO badges (user_id, badge_type, badge_name)
            VALUES (?, ?, ?)
        ''', (user_id, badge_type, badge_name))
        
        badge_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'badge_id': badge_id}
    
    def get_user_badges(self, user_id):
        """Récupérer les badges d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM badges 
            WHERE user_id = ? 
            ORDER BY earned_at DESC
        ''', (user_id,))
        
        badges = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return badges
    
    def get_leaderboard(self, limit=10):
        """Récupérer le classement des utilisateurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.user_type, up.total_points, up.level
            FROM user_points up
            JOIN users u ON up.user_id = u.id
            WHERE u.is_active = 1
            ORDER BY up.total_points DESC
            LIMIT ?
        ''', (limit,))
        
        leaderboard = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return leaderboard
    
    # ========== MESSAGERIE ==========
    
    def send_message(self, sender_id, receiver_id, subject, content):
        """Envoyer un message"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (sender_id, receiver_id, subject, content)
            VALUES (?, ?, ?, ?)
        ''', (sender_id, receiver_id, subject, content))
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'message_id': message_id}
    
    def get_messages(self, user_id, folder='inbox'):
        """Récupérer les messages (inbox ou sent)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if folder == 'inbox':
            cursor.execute('''
                SELECT m.*, u.username as sender_name
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.receiver_id = ?
                ORDER BY m.created_at DESC
            ''', (user_id,))
        else:  # sent
            cursor.execute('''
                SELECT m.*, u.username as receiver_name
                FROM messages m
                JOIN users u ON m.receiver_id = u.id
                WHERE m.sender_id = ?
                ORDER BY m.created_at DESC
            ''', (user_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return messages
    
    def get_unread_count(self, user_id):
        """Récupérer le nombre de messages non lus"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM messages 
            WHERE receiver_id = ? AND read = 0
        ''', (user_id,))
        
        count = cursor.fetchone()['count']
        conn.close()
        
        return count
    
    # ========== LOCALISATION ==========
    
    def save_location(self, user_id, producer_id, latitude, longitude, address=None, region=None):
        """Sauvegarder une localisation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO locations (producer_id, user_id, latitude, longitude, address, region)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producer_id, user_id, latitude, longitude, address, region))
        
        location_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'location_id': location_id}
    
    def get_locations(self, user_id=None, producer_id=None):
        """Récupérer les localisations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if producer_id:
            cursor.execute('''
                SELECT * FROM locations WHERE producer_id = ?
            ''', (producer_id,))
        elif user_id:
            cursor.execute('''
                SELECT * FROM locations WHERE user_id = ?
            ''', (user_id,))
        else:
            cursor.execute('SELECT * FROM locations')
        
        locations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return locations
    
    # ========== MÉTÉO ==========
    
    def cache_weather(self, region, latitude, longitude, temperature, humidity, precipitation, forecast_data):
        """Mettre en cache les données météo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        expires_at = datetime.now().timestamp() + 3600  # 1 heure
        
        cursor.execute('''
            INSERT OR REPLACE INTO weather_cache 
            (region, latitude, longitude, temperature, humidity, precipitation, forecast_data, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (region, latitude, longitude, temperature, humidity, precipitation, json.dumps(forecast_data), expires_at))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_cached_weather(self, region):
        """Récupérer les données météo en cache"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM weather_cache 
            WHERE region = ? AND expires_at > ?
        ''', (region, datetime.now().timestamp()))
        
        weather = cursor.fetchone()
        conn.close()
        
        if weather:
            return {
                'temperature': weather['temperature'],
                'humidity': weather['humidity'],
                'precipitation': weather['precipitation'],
                'forecast': json.loads(weather['forecast_data'])
            }
        
        return None

