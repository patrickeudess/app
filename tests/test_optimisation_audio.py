#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'optimisation des boutons audio
"""

import os

def test_optimisation_audio():
    """Tester l'optimisation des boutons audio"""
    
    print("🎤 TEST DE L'OPTIMISATION AUDIO")
    print("=" * 50)
    
    # Fichiers à tester
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
    
    tests_reussis = 0
    total_tests = 0
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            print(f"\n📄 Test de {fichier}")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier}")
                continue
            
            # Tests à effectuer
            tests = []
            
            # Test 1: Ancien script audio supprimé
            ancien_script = '// Fonction pour lire les titres' in content
            tests.append(not ancien_script)
            print(f"   ✅ Ancien script supprimé : {'✅' if not ancien_script else '❌'}")
            
            # Test 2: Nouveau script simple présent
            nouveau_script = '// Boutons audio seulement sur les labels' in content
            tests.append(nouveau_script)
            print(f"   ✅ Nouveau script présent : {'✅' if nouveau_script else '❌'}")
            
            # Test 3: Pas de boutons sur les titres
            boutons_titres = 'btn-audio-titre' in content
            tests.append(not boutons_titres)
            print(f"   ✅ Pas de boutons sur titres : {'✅' if not boutons_titres else '❌'}")
            
            # Test 4: Pas de boutons sur descriptions
            boutons_desc = 'btn-audio-desc' in content
            tests.append(not boutons_desc)
            print(f"   ✅ Pas de boutons sur descriptions : {'✅' if not boutons_desc else '❌'}")
            
            # Résumé pour ce fichier
            passed = sum(tests)
            total = len(tests)
            total_tests += total
            tests_reussis += passed
            
            print(f"   📊 {fichier} : {passed}/{total} tests réussis")
    
    # Test CSS
    print(f"\n🎨 Test du CSS")
    css_file = "frontend/css/style.css"
    
    if os.path.exists(css_file):
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
        except Exception as e:
            print(f"❌ Erreur lecture CSS")
        else:
            # Tests CSS
            css_tests = []
            
            # Test 1: CSS optimisé présent
            css_optimise = '/* ===== BOUTONS AUDIO OPTIMISÉS ===== */' in css_content
            css_tests.append(css_optimise)
            print(f"   ✅ CSS optimisé présent : {'✅' if css_optimise else '❌'}")
            
            # Test 2: Ancien CSS supprimé
            ancien_css = 'btn-audio-titre' in css_content
            css_tests.append(not ancien_css)
            print(f"   ✅ Ancien CSS supprimé : {'✅' if not ancien_css else '❌'}")
            
            # Test 3: Boutons plus petits
            boutons_petits = 'width: 26px' in css_content
            css_tests.append(boutons_petits)
            print(f"   ✅ Boutons plus petits : {'✅' if boutons_petits else '❌'}")
            
            passed_css = sum(css_tests)
            total_css = len(css_tests)
            total_tests += total_css
            tests_reussis += passed_css
            
            print(f"   📊 CSS : {passed_css}/{total_css} tests réussis")
    
    # Résumé final
    print("\n" + "=" * 50)
    print("🎯 RÉSULTAT FINAL")
    print("=" * 50)
    
    print(f"✅ Tests réussis : {tests_reussis}/{total_tests}")
    print(f"📈 Taux de réussite : {(tests_reussis/total_tests)*100:.1f}%")
    
    if tests_reussis == total_tests:
        print("\n🎉 SUCCÈS : OPTIMISATION PARFAITE !")
        print("\n📋 RÉCAPITULATIF :")
        print("   ✅ Boutons audio seulement sur les questions")
        print("   ✅ Anciens boutons supprimés")
        print("   ✅ Interface plus propre")
        print("   ✅ CSS optimisé")
        return True
    else:
        print(f"\n⚠️  {total_tests-tests_reussis} problème(s) détecté(s)")
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DU TEST D'OPTIMISATION")
    print("=" * 50)
    
    success = test_optimisation_audio()
    
    if success:
        print("\n🎉 CONFIRMATION : OPTIMISATION RÉUSSIE !")
        print("\n🎤 L'INTERFACE AUDIO EST MAINTENANT OPTIMALE")
        print("   ✅ Boutons audio seulement où nécessaire")
        print("   ✅ Interface plus claire et moins encombrée")
        print("   ✅ Meilleure expérience utilisateur")
        return True
    else:
        print("\n⚠️  ATTENTION : Vérifiez les problèmes détectés")
        return False

if __name__ == "__main__":
    main()
