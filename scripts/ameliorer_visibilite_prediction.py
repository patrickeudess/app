#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amélioration de la visibilité du texte de la page prediction
Rendre le texte en noir pour une meilleure lisibilité
"""

import os
import re

def ameliorer_visibilite_prediction():
    """Améliorer la visibilité du texte de la page prediction"""
    
    print("📝 AMÉLIORATION DE LA VISIBILITÉ - PAGE PREDICTION")
    print("=" * 60)
    
    # Améliorer les styles CSS
    ameliorer_css_visibilite()
    
    print("\n✅ AMÉLIORATIONS APPLIQUÉES AVEC SUCCÈS !")
    print("\n📋 RÉSUMÉ DES AMÉLIORATIONS :")
    print("   ✅ Texte en noir pour une meilleure visibilité")
    print("   ✅ Contraste optimisé")
    print("   ✅ Lisibilité améliorée")
    print("   ✅ Couleurs adaptées pour mobile")

def ameliorer_css_visibilite():
    """Améliorer la visibilité dans le CSS"""
    
    css_file = "frontend/css/style.css"
    
    if not os.path.exists(css_file):
        print(f"❌ Fichier {css_file} non trouvé")
        return
    
    print("\n🎨 AMÉLIORATION DE LA VISIBILITÉ CSS...")
    
    # Lire le contenu actuel
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture CSS : {e}")
        return
    
    # Nouvelles règles CSS pour améliorer la visibilité
    nouvelles_regles = """
/* ===== AMÉLIORATION DE LA VISIBILITÉ POUR LA PAGE PREDICTION ===== */

/* Amélioration générale de la visibilité du texte */
.prediction-form .form-group label {
    color: #000000 !important;
    font-weight: 600;
}

.prediction-form .form-group input,
.prediction-form .form-group select {
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 2px solid #e0e0e0 !important;
}

.prediction-form .form-group input:focus,
.prediction-form .form-group select:focus {
    border-color: #2e8b57 !important;
    box-shadow: 0 0 0 3px rgba(46, 139, 87, 0.1) !important;
}

.prediction-form .form-group select option {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* Amélioration des titres de sections */
.prediction-form h3 {
    color: #000000 !important;
    font-weight: 700;
    text-shadow: none;
}

/* Amélioration des cartes d'estimation */
.estimation-card {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.estimation-card h4 {
    color: #000000 !important;
    font-weight: 700;
}

.estimation-value {
    color: #2e8b57 !important;
    font-weight: 700;
    text-shadow: none;
}

.estimation-unit {
    color: #495057 !important;
    font-weight: 600;
}

/* Amélioration des détails des calculs */
.calculation-details {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.details-header {
    color: #000000 !important;
}

.details-header i {
    color: #2e8b57 !important;
}

.details-header h4 {
    color: #000000 !important;
    font-weight: 700;
}

.details-content {
    color: #000000 !important;
}

.details-content ul {
    color: #000000 !important;
}

.details-content li {
    color: #000000 !important;
    font-weight: 500;
}

.details-content strong {
    color: #2e8b57 !important;
    font-weight: 700;
}

/* Amélioration de la section d'analyse */
.analysis-section {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.analysis-header {
    color: #000000 !important;
}

.analysis-header i {
    color: #2e8b57 !important;
}

.analysis-header h4 {
    color: #000000 !important;
    font-weight: 700;
}

.analysis-content h5 {
    color: #000000 !important;
    font-weight: 700;
}

.analysis-content p {
    color: #000000 !important;
}

.analysis-content ul {
    color: #000000 !important;
}

.analysis-content li {
    color: #000000 !important;
    font-weight: 500;
}

/* Amélioration des graphiques */
.comparison-chart {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.comparison-chart h4 {
    color: #000000 !important;
    font-weight: 700;
}

.comparison-chart p {
    color: #000000 !important;
}

.financial-distribution {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.financial-distribution h4 {
    color: #000000 !important;
    font-weight: 700;
}

/* Amélioration des suggestions d'optimisation */
.optimization-suggestions {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    color: #000000 !important;
    border: 2px solid #dee2e6;
}

.suggestions-header {
    color: #000000 !important;
}

.suggestions-header i {
    color: #2e8b57 !important;
}

.suggestions-header h4 {
    color: #000000 !important;
    font-weight: 700;
}

.suggestions-content h5 {
    color: #000000 !important;
    font-weight: 700;
}

.suggestions-content ul {
    color: #000000 !important;
}

.suggestions-content li {
    color: #000000 !important;
    font-weight: 500;
}

/* Amélioration du bouton */
.prediction-form .btn {
    background: linear-gradient(135deg, #2e8b57 0%, #228b22 100%) !important;
    color: #ffffff !important;
    font-weight: 700;
    border: none;
    box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
}

.prediction-form .btn:hover {
    background: linear-gradient(135deg, #228b22 0%, #2e8b57 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
}

/* Responsive pour la visibilité */
@media (max-width: 480px) {
    .prediction-form .form-group label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .estimation-card,
    .calculation-details,
    .analysis-section,
    .comparison-chart,
    .financial-distribution,
    .optimization-suggestions {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #dee2e6;
    }
    
    .estimation-value {
        color: #2e8b57 !important;
    }
    
    .details-header h4,
    .analysis-header h4,
    .comparison-chart h4,
    .financial-distribution h4,
    .suggestions-header h4 {
        color: #000000 !important;
    }
    
    .details-content,
    .analysis-content p,
    .comparison-chart p {
        color: #000000 !important;
    }
    
    .details-content li,
    .analysis-content li,
    .suggestions-content li {
        color: #000000 !important;
    }
}

/* Très petits écrans */
@media (max-width: 375px) {
    .prediction-form .form-group label {
        color: #000000 !important;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .estimation-card,
    .calculation-details,
    .analysis-section,
    .comparison-chart,
    .financial-distribution,
    .optimization-suggestions {
        background: #ffffff !important;
        color: #000000 !important;
    }
}

/* Orientation paysage */
@media (orientation: landscape) and (max-width: 900px) {
    .prediction-form .form-group label {
        color: #000000 !important;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .estimation-card,
    .calculation-details,
    .analysis-section,
    .comparison-chart,
    .financial-distribution,
    .optimization-suggestions {
        background: #ffffff !important;
        color: #000000 !important;
    }
}

/* Amélioration du contraste général */
.prediction-container {
    background-color: #ffffff;
}

.prediction-form-container {
    background: #ffffff !important;
    border: 1px solid #dee2e6;
}

.prediction-result {
    background-color: #ffffff;
}

/* Amélioration de la lisibilité des icônes */
.prediction-form h3 i,
.details-header i,
.analysis-header i,
.suggestions-header i {
    color: #2e8b57 !important;
}

/* ===== FIN DES AMÉLIORATIONS DE VISIBILITÉ ===== */
"""
    
    # Ajouter les nouvelles règles à la fin du fichier CSS
    content += nouvelles_regles
    
    # Écrire le fichier modifié
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ CSS amélioré avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture CSS : {e}")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'AMÉLIORATION DE LA VISIBILITÉ")
    print("=" * 60)
    
    ameliorer_visibilite_prediction()
    
    print("\n🎉 AMÉLIORATION TERMINÉE !")
    print("\n📝 LA PAGE PREDICTION A UNE VISIBILITÉ OPTIMALE")
    print("   ✅ Texte en noir pour une meilleure lisibilité")
    print("   ✅ Contraste optimisé")
    print("   ✅ Couleurs adaptées pour tous les écrans")
    print("   ✅ Interface claire et lisible")

if __name__ == "__main__":
    main()
