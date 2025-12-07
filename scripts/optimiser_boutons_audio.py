#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimisation des boutons audio
Garder seulement les boutons sur les questions et labels
"""

import os

def optimiser_boutons_audio():
    """Optimiser les boutons audio pour une meilleure interface"""
    
    print("🎤 OPTIMISATION DES BOUTONS AUDIO")
    print("=" * 50)
    
    # Script audio optimisé
    script_audio_optimise = '''
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
        
        // Fonction pour lire les labels (questions)
        function lireLabel(element) {
            const texte = element.textContent || element.innerText;
            lireTexte(texte);
        }
        
        // Ajouter les boutons audio seulement sur les labels (questions)
        document.addEventListener('DOMContentLoaded', function() {
            // Ajouter des boutons audio seulement aux labels (questions)
            const labels = document.querySelectorAll('label');
            labels.forEach(label => {
                if (!label.querySelector('.btn-audio')) {
                    const btnAudio = document.createElement('button');
                    btnAudio.className = 'btn-audio btn-audio-label';
                    btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                    btnAudio.title = 'Écouter la question';
                    btnAudio.onclick = () => lireLabel(label);
                    label.appendChild(btnAudio);
                }
            });
            
            // Ajouter un bouton audio pour le titre principal de la page
            const titrePrincipal = document.querySelector('h1');
            if (titrePrincipal && !titrePrincipal.querySelector('.btn-audio')) {
                const btnAudio = document.createElement('button');
                btnAudio.className = 'btn-audio btn-audio-titre';
                btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                btnAudio.title = 'Écouter le titre';
                btnAudio.onclick = () => lireLabel(titrePrincipal);
                titrePrincipal.appendChild(btnAudio);
            }
        });
    </script>'''
    
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
            print(f"🎵 Optimisation audio dans {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier} : {e}")
                continue
            
            # Supprimer l'ancien script audio s'il existe
            if '// Fonction pour lire le texte à haute voix' in content:
                # Trouver et supprimer l'ancien script
                start_marker = '// Fonction pour lire le texte à haute voix'
                end_marker = '</script>'
                
                start_pos = content.find(start_marker)
                if start_pos != -1:
                    end_pos = content.find(end_marker, start_pos)
                    if end_pos != -1:
                        old_script = content[start_pos:end_pos + 8]
                        content = content.replace(old_script, '')
            
            # Insérer le nouveau script optimisé avant la fermeture de </head>
            if '</head>' in content and script_audio_optimise not in content:
                content = content.replace('</head>', script_audio_optimise + '\n</head>')
            
            # Écrire le fichier modifié
            try:
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Audio optimisé dans {fichier}")
            except Exception as e:
                print(f"❌ Erreur écriture {fichier} : {e}")

def optimiser_css_audio():
    """Optimiser le CSS pour les boutons audio réduits"""
    
    print("\n🎨 OPTIMISATION DU CSS AUDIO...")
    
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
    
    # Nouvelles règles CSS optimisées pour les boutons audio
    nouvelles_regles = """
/* ===== BOUTONS AUDIO OPTIMISÉS ===== */

/* Style général des boutons audio */
.btn-audio {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 28px;
    height: 28px;
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

/* Bouton audio pour le titre principal */
.btn-audio-titre {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    width: 32px;
    height: 32px;
    font-size: 13px;
}

.btn-audio-titre:hover {
    background: linear-gradient(135deg, #1976D2 0%, #2196F3 100%);
}

.btn-audio-titre i {
    font-size: 13px;
}

/* Boutons audio pour les labels (questions) */
.btn-audio-label {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    width: 26px;
    height: 26px;
    font-size: 11px;
}

.btn-audio-label:hover {
    background: linear-gradient(135deg, #F57C00 0%, #FF9800 100%);
}

.btn-audio-label i {
    font-size: 11px;
}

/* Responsive pour les boutons audio */
@media (max-width: 480px) {
    .btn-audio {
        width: 24px;
        height: 24px;
        font-size: 10px;
        margin-left: 6px;
    }
    
    .btn-audio-titre {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }
    
    .btn-audio-label {
        width: 22px;
        height: 22px;
        font-size: 9px;
    }
}

@media (max-width: 375px) {
    .btn-audio {
        width: 22px;
        height: 22px;
        font-size: 9px;
        margin-left: 4px;
    }
    
    .btn-audio-titre {
        width: 26px;
        height: 26px;
        font-size: 11px;
    }
    
    .btn-audio-label {
        width: 20px;
        height: 20px;
        font-size: 8px;
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

/* ===== FIN DES BOUTONS AUDIO OPTIMISÉS ===== */
"""
    
    # Supprimer l'ancien CSS audio s'il existe
    if '/* ===== BOUTONS AUDIO POUR L\'ACCESSIBILITÉ ===== */' in content:
        start_marker = '/* ===== BOUTONS AUDIO POUR L\'ACCESSIBILITÉ ===== */'
        end_marker = '/* ===== FIN DES BOUTONS AUDIO ===== */'
        
        start_pos = content.find(start_marker)
        if start_pos != -1:
            end_pos = content.find(end_marker, start_pos)
            if end_pos != -1:
                old_css = content[start_pos:end_pos + len(end_marker)]
                content = content.replace(old_css, '')
    
    # Ajouter les nouvelles règles optimisées
    content += nouvelles_regles
    
    # Écrire le fichier modifié
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ CSS audio optimisé avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture CSS : {e}")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'OPTIMISATION DES BOUTONS AUDIO")
    print("=" * 50)
    
    optimiser_boutons_audio()
    optimiser_css_audio()
    
    print("\n🎉 OPTIMISATION TERMINÉE !")
    print("\n🎤 INTERFACE AUDIO OPTIMISÉE")
    print("   ✅ Boutons audio seulement sur les questions")
    print("   ✅ Bouton audio sur le titre principal")
    print("   ✅ Interface plus propre et moins encombrée")
    print("   ✅ Meilleure expérience utilisateur")

if __name__ == "__main__":
    main()
