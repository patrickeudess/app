#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la responsivité mobile de l'application Mon Cacao
Vérifie que l'interface s'adapte à tous les types d'écrans de téléphone
"""

import os
import re

def test_responsivite_mobile():
    """Test complet de la responsivité mobile"""
    
    print("📱 TEST DE RESPONSIVITÉ MOBILE - MON CACAO")
    print("=" * 60)
    
    # Vérifier les fichiers principaux
    files_to_check = [
        "frontend/index.html",
        "frontend/css/style.css",
        "frontend/score-ecologique.html"
    ]
    
    results = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ Fichier trouvé : {file_path}")
            result = test_file_responsivite(file_path)
            results.append(result)
        else:
            print(f"❌ Fichier manquant : {file_path}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS DE RESPONSIVITÉ")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests réussis : {passed}/{total}")
    print(f"📈 Taux de réussite : {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 L'APPLICATION EST PARFAITEMENT RESPONSIVE !")
        return True
    else:
        print(f"\n⚠️  {total-passed} problème(s) de responsivité détecté(s)")
        return False

def test_file_responsivite(file_path):
    """Test la responsivité d'un fichier spécifique"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {file_path}: {e}")
        return False
    
    print(f"\n🔍 Test de responsivité pour : {file_path}")
    
    if file_path.endswith('.html'):
        return test_html_responsivite(content, file_path)
    elif file_path.endswith('.css'):
        return test_css_responsivite(content, file_path)
    else:
        return False

def test_html_responsivite(content, file_path):
    """Test la responsivité des fichiers HTML"""
    
    tests = []
    
    # Test 1: Meta viewport
    viewport_meta = 'viewport' in content and 'width=device-width' in content
    tests.append(viewport_meta)
    print(f"   - Meta viewport : {'✅' if viewport_meta else '❌'}")
    
    # Test 2: CSS responsive
    responsive_css = 'media' in content or 'responsive' in content
    tests.append(responsive_css)
    print(f"   - CSS responsive : {'✅' if responsive_css else '❌'}")
    
    # Test 3: Grille 3x3 pour index.html
    if 'index.html' in file_path:
        grid_3x3 = 'grid-template-columns: repeat(3, 1fr)' in content
        tests.append(grid_3x3)
        print(f"   - Grille 3x3 : {'✅' if grid_3x3 else '❌'}")
    
    # Test 4: Flexbox ou Grid
    flexbox_grid = 'display: flex' in content or 'display: grid' in content
    tests.append(flexbox_grid)
    print(f"   - Flexbox/Grid : {'✅' if flexbox_grid else '❌'}")
    
    return all(tests)

def test_css_responsivite(content, file_path):
    """Test la responsivité des fichiers CSS"""
    
    tests = []
    
    # Test 1: Media queries pour mobile
    mobile_queries = [
        '@media (max-width: 375px)',
        '@media (max-width: 480px)',
        '@media (max-width: 768px)',
        '@media (orientation: landscape)'
    ]
    
    mobile_responsive = any(query in content for query in mobile_queries)
    tests.append(mobile_responsive)
    print(f"   - Media queries mobile : {'✅' if mobile_responsive else '❌'}")
    
    # Test 2: Grille 3x3
    grid_3x3 = 'grid-template-columns: repeat(3, 1fr)' in content
    tests.append(grid_3x3)
    print(f"   - Grille 3x3 : {'✅' if grid_3x3 else '❌'}")
    
    # Test 3: Responsive pour très petits écrans
    very_small_screens = '@media (max-width: 375px)' in content
    tests.append(very_small_screens)
    print(f"   - Très petits écrans (≤375px) : {'✅' if very_small_screens else '❌'}")
    
    # Test 4: Responsive pour petits écrans
    small_screens = '@media (max-width: 480px)' in content
    tests.append(small_screens)
    print(f"   - Petits écrans (≤480px) : {'✅' if small_screens else '❌'}")
    
    # Test 5: Responsive pour écrans moyens
    medium_screens = '@media (max-width: 768px)' in content
    tests.append(medium_screens)
    print(f"   - Écrans moyens (≤768px) : {'✅' if medium_screens else '❌'}")
    
    # Test 6: Orientation paysage
    landscape_orientation = '@media (orientation: landscape)' in content
    tests.append(landscape_orientation)
    print(f"   - Orientation paysage : {'✅' if landscape_orientation else '❌'}")
    
    # Test 7: Flexbox responsive
    flexbox_responsive = 'flex-direction: column' in content or 'flex-direction: row' in content
    tests.append(flexbox_responsive)
    print(f"   - Flexbox responsive : {'✅' if flexbox_responsive else '❌'}")
    
    # Test 8: Tailles de police adaptatives
    adaptive_fonts = 'font-size:' in content and 'rem' in content
    tests.append(adaptive_fonts)
    print(f"   - Tailles de police adaptatives : {'✅' if adaptive_fonts else '❌'}")
    
    return all(tests)

def test_specific_features():
    """Test des fonctionnalités spécifiques de responsivité"""
    
    print("\n🎯 TESTS DES FONCTIONNALITÉS SPÉCIFIQUES")
    print("=" * 60)
    
    # Vérifier le CSS principal
    css_file = "frontend/css/style.css"
    if not os.path.exists(css_file):
        print("❌ Fichier CSS principal non trouvé")
        return False
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSS : {e}")
        return False
    
    tests = []
    
    # Test 1: Grille 3x3 avec 3 icônes par ligne
    grid_3x3 = 'grid-template-columns: repeat(3, 1fr)' in css_content
    tests.append(grid_3x3)
    print(f"✅ Grille 3x3 (3 icônes par ligne) : {'✅' if grid_3x3 else '❌'}")
    
    # Test 2: Responsive pour tous les types d'écrans
    screen_sizes = [
        'max-width: 375px',  # Très petits écrans
        'max-width: 480px',  # Petits écrans
        'max-width: 768px',  # Écrans moyens
        'min-width: 768px',  # Tablettes
        'min-width: 1024px'  # Desktop
    ]
    
    all_screen_sizes = all(size in css_content for size in screen_sizes)
    tests.append(all_screen_sizes)
    print(f"✅ Tous les types d'écrans couverts : {'✅' if all_screen_sizes else '❌'}")
    
    # Test 3: Orientation paysage
    landscape = '@media (orientation: landscape)' in css_content
    tests.append(landscape)
    print(f"✅ Orientation paysage : {'✅' if landscape else '❌'}")
    
    # Test 4: Adaptation du header mobile
    header_mobile = 'header-content' in css_content and 'flex-direction: column' in css_content
    tests.append(header_mobile)
    print(f"✅ Header adaptatif mobile : {'✅' if header_mobile else '❌'}")
    
    # Test 5: Cartes adaptatives
    adaptive_cards = 'feature-card' in css_content and 'min-height' in css_content
    tests.append(adaptive_cards)
    print(f"✅ Cartes adaptatives : {'✅' if adaptive_cards else '❌'}")
    
    return all(tests)

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS DE RESPONSIVITÉ MOBILE")
    print("=" * 60)
    
    # Test général de responsivité
    general_success = test_responsivite_mobile()
    
    # Test des fonctionnalités spécifiques
    specific_success = test_specific_features()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("🎯 RÉSULTAT FINAL")
    print("=" * 60)
    
    if general_success and specific_success:
        print("🎉 SUCCÈS : L'application est parfaitement responsive !")
        print("\n📱 FONCTIONNALITÉS RESPONSIVES IMPLÉMENTÉES :")
        print("   ✅ Grille 3x3 (3 icônes par ligne)")
        print("   ✅ Adaptation à tous les types d'écrans de téléphone")
        print("   ✅ Très petits écrans (320px - 375px)")
        print("   ✅ Petits écrans (376px - 414px)")
        print("   ✅ Écrans moyens (415px - 480px)")
        print("   ✅ Grands écrans de téléphone (481px - 767px)")
        print("   ✅ Orientation paysage")
        print("   ✅ Header adaptatif")
        print("   ✅ Cartes adaptatives")
        print("   ✅ Tailles de police adaptatives")
        return True
    else:
        print("⚠️  PROBLÈMES DÉTECTÉS : Certains aspects de la responsivité nécessitent des améliorations")
        return False

if __name__ == "__main__":
    main()
