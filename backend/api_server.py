from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import os
import numpy as np
from database import Database
import pyotp
from pdf_generator import PDFGenerator
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin pour le frontend

# Initialiser la base de données
db = Database()

# Charger le modèle XGBoost
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_productivite_xgb.pkl")
try:
xgb_model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
except:
    MODEL_LOADED = False
    print("⚠️ Modèle XGBoost non trouvé. Les prédictions utiliseront le mode simulation.")

# ========== ROUTES D'AUTHENTIFICATION ==========

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')
    email = data.get('email')
    phone = data.get('phone')
    region = data.get('region')
    
    if not username or not password or not user_type:
        return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
    
    result = db.create_user(username, password, user_type, email, phone, region)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur"""
    data = request.get_json()
    
    identifier = data.get('identifier')  # email, phone ou username
    password = data.get('password')
    two_factor_token = data.get('two_factor_token')
    
    if not identifier or not password:
        return jsonify({'success': False, 'error': 'Identifiants manquants'}), 400
    
    result = db.authenticate_user(identifier, password)
    
    if not result['success']:
        return jsonify(result), 401
    
    # Vérifier si 2FA est activé
    if result['user']['two_factor_enabled']:
        if not two_factor_token:
            return jsonify({
                'success': False,
                'requires_2fa': True,
                'user_id': result['user']['id']
            }), 200
        
        # Vérifier le code 2FA
        verify_result = db.verify_2fa(result['user']['id'], two_factor_token)
        if not verify_result['success']:
            return jsonify(verify_result), 401
    
    return jsonify(result), 200

@app.route('/api/auth/enable-2fa', methods=['POST'])
def enable_2fa():
    """Activer l'authentification à deux facteurs"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id requis'}), 400
    
    result = db.enable_2fa(user_id)
    return jsonify(result), 200

@app.route('/api/auth/verify-2fa', methods=['POST'])
def verify_2fa():
    """Vérifier un code 2FA"""
    data = request.get_json()
    user_id = data.get('user_id')
    token = data.get('token')
    
    if not user_id or not token:
        return jsonify({'success': False, 'error': 'user_id et token requis'}), 400
    
    result = db.verify_2fa(user_id, token)
    return jsonify(result), 200

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Demander une réinitialisation de mot de passe"""
    data = request.get_json()
    identifier = data.get('identifier')
    
    if not identifier:
        return jsonify({'success': False, 'error': 'Identifiant requis'}), 400
    
    result = db.generate_reset_token(identifier)
    return jsonify(result), 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Réinitialiser le mot de passe"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'success': False, 'error': 'Token et nouveau mot de passe requis'}), 400
    
    result = db.reset_password(token, new_password)
    return jsonify(result), 200

# ========== ROUTES PRODUCTEURS ==========

@app.route('/api/producers', methods=['POST'])
def create_producer():
    """Créer un nouveau producteur"""
    data = request.get_json()
    
    professional_id = data.get('professional_id')
    name = data.get('name')
    region = data.get('region')
    phone = data.get('phone')
    email = data.get('email')
    notes = data.get('notes')
    
    if not professional_id or not name or not region:
        return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
    
    result = db.create_producer(professional_id, name, region, phone, email, notes)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/producers/<int:professional_id>', methods=['GET'])
def get_producers(professional_id):
    """Récupérer les producteurs d'un professionnel"""
    producers = db.get_producers_by_professional(professional_id)
    return jsonify({'success': True, 'producers': producers}), 200

# ========== ROUTES SOUMISSIONS ==========

@app.route('/api/submissions', methods=['POST'])
def save_submission():
    """Sauvegarder une soumission"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    producer_id = data.get('producer_id')
    submission_data = data.get('submission_data')
    
    if not user_id or not submission_data:
        return jsonify({'success': False, 'error': 'user_id et submission_data requis'}), 400
    
    result = db.save_submission(user_id, producer_id, submission_data)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Récupérer les soumissions"""
    user_id = request.args.get('user_id', type=int)
    producer_id = request.args.get('producer_id', type=int)
    limit = request.args.get('limit', 100, type=int)
    
    submissions = db.get_submissions(user_id, producer_id, limit)
    return jsonify({'success': True, 'submissions': submissions}), 200

# ========== ROUTES CONSEILS ==========

@app.route('/api/advice', methods=['POST'])
def save_advice():
    """Sauvegarder un conseil"""
    data = request.get_json()
    
    producer_id = data.get('producer_id')
    user_id = data.get('user_id')
    advice_text = data.get('advice_text')
    category = data.get('category')
    advice_type = data.get('advice_type')
    source = data.get('source')
    
    if not user_id or not advice_text:
        return jsonify({'success': False, 'error': 'user_id et advice_text requis'}), 400
    
    result = db.save_advice(producer_id, user_id, advice_text, category, advice_type, source)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/advice/stats', methods=['GET'])
def get_advice_stats():
    """Récupérer les statistiques des conseils"""
    professional_id = request.args.get('professional_id', type=int)
    
    stats = db.get_advice_stats(professional_id)
    return jsonify({'success': True, 'stats': stats}), 200

# ========== ROUTES NOTIFICATIONS ==========

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    """Créer une notification"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    title = data.get('title')
    message = data.get('message')
    notification_type = data.get('type', 'info')
    
    if not user_id or not title or not message:
        return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
    
    result = db.create_notification(user_id, title, message, notification_type)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    """Récupérer les notifications d'un utilisateur"""
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = request.args.get('limit', 50, type=int)
    
    notifications = db.get_notifications(user_id, unread_only, limit)
    return jsonify({'success': True, 'notifications': notifications}), 200

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Marquer une notification comme lue"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'user_id requis'}), 400
    
    result = db.mark_notification_read(notification_id, user_id)
    return jsonify(result), 200

# ========== ROUTES GAMIFICATION ==========

@app.route('/api/gamification/points', methods=['POST'])
def add_points():
    """Ajouter des points à un utilisateur"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    points = data.get('points')
    reason = data.get('reason', '')
    
    if not user_id or not points:
        return jsonify({'success': False, 'error': 'user_id et points requis'}), 400
    
    result = db.add_points(user_id, points, reason)
    return jsonify(result), 200

@app.route('/api/gamification/badges', methods=['POST'])
def award_badge():
    """Attribuer un badge"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    badge_type = data.get('badge_type')
    badge_name = data.get('badge_name')
    
    if not user_id or not badge_type or not badge_name:
        return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
    
    result = db.award_badge(user_id, badge_type, badge_name)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/gamification/badges/<int:user_id>', methods=['GET'])
def get_badges(user_id):
    """Récupérer les badges d'un utilisateur"""
    badges = db.get_user_badges(user_id)
    return jsonify({'success': True, 'badges': badges}), 200

@app.route('/api/gamification/leaderboard', methods=['GET'])
def get_leaderboard():
    """Récupérer le classement"""
    limit = request.args.get('limit', 10, type=int)
    
    leaderboard = db.get_leaderboard(limit)
    return jsonify({'success': True, 'leaderboard': leaderboard}), 200

# ========== ROUTES MESSAGERIE ==========

@app.route('/api/messages', methods=['POST'])
def send_message():
    """Envoyer un message"""
    data = request.get_json()
    
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    subject = data.get('subject')
    content = data.get('content')
    
    if not sender_id or not receiver_id or not content:
        return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
    
    result = db.send_message(sender_id, receiver_id, subject, content)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    """Récupérer les messages"""
    folder = request.args.get('folder', 'inbox')
    
    messages = db.get_messages(user_id, folder)
    unread_count = db.get_unread_count(user_id)
    
    return jsonify({
        'success': True,
        'messages': messages,
        'unread_count': unread_count
    }), 200

# ========== ROUTES LOCALISATION ==========

@app.route('/api/locations', methods=['POST'])
def save_location():
    """Sauvegarder une localisation"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    producer_id = data.get('producer_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    address = data.get('address')
    region = data.get('region')
    
    if not latitude or not longitude:
        return jsonify({'success': False, 'error': 'latitude et longitude requis'}), 400
    
    result = db.save_location(user_id, producer_id, latitude, longitude, address, region)
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Récupérer les localisations"""
    user_id = request.args.get('user_id', type=int)
    producer_id = request.args.get('producer_id', type=int)
    
    locations = db.get_locations(user_id, producer_id)
    return jsonify({'success': True, 'locations': locations}), 200

# ========== ROUTES MÉTÉO ==========

@app.route('/api/weather/cache', methods=['POST'])
def cache_weather():
    """Mettre en cache les données météo"""
    data = request.get_json()
    
    region = data.get('region')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    precipitation = data.get('precipitation')
    forecast_data = data.get('forecast_data')
    
    if not region:
        return jsonify({'success': False, 'error': 'region requis'}), 400
    
    result = db.cache_weather(region, latitude, longitude, temperature, humidity, precipitation, forecast_data)
    return jsonify(result), 200

@app.route('/api/weather/<region>', methods=['GET'])
def get_weather(region):
    """Récupérer les données météo (cache ou API externe)"""
    cached = db.get_cached_weather(region)
    
    if cached:
        return jsonify({'success': True, 'data': cached, 'source': 'cache'}), 200
    
    # Si pas en cache, on retourne une structure vide (sera remplie par le frontend avec API externe)
    return jsonify({
        'success': True,
        'data': None,
        'source': 'external',
        'message': 'Utilisez une API météo externe (OpenWeatherMap, WeatherAPI)'
    }), 200

# ========== ROUTES PRÉDICTIONS (EXISTANTES) ==========

@app.route('/')
def home():
    return jsonify({
        "message": "API Mon Cacao - Modèle XGBoost",
        "version": "2.0",
        "database": "SQLite",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model_info": "/model-info",
            "auth": "/api/auth/*",
            "producers": "/api/producers",
            "submissions": "/api/submissions",
            "notifications": "/api/notifications",
            "gamification": "/api/gamification/*",
            "messages": "/api/messages",
            "locations": "/api/locations",
            "weather": "/api/weather/*"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": MODEL_LOADED,
        "database": "connected"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données du frontend
        data = request.get_json()
        
        # Validation des données - mêmes paramètres que Streamlit
        required_fields = [
            'age_verger', 'agroforest', 'engrais', 'fumier', 'maladie',
            'herbicide', 'insecticide', 'fongicide', 'cout_prod', 'prix_a',
            'region', 'pluviometrie', 'sexe', 'competences'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Champ manquant: {field}"}), 400
        
        # Utiliser le modèle si disponible, sinon simulation
        if MODEL_LOADED:
        # Création du dictionnaire de données - EXACTEMENT comme dans Streamlit
        model_data = {
            "Coût_production/ha": [data['cout_prod']],
            "Age_verger": [data['age_verger']],
            "Région": [data['region']],
            "Pluviometrie": [data['pluviometrie']],
            "Sexe": [data['sexe']],
                "Niveau_education": ["Non renseigné"],
            "Competences": [data['competences']],
            "Engrais chimique": [data['engrais']],
            "Agroforesterie": [data['agroforest']],
            "fumier/ compost": [data['fumier']],
            "Herbicide": [data['herbicide']],
            "Insecticide": [data['insecticide']],
            "Fongicide": [data['fongicide']],
            "Maladie": [data['maladie']],
        }
        
            # Création du DataFrame et prédiction
        df_input = pd.DataFrame(model_data)
        X_trans = xgb_model.named_steps["prep"].transform(df_input)
        pred = xgb_model.named_steps["model"].predict(X_trans)[0]
            production = pred  # t/ha
        else:
            # Mode simulation
            production = simulate_prediction(data)
        
        production_kg = production * 1000  # Conversion en kg/ha
        prix_vente = data['prix_a'] / 1000  # Conversion tonne vers kg (FCFA/kg)
        revenu = round(production_kg * prix_vente)  # FCFA/ha
        benefice = round(revenu - data['cout_prod'])  # FCFA/ha
        
        # Calcul de la confiance
        confidence = calculate_confidence(data)
        
        # Recommandations
        recommendation = get_recommendation(production, data)
        
        return jsonify({
            "success": True,
            "prediction": {
                "productivity_t_ha": round(production, 3),
                "productivity_kg_ha": round(production_kg),
                "revenue_fcfa": revenu,
                "benefit_fcfa": benefice,
                "confidence": confidence,
                "recommendation": recommendation,
                "price_per_kg": prix_vente,
                "cost_per_ha": data['cout_prod']
            },
            "input_data": data,
            "model_info": {
                "model_type": "XGBoost" if MODEL_LOADED else "Simulation",
                "features_used": list(data.keys())
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Erreur lors de la prédiction: {str(e)}",
            "success": False
        }), 500

def simulate_prediction(data):
    """Simulation de prédiction si le modèle n'est pas disponible"""
    base_production = 0.8  # t/ha de base
    
    # Ajustements selon les paramètres
    if data.get('engrais') == 'Oui':
        base_production *= 1.2
    if data.get('agroforest') == 'Oui':
        base_production *= 1.1
    if data.get('maladie') != 'Non':
        base_production *= 0.9
    
    age_factor = min(1.0 + (data.get('age_verger', 15) / 100), 1.3)
    base_production *= age_factor
    
    return base_production

def calculate_confidence(data):
    """Calcule un score de confiance basé sur la qualité des données"""
    confidence = 85  # Base de 85%
    
    if 0 <= data['age_verger'] <= 50:
        confidence += 5
    if data['cout_prod'] > 0:
        confidence += 5
    if data['prix_a'] > 0:
        confidence += 5
    
    return min(confidence, 95)

def get_recommendation(prediction, data):
    """Génère des recommandations basées sur la prédiction et les données"""
    recommendations = []
    
    if prediction < 0.8:
        recommendations.append("Productivité faible - Optimisez l'utilisation des engrais")
        recommendations.append("Vérifiez l'état sanitaire des plants")
    elif prediction > 1.2:
        recommendations.append("Excellente productivité - Maintenez vos bonnes pratiques")
    else:
        recommendations.append("Productivité moyenne - Quelques améliorations possibles")
    
    if data['engrais'] == "Non":
        recommendations.append("Envisagez l'utilisation d'engrais pour améliorer la productivité")
    
    if data['agroforest'] == "Non":
        recommendations.append("L'agroforesterie peut améliorer la résilience de votre plantation")
    
    if data['maladie'] != "Non":
        recommendations.append("Surveillez et traitez les maladies pour maintenir la productivité")
    
    return "; ".join(recommendations[:3])

# ========== ROUTES PDF ==========

@app.route('/api/pdf/report/professional/<int:professional_id>', methods=['GET'])
def generate_professional_pdf(professional_id):
    """Générer un rapport PDF pour un professionnel"""
    generator = PDFGenerator()
    pdf_buffer = BytesIO()
    generator.generate_professional_report(professional_id, pdf_buffer)
    pdf_buffer.seek(0)
    
    filename = f"rapport_professionnel_{professional_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/pdf/report/producer/<int:producer_id>', methods=['GET'])
def generate_producer_pdf(producer_id):
    """Générer un rapport PDF pour un producteur"""
    generator = PDFGenerator()
    pdf_buffer = BytesIO()
    generator.generate_producer_report(producer_id, pdf_buffer)
    pdf_buffer.seek(0)
    
    filename = f"rapport_producteur_{producer_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@app.route('/model-info')
def model_info():
    """Retourne des informations sur le modèle"""
    return jsonify({
        "model_type": "XGBoost" if MODEL_LOADED else "Simulation",
        "features": [
            "Coût_production/ha",
            "Age_verger", 
            "Région",
            "Pluviometrie",
            "Sexe",
            "Niveau_education",
            "Competences",
            "Engrais chimique",
            "Agroforesterie",
            "fumier/ compost",
            "Herbicide",
            "Insecticide",
            "Fongicide",
            "Maladie"
        ],
        "output": "Productivité (t/ha)",
        "preprocessing": "StandardScaler + OneHotEncoder",
        "streamlit_compatible": True
    })

if __name__ == '__main__':
    print("🌱 Démarrage de l'API Mon Cacao v2.0...")
    print(f"📦 Modèle chargé: {MODEL_LOADED}")
    print("💾 Base de données: SQLite")
    print("🚀 Serveur API disponible sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
