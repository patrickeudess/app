/**
 * Navigation et authentification pour MON CACAO
 * Gère la navigation entre les pages et l'état de connexion
 */

class CacaoNavigation {
    constructor() {
        this.currentUser = null;
        this.isAuthenticated = false;
        this.init();
    }

    init() {
        this.checkAuthStatus();
        this.setupEventListeners();
        this.updateNavigation();
    }

    /**
     * Vérifie le statut d'authentification
     */
    checkAuthStatus() {
        const token = localStorage.getItem('cacao_token');
        const user = localStorage.getItem('cacao_user');
        
        if (token && user) {
            try {
                this.currentUser = JSON.parse(user);
                this.isAuthenticated = true;
                this.validateToken(token);
            } catch (error) {
                this.logout();
            }
        }
    }

    /**
     * Valide le token d'authentification
     */
    async validateToken(token) {
        try {
            // Ici, vous pouvez ajouter une validation côté serveur
            // Pour l'instant, on simule une validation
            const isValid = await this.checkTokenValidity(token);
            if (!isValid) {
                this.logout();
            }
        } catch (error) {
            console.error('Erreur de validation du token:', error);
            this.logout();
        }
    }

    /**
     * Vérifie la validité du token (simulation)
     */
    async checkTokenValidity(token) {
        // Simulation d'une vérification de token
        // Remplacez par un appel API réel
        return new Promise((resolve) => {
            setTimeout(() => {
                // Vérifier si le token n'est pas expiré
                const tokenData = this.parseToken(token);
                if (tokenData && tokenData.exp > Date.now() / 1000) {
                    resolve(true);
                } else {
                    resolve(false);
                }
            }, 100);
        });
    }

    /**
     * Parse le token JWT (simulation)
     */
    parseToken(token) {
        try {
            // Simulation du parsing d'un token JWT
            // En réalité, utilisez une bibliothèque comme jwt-decode
            return {
                exp: Date.now() / 1000 + 3600, // Expire dans 1 heure
                user_id: this.currentUser?.id || 1
            };
        } catch (error) {
            return null;
        }
    }

    /**
     * Configure les écouteurs d'événements
     */
    setupEventListeners() {
        // Navigation entre les pages
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-nav]')) {
                e.preventDefault();
                this.navigateTo(e.target.getAttribute('data-nav'));
            }
        });

        // Gestion de la déconnexion
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-logout]')) {
                e.preventDefault();
                this.logout();
            }
        });

        // Gestion des formulaires d'authentification
        this.setupAuthForms();
    }

    /**
     * Configure les formulaires d'authentification
     */
    setupAuthForms() {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }
    }

    /**
     * Gère la connexion utilisateur
     */
    async handleLogin(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const email = formData.get('email');
        const password = formData.get('password');
        const rememberMe = formData.get('rememberMe');

        try {
            this.showMessage('Connexion en cours...', 'info');
            
            // Simulation d'une connexion API
            const success = await this.authenticateUser(email, password);
            
            if (success) {
                this.showMessage('Connexion réussie !', 'success');
                setTimeout(() => {
                    this.redirectToDashboard();
                }, 1500);
            } else {
                this.showMessage('Email ou mot de passe incorrect', 'error');
            }
        } catch (error) {
            this.showMessage('Erreur lors de la connexion', 'error');
        }
    }

    /**
     * Gère l'inscription utilisateur
     */
    async handleRegister(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const username = formData.get('username');
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');
        const acceptPolicy = formData.get('acceptPolicy');

        // Validation côté client
        if (!this.validateRegistrationData(username, email, password, confirmPassword, acceptPolicy)) {
            return;
        }

        try {
            this.showMessage('Création du compte en cours...', 'info');
            
            // Simulation d'une inscription API
            const success = await this.registerUser(username, email, password, formData);
            
            if (success) {
                this.showMessage('Compte créé avec succès !', 'success');
                setTimeout(() => {
                    this.switchToLogin();
                }, 1500);
            } else {
                this.showMessage('Erreur lors de la création du compte', 'error');
            }
        } catch (error) {
            this.showMessage('Erreur lors de l\'inscription', 'error');
        }
    }

    /**
     * Valide les données d'inscription
     */
    validateRegistrationData(username, email, password, confirmPassword, acceptPolicy) {
        if (!username || !email || !password || !confirmPassword) {
            this.showMessage('Tous les champs sont obligatoires', 'error');
            return false;
        }

        if (password.length < 8) {
            this.showMessage('Le mot de passe doit contenir au moins 8 caractères', 'error');
            return false;
        }

        if (password !== confirmPassword) {
            this.showMessage('Les mots de passe ne correspondent pas', 'error');
            return false;
        }

        if (!acceptPolicy) {
            this.showMessage('Vous devez accepter la politique de gestion des données', 'error');
            return false;
        }

        return true;
    }

    /**
     * Authentifie un utilisateur (simulation)
     */
    async authenticateUser(email, password) {
        // Simulation d'une API d'authentification
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simuler une vérification d'identifiants
                if (email && password) {
                    const user = {
                        id: 1,
                        username: email.split('@')[0],
                        email: email,
                        region: 'Abidjan',
                        user_type: 'agriculteur'
                    };
                    
                    this.currentUser = user;
                    this.isAuthenticated = true;
                    
                    // Stocker les informations de session
                    const token = this.generateToken(user);
                    localStorage.setItem('cacao_token', token);
                    localStorage.setItem('cacao_user', JSON.stringify(user));
                    
                    resolve(true);
                } else {
                    resolve(false);
                }
            }, 1000);
        });
    }

    /**
     * Inscrit un nouvel utilisateur (simulation)
     */
    async registerUser(username, email, password, formData) {
        // Simulation d'une API d'inscription
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simuler la création d'un compte
                const user = {
                    id: Date.now(),
                    username: username,
                    email: email,
                    first_name: formData.get('firstName') || '',
                    last_name: formData.get('lastName') || '',
                    region: formData.get('region') || 'Abidjan',
                    user_type: 'agriculteur'
                };
                
                // Stocker l'utilisateur (simulation)
                localStorage.setItem('cacao_new_user', JSON.stringify(user));
                
                resolve(true);
            }, 1000);
        });
    }

    /**
     * Génère un token d'authentification (simulation)
     */
    generateToken(user) {
        // Simulation d'un token JWT
        const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
        const payload = btoa(JSON.stringify({
            user_id: user.id,
            username: user.username,
            exp: Date.now() / 1000 + 3600
        }));
        const signature = btoa('signature_simulation');
        
        return `${header}.${payload}.${signature}`;
    }

    /**
     * Navigue vers une page spécifique
     */
    navigateTo(page) {
        if (!this.isAuthenticated && page !== 'index') {
            this.showMessage('Veuillez vous connecter pour accéder à cette page', 'warning');
            return;
        }

        const pageMap = {
            'index': 'index.html',
            'dashboard': 'dashboard.html',
            'prediction': 'prediction.html',
            'analyse': 'analyse.html',
            'soumettre': 'soumettre.html',
            'historique': 'historique.html',
            'score-ecologique': 'score-ecologique.html',
            'assistant': 'assistant.html',
            'conseils': 'conseils.html',
            'revenue': 'revenus.html',
            'production': 'production.html',
            'revenus': 'revenus.html'
        };

        const targetPage = pageMap[page];
        if (targetPage) {
            window.location.href = targetPage;
        }
    }

    /**
     * Redirige vers le tableau de bord
     */
    redirectToDashboard() {
        window.location.href = 'dashboard.html';
    }

    /**
     * Bascule vers le formulaire de connexion
     */
    switchToLogin() {
        if (typeof switchTab === 'function') {
            switchTab('login');
        }
    }

    /**
     * Déconnecte l'utilisateur
     */
    logout() {
        this.currentUser = null;
        this.isAuthenticated = false;
        
        // Nettoyer le stockage local
        localStorage.removeItem('cacao_token');
        localStorage.removeItem('cacao_user');
        
        // Rediriger vers la page d'accueil
        window.location.href = 'index.html';
    }

    /**
     * Met à jour la navigation selon l'état d'authentification
     */
    updateNavigation() {
        const navElements = document.querySelectorAll('[data-auth]');
        
        navElements.forEach(element => {
            const authRequired = element.getAttribute('data-auth') === 'required';
            const authForbidden = element.getAttribute('data-auth') === 'forbidden';
            
            if (authRequired && !this.isAuthenticated) {
                element.style.display = 'none';
            } else if (authForbidden && this.isAuthenticated) {
                element.style.display = 'none';
            } else {
                element.style.display = '';
            }
        });

        // Mettre à jour l'affichage du nom d'utilisateur
        const usernameElements = document.querySelectorAll('[data-username]');
        usernameElements.forEach(element => {
            if (this.isAuthenticated && this.currentUser) {
                element.textContent = this.currentUser.username;
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        });
    }

    /**
     * Affiche un message à l'utilisateur
     */
    showMessage(text, type = 'info') {
        // Supprimer les messages existants
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        // Créer un nouveau message
        const message = document.createElement('div');
        message.className = `message ${type}`;
        
        const iconMap = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        
        message.innerHTML = `
            <i class="fas fa-${iconMap[type] || 'info-circle'}"></i> 
            ${text}
        `;
        
        // Insérer le message dans le formulaire actif
        const activeForm = document.querySelector('.auth-form.active') || document.querySelector('form');
        if (activeForm) {
            const submitButton = activeForm.querySelector('.btn');
            if (submitButton) {
                submitButton.parentNode.insertBefore(message, submitButton);
            } else {
                activeForm.appendChild(message);
            }
        }
        
        // Auto-suppression après 5 secondes
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 5000);
    }

    /**
     * Vérifie si l'utilisateur est connecté
     */
    isUserAuthenticated() {
        return this.isAuthenticated;
    }

    /**
     * Récupère les informations de l'utilisateur actuel
     */
    getCurrentUser() {
        return this.currentUser;
    }
}

// Initialisation de la navigation
document.addEventListener('DOMContentLoaded', () => {
    window.cacaoNav = new CacaoNavigation();
});

// Export pour utilisation dans d'autres fichiers
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CacaoNavigation;
}
