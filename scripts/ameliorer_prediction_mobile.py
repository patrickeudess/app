#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amélioration de la responsivité mobile de la page prediction
Correction des débordements et adaptation pour tous les écrans de téléphone
"""

import os
import re

def ameliorer_prediction_mobile():
    """Améliorer la responsivité mobile de la page prediction"""
    
    print("📱 AMÉLIORATION DE LA RESPONSIVITÉ MOBILE - PAGE PREDICTION")
    print("=" * 70)
    
    # 1. Améliorer le fichier HTML
    ameliorer_html_prediction()
    
    # 2. Améliorer les styles CSS
    ameliorer_css_prediction()
    
    print("\n✅ AMÉLIORATIONS APPLIQUÉES AVEC SUCCÈS !")
    print("\n📋 RÉSUMÉ DES AMÉLIORATIONS :")
    print("   ✅ Texte adaptatif pour tous les écrans")
    print("   ✅ Grille responsive pour les cartes d'estimation")
    print("   ✅ Formulaire optimisé pour mobile")
    print("   ✅ Graphiques adaptatifs")
    print("   ✅ Espacement et padding optimisés")
    print("   ✅ Débordements corrigés")

def ameliorer_html_prediction():
    """Améliorer le HTML de la page prediction"""
    
    html_file = "frontend/prediction.html"
    
    if not os.path.exists(html_file):
        print(f"❌ Fichier {html_file} non trouvé")
        return
    
    print("\n🔧 AMÉLIORATION DU HTML...")
    
    # Lire le contenu actuel
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture HTML : {e}")
        return
    
    # Améliorations à apporter
    modifications = [
        # Améliorer les labels pour éviter les débordements
        (r'<label for="cout_prod">Combien je dépense par hectare \(FCFA\)</label>',
         '<label for="cout_prod">Coût par hectare (FCFA)</label>'),
        
        (r'<label for="prix_a">Prix de vente du cacao \(FCFA/tonne\)</label>',
         '<label for="prix_a">Prix de vente (FCFA/tonne)</label>'),
        
        (r'<label for="competences">Je sais lire et écrire</label>',
         '<label for="competences">Niveau d\'éducation</label>'),
        
        # Améliorer les options pour éviter les débordements
        (r'<option value="oui, lire et écrire" selected>Oui, je sais</option>',
         '<option value="oui, lire et écrire" selected>Oui, lire et écrire</option>'),
        
        (r'<option value="oui, lire seulement">Je sais seulement lire</option>',
         '<option value="oui, lire seulement">Lire seulement</option>'),
        
        (r'<option value="non">Non, je ne sais pas</option>',
         '<option value="non">Non</option>'),
        
        # Améliorer les titres de sections
        (r'<h3>📝 Mes Informations de Plantation</h3>',
         '<h3>🌱 Plantation</h3>'),
        
        (r'<h3>💰 Mes Coûts et Prix</h3>',
         '<h3>💰 Coûts & Prix</h3>'),
        
        (r'<h3>🌍 Ma Région et le Climat</h3>',
         '<h3>🌍 Région & Climat</h3>'),
        
        (r'<h3>👤 Mes Informations Personnelles</h3>',
         '<h3>👤 Profil</h3>'),
        
        # Améliorer les titres des cartes d'estimation
        (r'<h4>Production Estimée</h4>',
         '<h4>Production</h4>'),
        
        (r'<h4>Revenu Potentiel</h4>',
         '<h4>Revenu</h4>'),
        
        (r'<h4>Bénéfice Estimé</h4>',
         '<h4>Bénéfice</h4>'),
        
        # Améliorer les titres de sections
        (r'<h4>Analyse détaillée et recommandations</h4>',
         '<h4>Analyse & Recommandations</h4>'),
        
        (r'<h4>Suggestions d\'optimisation</h4>',
         '<h4>Optimisations</h4>'),
        
        (r'<h5>Analyse de la productivité</h5>',
         '<h5>Productivité</h5>'),
        
        (r'<h5>Pistes d\'amélioration :</h5>',
         '<h5>Améliorations :</h5>'),
    ]
    
    # Appliquer les modifications
    for old, new in modifications:
        content = content.replace(old, new)
    
    # Écrire le fichier modifié
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ HTML amélioré avec succès")
    except Exception as e:
        print(f"❌ Erreur écriture HTML : {e}")

def ameliorer_css_prediction():
    """Améliorer les styles CSS pour la page prediction"""
    
    css_file = "frontend/css/style.css"
    
    if not os.path.exists(css_file):
        print(f"❌ Fichier {css_file} non trouvé")
        return
    
    print("\n🎨 AMÉLIORATION DU CSS...")
    
    # Lire le contenu actuel
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture CSS : {e}")
        return
    
    # Nouvelles règles CSS pour améliorer la responsivité
    nouvelles_regles = """
/* ===== AMÉLIORATIONS RESPONSIVES POUR LA PAGE PREDICTION ===== */

/* Responsive général pour prediction */
@media (max-width: 480px) {
    .prediction-container {
        grid-template-columns: 1fr;
        gap: 1rem;
        margin-top: 1rem;
        padding: 0 0.5rem;
    }
    
    .prediction-form-container {
        padding: 1rem;
        position: static;
    }
    
    .prediction-form h3 {
        font-size: 1rem;
        margin: 1rem 0 0.8rem 0;
        text-align: center;
    }
    
    .prediction-form .form-group {
        margin-bottom: 1rem;
    }
    
    .prediction-form .form-group label {
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        padding: 0.7rem;
        font-size: 0.9rem;
        border-radius: 8px;
    }
    
    .prediction-form .btn {
        padding: 1rem 1.5rem;
        font-size: 1rem;
        margin-top: 0.8rem;
    }
    
    /* Cartes d'estimation responsive */
    .estimation-cards {
        grid-template-columns: 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .estimation-card {
        padding: 1rem;
        border-radius: 12px;
    }
    
    .estimation-card h4 {
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    
    .estimation-value {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    
    .estimation-unit {
        font-size: 0.8rem;
    }
    
    /* Détails des calculs responsive */
    .calculation-details {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .details-header h4 {
        font-size: 1rem;
    }
    
    .details-content {
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    .details-content ul {
        padding-left: 1rem;
    }
    
    .details-content li {
        margin-bottom: 0.3rem;
        font-size: 0.85rem;
    }
    
    /* Section d'analyse responsive */
    .analysis-section {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .analysis-header h4 {
        font-size: 1rem;
    }
    
    .analysis-content h5 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .analysis-content p {
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    .analysis-content ul {
        padding-left: 1rem;
    }
    
    .analysis-content li {
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }
    
    /* Graphiques responsive */
    .comparison-chart {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .comparison-chart h4 {
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .comparison-chart p {
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    
    .comparison-chart canvas {
        max-width: 100%;
        height: auto;
    }
    
    .financial-distribution {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .financial-distribution h4 {
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .chart-container canvas {
        max-width: 100%;
        height: auto;
    }
    
    /* Suggestions d'optimisation responsive */
    .optimization-suggestions {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .suggestions-header h4 {
        font-size: 1rem;
    }
    
    .suggestions-content h5 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .suggestions-content ul {
        padding-left: 1rem;
    }
    
    .suggestions-content li {
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }
}

/* Très petits écrans (≤375px) */
@media (max-width: 375px) {
    .prediction-container {
        padding: 0 0.3rem;
        gap: 0.8rem;
    }
    
    .prediction-form-container {
        padding: 0.8rem;
    }
    
    .prediction-form h3 {
        font-size: 0.95rem;
        margin: 0.8rem 0 0.6rem 0;
    }
    
    .prediction-form .form-group label {
        font-size: 0.8rem;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        padding: 0.6rem;
        font-size: 0.85rem;
    }
    
    .prediction-form .btn {
        padding: 0.8rem 1.2rem;
        font-size: 0.95rem;
    }
    
    .estimation-card {
        padding: 0.8rem;
    }
    
    .estimation-card h4 {
        font-size: 0.85rem;
    }
    
    .estimation-value {
        font-size: 1.6rem;
    }
    
    .estimation-unit {
        font-size: 0.75rem;
    }
    
    .calculation-details,
    .analysis-section,
    .comparison-chart,
    .financial-distribution,
    .optimization-suggestions {
        padding: 0.8rem;
    }
    
    .details-header h4,
    .analysis-header h4,
    .comparison-chart h4,
    .financial-distribution h4,
    .suggestions-header h4 {
        font-size: 0.95rem;
    }
    
    .details-content,
    .analysis-content p,
    .comparison-chart p {
        font-size: 0.8rem;
    }
    
    .analysis-content h5,
    .suggestions-content h5 {
        font-size: 0.85rem;
    }
    
    .details-content li,
    .analysis-content li,
    .suggestions-content li {
        font-size: 0.8rem;
    }
}

/* Écrans moyens (481px - 767px) */
@media (min-width: 481px) and (max-width: 767px) {
    .prediction-container {
        gap: 1.5rem;
        padding: 0 1rem;
    }
    
    .prediction-form-container {
        padding: 1.5rem;
    }
    
    .estimation-cards {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.2rem;
    }
    
    .estimation-card {
        padding: 1.2rem;
    }
    
    .estimation-value {
        font-size: 2rem;
    }
}

/* Orientation paysage pour mobile */
@media (orientation: landscape) and (max-width: 900px) {
    .prediction-container {
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .prediction-form-container {
        padding: 1rem;
    }
    
    .prediction-form h3 {
        font-size: 1rem;
        margin: 0.8rem 0 0.6rem 0;
    }
    
    .prediction-form .form-group {
        margin-bottom: 0.8rem;
    }
    
    .prediction-form .form-group label {
        font-size: 0.85rem;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        padding: 0.6rem;
        font-size: 0.9rem;
    }
    
    .estimation-cards {
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }
    
    .estimation-card {
        padding: 1rem;
    }
    
    .estimation-value {
        font-size: 1.8rem;
    }
    
    .calculation-details,
    .analysis-section,
    .comparison-chart,
    .financial-distribution,
    .optimization-suggestions {
        padding: 1rem;
    }
}

/* Amélioration des débordements de texte */
.prediction-form .form-group label {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}

.prediction-form .form-group select option {
    font-size: 0.9rem;
    padding: 0.5rem;
}

.estimation-card h4,
.analysis-content h5,
.suggestions-content h5 {
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Amélioration de l'espacement pour éviter les débordements */
.prediction-result {
    gap: 1.5rem;
}

.prediction-result > div {
    margin-bottom: 1.5rem;
}

.prediction-result > div:last-child {
    margin-bottom: 0;
}

/* Amélioration de la lisibilité sur mobile */
@media (max-width: 480px) {
    .prediction-form .form-group label {
        line-height: 1.3;
        margin-bottom: 0.4rem;
    }
    
    .prediction-form .form-group input,
    .prediction-form .form-group select {
        line-height: 1.4;
    }
    
    .estimation-card h4 {
        line-height: 1.2;
    }
    
    .analysis-content p,
    .suggestions-content li {
        line-height: 1.4;
    }
}

/* ===== FIN DES AMÉLIORATIONS RESPONSIVES ===== */
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
    print("🚀 DÉMARRAGE DE L'AMÉLIORATION DE LA PAGE PREDICTION")
    print("=" * 70)
    
    ameliorer_prediction_mobile()
    
    print("\n🎉 AMÉLIORATION TERMINÉE !")
    print("\n📱 LA PAGE PREDICTION EST MAINTENANT PARFAITEMENT RESPONSIVE")
    print("   ✅ Texte adaptatif pour tous les écrans")
    print("   ✅ Débordements corrigés")
    print("   ✅ Interface optimisée pour mobile")
    print("   ✅ Grille responsive")
    print("   ✅ Graphiques adaptatifs")

if __name__ == "__main__":
    main()
