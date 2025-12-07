#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amélioration du langage et ajout des options audio
- Langage simple adapté à un faible niveau scolaire
- Options audio pour écouter les versions vocales
"""

import os
import re

def ameliorer_langage_et_audio():
    """Améliorer le langage et ajouter les options audio"""
    
    print("🎤 AMÉLIORATION DU LANGAGE ET AJOUT AUDIO")
    print("=" * 60)
    
    # 1. Améliorer le langage dans tous les fichiers HTML
    ameliorer_langage_simple()
    
    # 2. Ajouter les options audio
    ajouter_options_audio()
    
    # 3. Améliorer le CSS pour les boutons audio
    ameliorer_css_audio()
    
    print("\n✅ AMÉLIORATIONS APPLIQUÉES AVEC SUCCÈS !")
    print("\n📋 RÉSUMÉ DES AMÉLIORATIONS :")
    print("   ✅ Langage simple et clair")
    print("   ✅ Options audio pour écouter")
    print("   ✅ Interface adaptée au niveau scolaire")
    print("   ✅ Boutons audio visibles")

def ameliorer_langage_simple():
    """Améliorer le langage pour le rendre plus simple"""
    
    print("\n📝 AMÉLIORATION DU LANGAGE...")
    
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
        'Prix de vente du cacao (Fcfa/Kg)': 'Prix de vente du cacao (Fcfa/Kg)',
        'Ma Région et le Climat': 'Ma région et la pluie',
        'Région': 'Ma région',
        'Niveau de pluviométrie': 'Combien il pleut',
        'Mes Informations Personnelles': 'Mes informations',
        'Je suis': 'Je suis',
        'Je sais lire et écrire': 'Je sais lire et écrire',
        'Calculer ma récolte': 'Calculer ma récolte',
        
        # Résultats
        'Production Estimée': 'Récolte prévue',
        'Revenu Potentiel': 'Gains possibles',
        'Bénéfice Estimé': 'Profit prévu',
        'Détails des calculs': 'Comment j\'ai calculé',
        'Analyse détaillée et recommandations': 'Étude et conseils',
        'Analyse de la productivité': 'Étude de ma récolte',
        'Recommandations': 'Conseils',
        'Suggestions d\'optimisation': 'Comment faire mieux',
        'Pistes d\'amélioration': 'Comment améliorer',
        
        # Options
        'Oui': 'Oui',
        'Non': 'Non',
        'Un peu': 'Un peu',
        'Faible': 'Peu',
        'Moyenne': 'Moyen',
        'Élevée': 'Beaucoup',
        'Un homme': 'Un homme',
        'Une femme': 'Une femme',
        'Oui, je sais': 'Oui, je sais',
        'Lire seulement': 'Lire seulement',
        'Non, je ne sais pas': 'Non, je ne sais pas',
        
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
        'Certification': 'Certificat de qualité',
        
        # Notations
        'Aucun arbre': 'Aucun arbre',
        'Faible (<10 arbres/ha)': 'Peu d\'arbres (moins de 10 par hectare)',
        'Moyen (10–29 arbres/ha)': 'Moyen (10 à 29 arbres par hectare)',
        'Bon (≥30 arbres/ha)': 'Beaucoup (30 arbres ou plus par hectare)',
        'Sol nu': 'Sol sans rien',
        'Couverture partielle': 'Sol partiellement couvert',
        'Couverture bonne': 'Sol bien couvert',
        'Bande tampon existe': 'Bande de protection présente',
        'Parcelle en zone interdite': 'Terrain dans une zone interdite',
        'Emballages collectés': 'Déchets bien ramassés',
        'Producteur certifié': 'Producteur avec certificat'
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

def ajouter_options_audio():
    """Ajouter les options audio dans tous les fichiers"""
    
    print("\n🎤 AJOUT DES OPTIONS AUDIO...")
    
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
            print(f"🎵 Ajout audio dans {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier} : {e}")
                continue
            
            # Ajouter le script audio dans le head
            script_audio = '''
    <script>
        // Fonction pour lire le texte à haute voix
        function lireTexte(texte) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(texte);
                utterance.lang = 'fr-FR';
                utterance.rate = 0.8; // Vitesse plus lente
                utterance.pitch = 1.0;
                speechSynthesis.speak(utterance);
            } else {
                alert('Votre navigateur ne supporte pas la lecture vocale');
            }
        }
        
        // Fonction pour lire les titres
        function lireTitre(element) {
            const texte = element.textContent || element.innerText;
            lireTexte(texte);
        }
        
        // Fonction pour lire les labels
        function lireLabel(element) {
            const texte = element.textContent || element.innerText;
            lireTexte(texte);
        }
        
        // Fonction pour lire les descriptions
        function lireDescription(element) {
            const texte = element.textContent || element.innerText;
            lireTexte(texte);
        }
        
        // Ajouter les boutons audio automatiquement
        document.addEventListener('DOMContentLoaded', function() {
            // Ajouter des boutons audio aux titres
            const titres = document.querySelectorAll('h1, h2, h3, h4, h5');
            titres.forEach(titre => {
                if (!titre.querySelector('.btn-audio')) {
                    const btnAudio = document.createElement('button');
                    btnAudio.className = 'btn-audio btn-audio-titre';
                    btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                    btnAudio.title = 'Écouter';
                    btnAudio.onclick = () => lireTitre(titre);
                    titre.appendChild(btnAudio);
                }
            });
            
            // Ajouter des boutons audio aux labels
            const labels = document.querySelectorAll('label');
            labels.forEach(label => {
                if (!label.querySelector('.btn-audio')) {
                    const btnAudio = document.createElement('button');
                    btnAudio.className = 'btn-audio btn-audio-label';
                    btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                    btnAudio.title = 'Écouter';
                    btnAudio.onclick = () => lireLabel(label);
                    label.appendChild(btnAudio);
                }
            });
            
            // Ajouter des boutons audio aux descriptions
            const descriptions = document.querySelectorAll('p');
            descriptions.forEach(desc => {
                if (!desc.querySelector('.btn-audio') && desc.textContent.trim().length > 20) {
                    const btnAudio = document.createElement('button');
                    btnAudio.className = 'btn-audio btn-audio-desc';
                    btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                    btnAudio.title = 'Écouter';
                    btnAudio.onclick = () => lireDescription(desc);
                    desc.appendChild(btnAudio);
                }
            });
        });
    </script>'''
            
            # Insérer le script avant la fermeture de </head>
            if '</head>' in content and script_audio not in content:
                content = content.replace('</head>', script_audio + '\n</head>')
            
            # Écrire le fichier modifié
            try:
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Audio ajouté dans {fichier}")
            except Exception as e:
                print(f"❌ Erreur écriture {fichier} : {e}")

def ameliorer_css_audio():
    """Améliorer le CSS pour les boutons audio"""
    
    print("\n🎨 AMÉLIORATION DU CSS AUDIO...")
    
    css_file = "frontend/css/style.css"
    
    if not os.path.exists(css_file):
        print(f"❌ Fichier {css_file} non trouvé")
        return
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture CSS : {e}")
        return
    
    # Nouvelles règles CSS pour les boutons audio
    nouvelles_regles = """
/* ===== BOUTONS AUDIO POUR L'ACCESSIBILITÉ ===== */

/* Style général des boutons audio */
.btn-audio {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    font-size: 12px;
    cursor: pointer;
    margin-left: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    position: relative;
    z-index: 10;
}

.btn-audio:hover {
    background: linear-gradient(135deg, #45a049 0%, #4CAF50 100%);
    transform: scale(1.1);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.btn-audio:active {
    transform: scale(0.95);
}

.btn-audio i {
    font-size: 12px;
}

/* Boutons audio pour les titres */
.btn-audio-titre {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    width: 35px;
    height: 35px;
    font-size: 14px;
}

.btn-audio-titre:hover {
    background: linear-gradient(135deg, #1976D2 0%, #2196F3 100%);
}

.btn-audio-titre i {
    font-size: 14px;
}

/* Boutons audio pour les labels */
.btn-audio-label {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    width: 28px;
    height: 28px;
    font-size: 11px;
}

.btn-audio-label:hover {
    background: linear-gradient(135deg, #F57C00 0%, #FF9800 100%);
}

.btn-audio-label i {
    font-size: 11px;
}

/* Boutons audio pour les descriptions */
.btn-audio-desc {
    background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%);
    width: 32px;
    height: 32px;
    font-size: 13px;
}

.btn-audio-desc:hover {
    background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 100%);
}

.btn-audio-desc i {
    font-size: 13px;
}

/* Responsive pour les boutons audio */
@media (max-width: 480px) {
    .btn-audio {
        width: 28px;
        height: 28px;
        font-size: 11px;
        margin-left: 6px;
    }
    
    .btn-audio-titre {
        width: 32px;
        height: 32px;
        font-size: 13px;
    }
    
    .btn-audio-label {
        width: 26px;
        height: 26px;
        font-size: 10px;
    }
    
    .btn-audio-desc {
        width: 30px;
        height: 30px;
        font-size: 12px;
    }
}

@media (max-width: 375px) {
    .btn-audio {
        width: 26px;
        height: 26px;
        font-size: 10px;
        margin-left: 4px;
    }
    
    .btn-audio-titre {
        width: 30px;
        height: 30px;
        font-size: 12px;
    }
    
    .btn-audio-label {
        width: 24px;
        height: 24px;
        font-size: 9px;
    }
    
    .btn-audio-desc {
        width: 28px;
        height: 28px;
        font-size: 11px;
    }
}

/* Animation pour les boutons audio */
@keyframes pulse-audio {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.btn-audio:focus {
    animation: pulse-audio 0.3s ease-in-out;
    outline: 2px solid #4CAF50;
    outline-offset: 2px;
}

/* Amélioration de l'accessibilité */
.btn-audio[title] {
    position: relative;
}

.btn-audio[title]:hover::after {
    content: attr(title);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 1000;
    margin-bottom: 5px;
}

/* ===== FIN DES BOUTONS AUDIO ===== */
"""
    
    # Ajouter les nouvelles règles à la fin du fichier CSS
    content += nouvelles_regles
    
    # Écrire le fichier modifié
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ CSS audio amélioré avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture CSS : {e}")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'AMÉLIORATION DU LANGAGE ET AUDIO")
    print("=" * 60)
    
    ameliorer_langage_et_audio()
    
    print("\n🎉 AMÉLIORATION TERMINÉE !")
    print("\n📝 L'APPLICATION A UN LANGAGE SIMPLE ET DES OPTIONS AUDIO")
    print("   ✅ Langage adapté au niveau scolaire")
    print("   ✅ Boutons audio pour écouter")
    print("   ✅ Interface plus accessible")
    print("   ✅ Textes plus clairs et simples")

if __name__ == "__main__":
    main()
