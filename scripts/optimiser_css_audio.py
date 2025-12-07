#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimisation du CSS pour les boutons audio réduits
"""

import os

def optimiser_css_audio():
    """Optimiser le CSS pour les boutons audio"""
    
    print("🎨 OPTIMISATION DU CSS AUDIO")
    print("=" * 40)
    
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
    
    # CSS optimisé pour les boutons audio
    css_optimise = """
/* ===== BOUTONS AUDIO OPTIMISÉS ===== */

.btn-audio {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 26px;
    height: 26px;
    font-size: 11px;
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
    background: linear-gradient(135deg, #F57C00 0%, #FF9800 100%);
    transform: scale(1.1);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.btn-audio:active {
    transform: scale(0.95);
}

.btn-audio i {
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
}

@media (max-width: 375px) {
    .btn-audio {
        width: 22px;
        height: 22px;
        font-size: 9px;
        margin-left: 4px;
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
    outline: 2px solid #FF9800;
    outline-offset: 2px;
}

/* Tooltip pour les boutons audio */
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
    if '/* ===== BOUTONS AUDIO' in content:
        start_marker = '/* ===== BOUTONS AUDIO'
        end_marker = '/* ===== FIN DES BOUTONS AUDIO ===== */'
        
        start_pos = content.find(start_marker)
        if start_pos != -1:
            end_pos = content.find(end_marker, start_pos)
            if end_pos != -1:
                old_css = content[start_pos:end_pos + len(end_marker)]
                content = content.replace(old_css, '')
    
    # Ajouter le nouveau CSS optimisé
    content += css_optimise
    
    # Écrire le fichier modifié
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ CSS audio optimisé avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture CSS : {e}")

def main():
    """Fonction principale"""
    print("🚀 OPTIMISATION DU CSS AUDIO")
    print("=" * 40)
    
    optimiser_css_audio()
    
    print("\n🎉 CSS OPTIMISÉ !")
    print("✅ Boutons audio plus discrets")
    print("✅ Interface plus propre")

if __name__ == "__main__":
    main()
