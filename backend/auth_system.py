# -*- coding: utf-8 -*-
"""
Module d'authentification pour l'application MON CACAO
Gère l'inscription, la connexion et la gestion des comptes utilisateurs
"""

import sqlite3
import streamlit as st
import re
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class AuthSystem:
    def __init__(self, db_path="data.sqlite"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                region VARCHAR(100),
                user_type VARCHAR(20) DEFAULT 'agriculteur',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                consent_gdpr BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"
        return True, "Mot de passe valide"
    
    def register_user(self, username, email, password, first_name="", last_name="", region=""):
        try:
            if not self.validate_email(email):
                return False, "Format d'email invalide"
            
            if not self.validate_password(password)[0]:
                return False, self.validate_password(password)[1]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Nom d'utilisateur ou email déjà utilisé"
            
            password_hash = generate_password_hash(password, method='sha256')
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, first_name, last_name, region, consent_gdpr)
                VALUES (?, ?, ?, ?, ?, ?, TRUE)
            ''', (username, email, password_hash, first_name, last_name, region))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, f"Compte créé avec succès ! ID: {user_id}"
            
        except Exception as e:
            return False, f"Erreur: {str(e)}"
    
    def login_user(self, email, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, password_hash FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False, "Email ou mot de passe incorrect"
            
            user_id, username, password_hash = user
            
            if not check_password_hash(password_hash, password):
                conn.close()
                return False, "Email ou mot de passe incorrect"
            
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, session_token, expires_at))
            
            conn.commit()
            conn.close()
            
            return True, {
                "user_id": user_id,
                "username": username,
                "session_token": session_token
            }
            
        except Exception as e:
            return False, f"Erreur: {str(e)}"
    
    def verify_session(self, session_token):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username
            FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (session_token, datetime.now()))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {"user_id": user[0], "username": user[1]}
        return False, "Session invalide"
    
    def logout_user(self, session_token):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_sessions WHERE session_token = ?", (session_token,))
        conn.commit()
        conn.close()
        return True

auth = AuthSystem()
