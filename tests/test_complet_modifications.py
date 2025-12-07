#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet des modifications de prix dans l'application
"""

import os

def test_complet_modifications():
    """Test complet des modifications de prix"""
    
    print("🔍 TEST COMPLET DES MODIFICATIONS DE PRIX")
    print("=" * 60)
    
    # Fichiers à vérifier
    fichiers = [
        "frontend/prediction.html",
        "frontend/index.html"
    ]
    
    tous_tests_reussis = True
    
    for fichier in fichiers:
        print(f"\n📄 VÉRIFICATION DE {fichier}")
        print("-" * 40)
        
        if not os.path.exists(fichier):
            print(f"❌ Fichier {fichier} non trouvé")
            tous_tests_reussis = False
            continue
        
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Erreur lecture {fichier} : {e}")
            tous_tests_reussis = False
            continue
        
        # Tests pour ce fichier
        tests_fichier = []
        
        # Test 1: Nouveau label présent
        nouveau_label = 'Prix de vente du cacao (Fcfa/Kg)' in content
        tests_fichier.append(nouveau_label)
        print(f"✅ Nouveau label présent : {'✅' if nouveau_label else '❌'}")
        
        # Test 2: Ancien label supprimé
        ancien_label = 'Prix de vente (FCFA/tonne)' in content
        tests_fichier.append(not ancien_label)
        print(f"✅ Ancien label supprimé : {'✅' if not ancien_label else '❌'}")
        
        # Test 3: Nouvelle valeur présente
        nouvelle_valeur = 'value="1000"' in content
        tests_fichier.append(nouvelle_valeur)
        print(f"✅ Nouvelle valeur présente : {'✅' if nouvelle_valeur else '❌'}")
        
        # Test 4: Ancienne valeur supprimée
        ancienne_valeur = 'value="750000"' in content
        tests_fichier.append(not ancienne_valeur)
        print(f"✅ Ancienne valeur supprimée : {'✅' if not ancienne_valeur else '❌'}")
        
        # Test 5: Nouveau placeholder présent
        nouveau_placeholder = 'placeholder="1000"' in content
        tests_fichier.append(nouveau_placeholder)
        print(f"✅ Nouveau placeholder présent : {'✅' if nouveau_placeholder else '❌'}")
        
        # Résumé pour ce fichier
        passed = sum(tests_fichier)
        total = len(tests_fichier)
        
        print(f"📊 {fichier} : {passed}/{total} tests réussis")
        
        if passed < total:
            tous_tests_reussis = False
    
    # Test final global
    print("\n" + "=" * 60)
    print("🎯 RÉSULTAT FINAL")
    print("=" * 60)
    
    if tous_tests_reussis:
        print("🎉 SUCCÈS : TOUTES LES MODIFICATIONS ONT ÉTÉ APPLIQUÉES !")
        print("\n📋 RÉSUMÉ DES MODIFICATIONS :")
        print("   ✅ Label : 'Prix de vente du cacao (Fcfa/Kg)'")
        print("   ✅ Valeur par défaut : 1000")
        print("   ✅ Placeholder : 1000")
        print("   ✅ Anciens éléments supprimés")
        print("   ✅ Modifications dans prediction.html")
        print("   ✅ Modifications dans index.html")
        return True
    else:
        print("⚠️  ATTENTION : Certaines modifications nécessitent une vérification")
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DU TEST COMPLET")
    print("=" * 60)
    
    success = test_complet_modifications()
    
    if success:
        print("\n🎉 CONFIRMATION : TOUTES LES MODIFICATIONS SONT APPLIQUÉES !")
        print("\n💡 CONSEIL : Si vous voyez encore l'ancien label, essayez de :")
        print("   1. Vider le cache du navigateur (Ctrl+F5)")
        print("   2. Recharger la page")
        print("   3. Vérifier que vous regardez la bonne page")
        return True
    else:
        print("\n⚠️  ATTENTION : Vérifiez les fichiers mentionnés")
        return False

if __name__ == "__main__":
    main()
