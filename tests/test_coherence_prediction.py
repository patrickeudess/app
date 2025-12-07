#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de cohérence des calculs de la page prediction
"""

import re

def test_coherence_prediction():
    """Tester la cohérence des calculs dans la page prediction"""
    
    print("🧪 TEST DE COHÉRENCE DES CALCULS - PAGE PREDICTION")
    print("=" * 60)
    
    # Lire le fichier JavaScript
    try:
        with open('frontend/js/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture script.js: {e}")
        return
    
    # Lire le fichier HTML
    try:
        with open('frontend/prediction.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture prediction.html: {e}")
        return
    
    print("🔍 ANALYSE DES VALEURS PAR DÉFAUT")
    print("-" * 40)
    
    # Vérifier les valeurs par défaut dans le HTML
    cout_prod_default = re.search(r'placeholder="(\d+)"', html_content)
    prix_a_default = re.search(r'value="(\d+)"', html_content)
    
    if cout_prod_default:
        print(f"✅ Coût par hectare (placeholder): {cout_prod_default.group(1)} FCFA")
    else:
        print("❌ Coût par hectare (placeholder): Non trouvé")
    
    if prix_a_default:
        print(f"✅ Prix de vente (value): {prix_a_default.group(1)} FCFA/Kg")
    else:
        print("❌ Prix de vente (value): Non trouvé")
    
    print("\n🔍 ANALYSE DES CALCULS DANS LE JAVASCRIPT")
    print("-" * 40)
    
    # Extraire les valeurs utilisées dans les calculs
    price_pattern = r'const price = (\d+);'
    cost_pattern = r'const cost = (\d+);'
    prix_kg_pattern = r'const prix_kg = (\d+);'
    
    price_match = re.search(price_pattern, js_content)
    cost_match = re.search(cost_pattern, js_content)
    prix_kg_match = re.search(prix_kg_pattern, js_content)
    
    if price_match:
        print(f"✅ Prix utilisé dans updateCalculationDetails: {price_match.group(1)} FCFA/Kg")
    else:
        print("❌ Prix dans updateCalculationDetails: Non trouvé")
    
    if cost_match:
        print(f"✅ Coût utilisé dans updateCalculationDetails: {cost_match.group(1)} FCFA/ha")
    else:
        print("❌ Coût dans updateCalculationDetails: Non trouvé")
    
    if prix_kg_match:
        print(f"✅ Prix utilisé dans simulatePrediction: {prix_kg_match.group(1)} FCFA/Kg")
    else:
        print("❌ Prix dans simulatePrediction: Non trouvé")
    
    print("\n🔍 VÉRIFICATION DES INCOHÉRENCES")
    print("-" * 40)
    
    # Vérifier les incohérences
    incohérences = []
    
    # 1. Vérifier si les valeurs par défaut correspondent aux calculs
    if cout_prod_default and cost_match:
        cout_default = int(cout_prod_default.group(1))
        cost_calc = int(cost_match.group(1))
        if cout_default != cost_calc:
            incohérences.append(f"Coût par hectare: {cout_default} (HTML) vs {cost_calc} (calcul)")
    
    if prix_a_default and price_match:
        prix_default = int(prix_a_default.group(1))
        price_calc = int(price_match.group(1))
        if prix_default != price_calc:
            incohérences.append(f"Prix de vente: {prix_default} (HTML) vs {price_calc} (calcul)")
    
    # 2. Vérifier les valeurs codées en dur
    hardcoded_values = []
    
    # Chercher les valeurs codées en dur
    hardcoded_patterns = [
        (r'const price = (\d+);', 'Prix codé en dur'),
        (r'const cost = (\d+);', 'Coût codé en dur'),
        (r'const prix_kg = (\d+);', 'Prix kg codé en dur'),
        (r'const regionalCost = (\d+);', 'Coût régional codé en dur')
    ]
    
    for pattern, description in hardcoded_patterns:
        match = re.search(pattern, js_content)
        if match:
            hardcoded_values.append(f"{description}: {match.group(1)}")
    
    print("\n📊 RÉSULTATS")
    print("-" * 40)
    
    if incohérences:
        print("❌ INCOHÉRENCES DÉTECTÉES:")
        for incohérence in incohérences:
            print(f"   • {incohérence}")
    else:
        print("✅ Aucune incohérence détectée")
    
    if hardcoded_values:
        print("\n⚠️ VALEURS CODÉES EN DUR:")
        for value in hardcoded_values:
            print(f"   • {value}")
    
    print("\n🔧 RECOMMANDATIONS")
    print("-" * 40)
    
    if incohérences or hardcoded_values:
        print("1. Corriger les valeurs codées en dur dans le JavaScript")
        print("2. Utiliser les valeurs saisies par l'utilisateur dans les calculs")
        print("3. S'assurer que les valeurs par défaut correspondent aux calculs")
        print("4. Récupérer dynamiquement les valeurs des champs de formulaire")
    else:
        print("✅ Les calculs semblent cohérents")
    
    return incohérences, hardcoded_values

if __name__ == "__main__":
    test_coherence_prediction()
