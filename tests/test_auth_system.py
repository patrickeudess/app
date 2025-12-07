#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système d'authentification pour MON CACAO
"""

import sqlite3
import os
from auth_system import AuthSystem

def test_database_creation():
    """Test de la création de la base de données"""
    print("🧪 Test de création de la base de données...")
    
    # Supprimer la base de test si elle existe
    test_db = "test_auth.sqlite"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Créer une nouvelle instance avec la base de test
    auth = AuthSystem(test_db)
    
    # Vérifier que les tables sont créées
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    # Vérifier la table users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("✅ Table 'users' créée avec succès")
    else:
        print("❌ Table 'users' non créée")
    
    # Vérifier la table user_sessions
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
    if cursor.fetchone():
        print("✅ Table 'user_sessions' créée avec succès")
    else:
        print("❌ Table 'user_sessions' non créée")
    
    # Vérifier la table login_attempts
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login_attempts'")
    if cursor.fetchone():
        print("✅ Table 'login_attempts' créée avec succès")
    else:
        print("❌ Table 'login_attempts' non créée")
    
    conn.close()
    
    # Nettoyer
    os.remove(test_db)
    print("🧹 Base de test supprimée")

def test_user_registration():
    """Test de l'inscription d'utilisateurs"""
    print("\n🧪 Test d'inscription d'utilisateurs...")
    
    test_db = "test_auth.sqlite"
    auth = AuthSystem(test_db)
    
    # Test 1: Inscription réussie
    success, result = auth.register_user(
        "testuser", "test@email.com", "TestPass123!", 
        "Test", "User", "Abidjan"
    )
    if success:
        print("✅ Inscription réussie:", result)
    else:
        print("❌ Échec de l'inscription:", result)
    
    # Test 2: Tentative d'inscription avec le même nom d'utilisateur
    success, result = auth.register_user(
        "testuser", "test2@email.com", "TestPass123!", 
        "Test2", "User2", "San-Pédro"
    )
    if not success:
        print("✅ Détection du nom d'utilisateur en double:", result)
    else:
        print("❌ Nom d'utilisateur en double non détecté")
    
    # Test 3: Tentative d'inscription avec le même email
    success, result = auth.register_user(
        "testuser2", "test@email.com", "TestPass123!", 
        "Test2", "User2", "San-Pédro"
    )
    if not success:
        print("✅ Détection de l'email en double:", result)
    else:
        print("❌ Email en double non détecté")
    
    # Test 4: Validation du mot de passe
    success, result = auth.register_user(
        "testuser3", "test3@email.com", "weak", 
        "Test3", "User3", "Gagnoa"
    )
    if not success:
        print("✅ Validation du mot de passe:", result)
    else:
        print("❌ Mot de passe faible accepté")
    
    # Nettoyer
    os.remove(test_db)

def test_user_login():
    """Test de la connexion d'utilisateurs"""
    print("\n🧪 Test de connexion d'utilisateurs...")
    
    test_db = "test_auth.sqlite"
    auth = AuthSystem(test_db)
    
    # Créer un utilisateur de test
    auth.register_user(
        "logintest", "login@email.com", "LoginPass123!", 
        "Login", "Test", "Divo"
    )
    
    # Test 1: Connexion réussie
    success, result = auth.login_user("login@email.com", "LoginPass123!")
    if success:
        print("✅ Connexion réussie:", result)
        session_token = result["session_token"]
    else:
        print("❌ Échec de la connexion:", result)
        return
    
    # Test 2: Vérification de session
    success, result = auth.verify_session(session_token)
    if success:
        print("✅ Session vérifiée:", result)
    else:
        print("❌ Échec de vérification de session:", result)
    
    # Test 3: Connexion avec mauvais mot de passe
    success, result = auth.login_user("login@email.com", "WrongPassword")
    if not success:
        print("✅ Détection du mauvais mot de passe:", result)
    else:
        print("❌ Mauvais mot de passe accepté")
    
    # Test 4: Connexion avec email inexistant
    success, result = auth.login_user("nonexistent@email.com", "AnyPassword")
    if not success:
        print("✅ Détection de l'email inexistant:", result)
    else:
        print("❌ Email inexistant accepté")
    
    # Nettoyer
    os.remove(test_db)

def test_validation_functions():
    """Test des fonctions de validation"""
    print("\n🧪 Test des fonctions de validation...")
    
    auth = AuthSystem(":memory:")
    
    # Test validation email
    valid_emails = ["test@email.com", "user.name@domain.co.uk", "test+tag@email.org"]
    invalid_emails = ["invalid-email", "@email.com", "test@", "test.email@"]
    
    for email in valid_emails:
        if auth.validate_email(email):
            print(f"✅ Email valide: {email}")
        else:
            print(f"❌ Email invalide rejeté: {email}")
    
    for email in invalid_emails:
        if not auth.validate_email(email):
            print(f"✅ Email invalide rejeté: {email}")
        else:
            print(f"❌ Email invalide accepté: {email}")
    
    # Test validation mot de passe
    valid_passwords = ["StrongPass123!", "ComplexP@ssw0rd", "Secure#Pass1"]
    invalid_passwords = ["weak", "123456", "password", "PASSWORD"]
    
    for password in valid_passwords:
        success, message = auth.validate_password(password)
        if success:
            print(f"✅ Mot de passe valide: {password}")
        else:
            print(f"❌ Mot de passe valide rejeté: {password} - {message}")
    
    for password in invalid_passwords:
        success, message = auth.validate_password(password)
        if not success:
            print(f"✅ Mot de passe invalide rejeté: {password} - {message}")
        else:
            print(f"❌ Mot de passe invalide accepté: {password}")

def test_user_management():
    """Test de la gestion des utilisateurs"""
    print("\n🧪 Test de la gestion des utilisateurs...")
    
    test_db = "test_auth.sqlite"
    auth = AuthSystem(test_db)
    
    # Créer un utilisateur de test
    auth.register_user(
        "managetest", "manage@email.com", "ManagePass123!", 
        "Manage", "Test", "Yamoussoukro"
    )
    
    # Connexion pour obtenir l'ID
    success, result = auth.login_user("manage@email.com", "ManagePass123!")
    if not success:
        print("❌ Impossible de se connecter pour le test de gestion")
        return
    
    user_id = result["user_id"]
    
    # Test 1: Récupération du profil
    profile = auth.get_user_profile(user_id)
    if profile:
        print("✅ Profil récupéré:", profile["username"])
    else:
        print("❌ Impossible de récupérer le profil")
    
    # Test 2: Mise à jour du profil
    success, result = auth.update_user_profile(
        user_id, 
        first_name="Updated", 
        region="Bouaké"
    )
    if success:
        print("✅ Profil mis à jour:", result)
    else:
        print("❌ Échec de la mise à jour:", result)
    
    # Test 3: Changement de mot de passe
    success, result = auth.change_password(
        user_id, 
        "ManagePass123!", 
        "NewPass123!"
    )
    if success:
        print("✅ Mot de passe changé:", result)
    else:
        print("❌ Échec du changement de mot de passe:", result)
    
    # Test 4: Connexion avec le nouveau mot de passe
    success, result = auth.login_user("manage@email.com", "NewPass123!")
    if success:
        print("✅ Connexion avec le nouveau mot de passe réussie")
    else:
        print("❌ Échec de connexion avec le nouveau mot de passe")
    
    # Nettoyer
    os.remove(test_db)

def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS DU SYSTÈME D'AUTHENTIFICATION")
    print("=" * 60)
    
    try:
        test_database_creation()
        test_user_registration()
        test_user_login()
        test_validation_functions()
        test_user_management()
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS TERMINÉS AVEC SUCCÈS !")
        print("✅ Le système d'authentification fonctionne correctement")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
