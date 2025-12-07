#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amélioration du langage pour le rendre plus simple
Adapté à un faible niveau scolaire
"""

import os

def ameliorer_langage_simple():
    """Améliorer le langage pour le rendre plus simple"""
    
    print("📝 AMÉLIORATION DU LANGAGE SIMPLE")
    print("=" * 50)
    
    # Dictionnaire des remplacements pour simplifier le langage
    remplacements = {
        # Titres et sections
        'Fonctionnalités': 'Outils',
        'Prédiction': 'Estimation',
        'Productivité + Revenus + Recommandations': 'Estimer ma récolte et mes gains',
        'Soumettre': 'Enregistrer',
        'Données de production régulières': 'Mes informations de récolte',
        'Historique': 'Mes enregistrements',
        'Données saisies précédemment': 'Ce que j\'ai noté avant',
        'Analyse': 'Étude',
        'Analysez vos données de production': 'Regarder mes informations',
        'Conseils': 'Aide',
        'Conseils personnalisés': 'Aide pour moi',
        'Assistant IA': 'Aide intelligent',
        'Assistant intelligent pour vos questions': 'Posez vos questions',
        'Score Écologique': 'Note environnement',
        'Évaluez votre impact environnemental': 'Voir si je respecte la nature',
        
        # Formulaire de prédiction
        'Mes Informations de Plantation': 'Ma plantation',
        'Âge du verger (années)': 'Depuis combien d\'années j\'ai planté',
        'Agroforesterie': 'J\'ai des arbres avec le cacao',
        'Engrais chimique': 'J\'utilise des engrais chimiques',
        'Fumier / Compost': 'J\'utilise du fumier ou compost',
        'Présence de maladies': 'Mes plants sont malades',
        'Utilisation d\'herbicides': 'J\'utilise des produits contre les mauvaises herbes',
        'Utilisation d\'insecticides': 'J\'utilise des produits contre les insectes',
        'Utilisation de fongicides': 'J\'utilise des produits contre les champignons',
        'Mes Coûts et Prix': 'Mes dépenses et prix',
        'Combien je dépense par hectare (FCFA)': 'Combien je dépense par hectare',
        'Ma Région et le Climat': 'Ma région et la pluie',
        'Niveau de pluviométrie': 'Combien il pleut',
        'Mes Informations Personnelles': 'Mes informations',
        'Je sais lire et écrire': 'Je sais lire et écrire',
        
        # Résultats
        'Production Estimée': 'Récolte prévue',
        'Revenu Potentiel': 'Gains possibles',
        'Bénéfice Estimé': 'Profit prévu',
        'Détails des calculs': 'Comment j\'ai calculé',
        'Analyse détaillée et recommandations': 'Étude et conseils',
        'Analyse de la productivité': 'Étude de ma récolte',
        'Suggestions d\'optimisation': 'Comment faire mieux',
        'Pistes d\'amélioration': 'Comment améliorer',
        
        # Messages
        'Connecté': 'En ligne',
        'Déconnexion': 'Quitter',
        'Retour': 'Retour',
        'En ligne': 'En ligne',
        'Agriculteur': 'Agriculteur',
        
        # Score écologique
        'Arbres d\'ombrage': 'Arbres pour l\'ombre',
        'Couverture du sol': 'Sol couvert',
        'Fertilisation': 'Engrais',
        'Pesticides': 'Produits contre les maladies',
        'Taille sanitaire': 'Couper les branches malades',
        'Protection berges': 'Protéger les bords',
        'Gestion déchets': 'Gérer les déchets',
        'Biodiversité': 'Différents animaux et plantes',
        'Déforestation': 'Couper les arbres',
        'Certification': 'Certificat de qualité'
    }
    
    # Fichiers HTML à modifier
    fichiers_html = [
        "frontend/index.html",
        "frontend/prediction.html",
        "frontend/soumettre.html",
        "frontend/historique.html",
        "frontend/analyse.html",
        "frontend/conseils.html",
        "frontend/assistant.html",
        "frontend/score-ecologique.html"
    ]
    
    for fichier in fichiers_html:
        if os.path.exists(fichier):
            print(f"🔧 Amélioration de {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier} : {e}")
                continue
            
            # Appliquer les remplacements
            for ancien, nouveau in remplacements.items():
                content = content.replace(ancien, nouveau)
            
            # Écrire le fichier modifié
            try:
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {fichier} amélioré")
            except Exception as e:
                print(f"❌ Erreur écriture {fichier} : {e}")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'AMÉLIORATION DU LANGAGE")
    print("=" * 50)
    
    ameliorer_langage_simple()
    
    print("\n🎉 LANGAGE AMÉLIORÉ !")
    print("\n📝 L'APPLICATION UTILISE MAINTENANT UN LANGAGE SIMPLE")
    print("   ✅ Textes adaptés au niveau scolaire")
    print("   ✅ Termes plus clairs et compréhensibles")
    print("   ✅ Interface plus accessible")

if __name__ == "__main__":
    main()
