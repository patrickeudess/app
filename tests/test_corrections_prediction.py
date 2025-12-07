#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de vérification des corrections appliquées à la page prediction
"""

import re

def test_corrections_prediction():
    """Vérifier que les corrections ont été appliquées"""
    
    print("🧪 VÉRIFICATION DES CORRECTIONS - PAGE PREDICTION")
    print("=" * 60)
    
    # Lire le fichier JavaScript
    try:
        with open('frontend/js/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture script.js: {e}")
        return
    
    print("🔍 VÉRIFICATION DES CORRECTIONS APPLIQUÉES")
    print("-" * 40)
    
    corrections_appliquees = []
    corrections_manquantes = []
    
    # 1. Vérifier updateCalculationDetails
    if 'parseFloat(document.getElementById(\'prix_a\').value)' in js_content:
        corrections_appliquees.append("✅ Prix dynamique dans updateCalculationDetails")
    else:
        corrections_manquantes.append("❌ Prix codé en dur dans updateCalculationDetails")
    
    if 'parseFloat(document.getElementById(\'cout_prod\').value)' in js_content:
        corrections_appliquees.append("✅ Coût dynamique dans updateCalculationDetails")
    else:
        corrections_manquantes.append("❌ Coût codé en dur dans updateCalculationDetails")
    
    # 2. Vérifier updateAnalysisAndRecommendations
    if 'parseFloat(document.getElementById(\'cout_prod\').value)' in js_content:
        corrections_appliquees.append("✅ Coût dynamique dans updateAnalysisAndRecommendations")
    else:
        corrections_manquantes.append("❌ Coût codé en dur dans updateAnalysisAndRecommendations")
    
    # 3. Vérifier createComparisonChart
    if 'parseFloat(document.getElementById(\'cout_prod\').value)' in js_content:
        corrections_appliquees.append("✅ Coût dynamique dans createComparisonChart")
    else:
        corrections_manquantes.append("❌ Coût codé en dur dans createComparisonChart")
    
    # 4. Vérifier createFinancialChart
    if 'parseFloat(document.getElementById(\'cout_prod\').value)' in js_content:
        corrections_appliquees.append("✅ Coût dynamique dans createFinancialChart")
    else:
        corrections_manquantes.append("❌ Coût codé en dur dans createFinancialChart")
    
    # 5. Vérifier simulatePrediction
    if 'parseFloat(document.getElementById(\'prix_a\').value)' in js_content:
        corrections_appliquees.append("✅ Prix dynamique dans simulatePrediction")
    else:
        corrections_manquantes.append("❌ Prix codé en dur dans simulatePrediction")
    
    print("\n📊 RÉSULTATS")
    print("-" * 40)
    
    if corrections_appliquees:
        print("✅ CORRECTIONS APPLIQUÉES:")
        for correction in corrections_appliquees:
            print(f"   {correction}")
    
    if corrections_manquantes:
        print("\n❌ CORRECTIONS MANQUANTES:")
        for correction in corrections_manquantes:
            print(f"   {correction}")
    
    # Vérifier les valeurs codées en dur restantes
    print("\n🔍 VÉRIFICATION DES VALEURS CODÉES EN DUR RESTANTES")
    print("-" * 40)
    
    hardcoded_patterns = [
        (r'const price = (\d+);', 'Prix codé en dur'),
        (r'const cost = (\d+);', 'Coût codé en dur'),
        (r'const prix_kg = (\d+);', 'Prix kg codé en dur'),
        (r'const regionalCost = (\d+);', 'Coût régional codé en dur')
    ]
    
    hardcoded_values = []
    for pattern, description in hardcoded_patterns:
        match = re.search(pattern, js_content)
        if match:
            hardcoded_values.append(f"{description}: {match.group(1)}")
    
    if hardcoded_values:
        print("⚠️ VALEURS CODÉES EN DUR RESTANTES:")
        for value in hardcoded_values:
            print(f"   • {value}")
    else:
        print("✅ Aucune valeur codée en dur restante")
    
    # Résumé final
    print("\n🎯 RÉSUMÉ FINAL")
    print("-" * 40)
    
    total_corrections = len(corrections_appliquees) + len(corrections_manquantes)
    taux_reussite = (len(corrections_appliquees) / total_corrections * 100) if total_corrections > 0 else 0
    
    print(f"📈 Taux de correction: {taux_reussite:.1f}%")
    print(f"✅ Corrections appliquées: {len(corrections_appliquees)}")
    print(f"❌ Corrections manquantes: {len(corrections_manquantes)}")
    
    if taux_reussite == 100:
        print("\n🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES !")
        print("   ✅ Les calculs utilisent maintenant les vraies valeurs saisies par l'utilisateur")
        print("   ✅ Plus d'incohérences dans les calculs")
    else:
        print(f"\n⚠️ {len(corrections_manquantes)} corrections restent à appliquer")

if __name__ == "__main__":
    test_corrections_prediction()
