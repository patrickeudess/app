import requests
import json

# Test de l'API avec les mêmes paramètres que Streamlit
def test_api():
    print("🌱 Test de l'API Mon Cacao avec paramètres Streamlit")
    print("=" * 50)
    
    # URL de l'API
    base_url = "http://localhost:5000"
    
    try:
        # Test 1: Vérifier que l'API est en ligne
        print("1. Test de connexion...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API en ligne")
        else:
            print("❌ API hors ligne")
            return
        
        # Test 2: Récupérer les paramètres attendus
        print("\n2. Récupération des paramètres...")
        response = requests.get(f"{base_url}/streamlit-params")
        if response.status_code == 200:
            params = response.json()
            print("✅ Paramètres récupérés")
            print(f"   Paramètres requis: {len(params['required_parameters'])}")
        else:
            print("❌ Impossible de récupérer les paramètres")
            return
        
        # Test 3: Test de prédiction avec données Streamlit
        print("\n3. Test de prédiction...")
        
        # Données de test identiques à Streamlit
        test_data = {
            "age_verger": 15.0,
            "agroforest": "Non",
            "engrais": "Oui",
            "fumier": "Non",
            "maladie": "Non",
            "herbicide": "Non",
            "insecticide": "Oui",
            "fongicide": "Non",
            "cout_prod": 450000.0,
            "prix_a": 750000.0,
            "region": "Indenie-Djuablin",
            "pluviometrie": "Moyenne",
            "sexe": "Masculin",
            "competences": "oui, lire et écrire"
        }
        
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                prediction = result['prediction']
                print("✅ Prédiction réussie!")
                print(f"   Productivité: {prediction['productivity_t_ha']} t/ha")
                print(f"   Revenu: {prediction['revenue_fcfa']} FCFA")
                print(f"   Bénéfice: {prediction['benefit_fcfa']} FCFA")
                print(f"   Confiance: {prediction['confidence']}%")
                print(f"   Recommandation: {prediction['recommendation']}")
            else:
                print("❌ Erreur dans la prédiction")
                print(f"   Erreur: {result.get('error', 'Inconnue')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"   Réponse: {response.text}")
        
        # Test 4: Informations sur le modèle
        print("\n4. Informations sur le modèle...")
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            model_info = response.json()
            print("✅ Informations modèle récupérées")
            print(f"   Type: {model_info['model_type']}")
            print(f"   Features: {len(model_info['features'])}")
            print(f"   Compatible Streamlit: {model_info.get('streamlit_compatible', False)}")
        else:
            print("❌ Impossible de récupérer les infos modèle")
        
        print("\n" + "=" * 50)
        print("🎉 Tests terminés!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("   Vérifiez que l'API est démarrée sur http://localhost:5000")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_api()
