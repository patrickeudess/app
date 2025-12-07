#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réduction des boutons audio
Garder seulement sur les questions et labels
"""

import os

def reduire_boutons_audio():
    """Réduire les boutons audio pour une meilleure interface"""
    
    print("🎤 RÉDUCTION DES BOUTONS AUDIO")
    print("=" * 40)
    
    # Script audio simplifié
    script_simple = '''
    <script>
        function lireTexte(texte) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(texte);
                utterance.lang = 'fr-FR';
                utterance.rate = 0.8;
                speechSynthesis.speak(utterance);
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            // Boutons audio seulement sur les labels (questions)
            const labels = document.querySelectorAll('label');
            labels.forEach(label => {
                if (!label.querySelector('.btn-audio')) {
                    const btnAudio = document.createElement('button');
                    btnAudio.className = 'btn-audio';
                    btnAudio.innerHTML = '<i class="fas fa-volume-up"></i>';
                    btnAudio.title = 'Écouter';
                    btnAudio.onclick = () => lireTexte(label.textContent);
                    label.appendChild(btnAudio);
                }
            });
        });
    </script>'''
    
    # Fichiers à modifier
    fichiers = [
        "frontend/index.html",
        "frontend/prediction.html",
        "frontend/soumettre.html",
        "frontend/historique.html",
        "frontend/analyse.html",
        "frontend/conseils.html",
        "frontend/assistant.html",
        "frontend/score-ecologique.html"
    ]
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            print(f"🎵 Optimisation de {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier}")
                continue
            
            # Supprimer l'ancien script audio
            if '// Fonction pour lire le texte à haute voix' in content:
                start = content.find('// Fonction pour lire le texte à haute voix')
                end = content.find('</script>', start) + 8
                content = content[:start] + content[end:]
            
            # Ajouter le nouveau script simple
            if '</head>' in content and script_simple not in content:
                content = content.replace('</head>', script_simple + '\n</head>')
            
            # Écrire le fichier
            try:
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {fichier} optimisé")
            except Exception as e:
                print(f"❌ Erreur écriture {fichier}")

def main():
    """Fonction principale"""
    print("🚀 RÉDUCTION DES BOUTONS AUDIO")
    print("=" * 40)
    
    reduire_boutons_audio()
    
    print("\n🎉 OPTIMISATION TERMINÉE !")
    print("✅ Boutons audio seulement sur les questions")
    print("✅ Interface plus propre")

if __name__ == "__main__":
    main()
