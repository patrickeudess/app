#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de suppression de la page profil
"""

import os

def test_suppression_profil():
    """Tester que toutes les références au profil ont été supprimées"""
    
    print("🧪 TEST DE SUPPRESSION DE LA PAGE PROFIL")
    print("=" * 50)
    
    # Fichiers à vérifier
    fichiers = [
        "frontend/index.html",
        "frontend/dashboard.html", 
        "frontend/revenue.html",
        "frontend/prediction.html",
        "frontend/js/script.js"
    ]
    
    tests_reussis = 0
    tests_totaux = 0
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            print(f"🔍 Vérification de {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Erreur lecture {fichier}")
                continue
            
            # Tests spécifiques selon le fichier
            if fichier == "frontend/index.html":
                tests = [
                    ("Carte profil supprimée", "<!-- Profil -->" not in content),
                    ("Section profil supprimée", "<!-- Section Profil -->" not in content),
                    ("Modal profil supprimé", "<!-- Modal Profil -->" not in content),
                    ("Fonction openProfile supprimée", "openProfile()" not in content),
                    ("Fonction saveProfile supprimée", "saveProfile()" not in content)
                ]
            elif fichier == "frontend/dashboard.html":
                tests = [
                    ("Carte profil dashboard supprimée", "<!-- 9. Profil -->" not in content),
                    ("Navigation profil supprimée", "navigateTo('profile')" not in content)
                ]
            elif fichier == "frontend/revenue.html":
                tests = [
                    ("Navigation profil revenue supprimée", "navigateTo('profile')" not in content)
                ]
            elif fichier == "frontend/prediction.html":
                tests = [
                    ("Section profil prediction supprimée", "👤 Profil" not in content),
                    ("Champs profil supprimés", "sexe" not in content and "competences" not in content)
                ]
            elif fichier == "frontend/js/script.js":
                tests = [
                    ("Fonction openProfile supprimée", "function openProfile()" not in content),
                    ("Fonction saveProfile supprimée", "function saveProfile()" not in content),
                    ("Fonction loadProfileData supprimée", "function loadProfileData()" not in content),
                    ("Fonction updateProfileDisplay supprimée", "function updateProfileDisplay()" not in content),
                    ("Référence profile-modal supprimée", "profile-modal" not in content)
                ]
            
            # Exécuter les tests
            for test_name, test_result in tests:
                tests_totaux += 1
                if test_result:
                    print(f"   ✅ {test_name}")
                    tests_reussis += 1
                else:
                    print(f"   ❌ {test_name}")
            
            print(f"   📊 {len(tests)} tests effectués")
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    taux_reussite = (tests_reussis / tests_totaux * 100) if tests_totaux > 0 else 0
    print(f"✅ Tests réussis: {tests_reussis}/{tests_totaux}")
    print(f"📈 Taux de réussite: {taux_reussite:.1f}%")
    
    if taux_reussite == 100:
        print("\n🎉 SUPPRESSION COMPLÈTE !")
        print("   ✅ Toutes les références au profil ont été supprimées")
        print("   ✅ La page profil n'existe plus")
        print("   ✅ Les fonctions JavaScript ont été nettoyées")
    else:
        print(f"\n⚠️ ATTENTION: {tests_totaux - tests_reussis} références restent")
        print("   🔧 Vérifiez manuellement les fichiers concernés")

if __name__ == "__main__":
    test_suppression_profil()
