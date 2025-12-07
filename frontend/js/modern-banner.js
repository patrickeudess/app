// Script pour la bannière moderne uniformisée - Mon Cacao

class ModernBanner {
    constructor() {
        this.currentUser = this.getCurrentUser();
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    // Obtenir l'utilisateur actuel (simulation)
    getCurrentUser() {
        // En production, cela viendrait de l'authentification
        return {
            id: 1,
            username: "Agriculteur",
            isOnline: true,
            role: "Agriculteur"
        };
    }

    // Détecter la page actuelle
    getCurrentPage() {
        const path = window.location.pathname;
        const filename = path.split('/').pop();
        
        const pageMap = {
            'soumettre.html': { context: 'Soumettre', icon: '📥', subtitle: 'Soumission de données' },
            'historique.html': { context: 'Historique', icon: '📈', subtitle: 'Historique et analyses' },
            'analyse.html': { context: 'Analyse', icon: '📊', subtitle: 'Analyse détaillée' },
            'conseils.html': { context: 'Conseil', icon: '💡', subtitle: 'Conseils personnalisés' },
            'assistant.html': { context: 'Assistant', icon: '🤖', subtitle: 'Assistant IA' },
            'prediction.html': { context: 'Prédiction', icon: '🎯', subtitle: 'Prédiction IA' },
            'production.html': { context: 'Production', icon: '🌱', subtitle: 'Production cacao' },
            'revenus.html': { context: 'Revenus', icon: '💰', subtitle: 'Gestion des revenus' },
            'dashboard.html': { context: 'Dashboard', icon: '📊', subtitle: 'Tableau de bord' },
            'index.html': { context: 'Accueil', icon: '🏠', subtitle: 'Page d\'accueil' }
        };

        return pageMap[filename] || { context: '', icon: '🍃', subtitle: '' };
    }

    // Initialiser la bannière
    init() {
        this.createBanner();
        this.setupEventListeners();
        this.startAnimations();
    }

    // Créer la bannière moderne
    createBanner() {
        const header = document.querySelector('.app-header');
        if (!header) return;

        // Remplacer l'ancienne bannière par la nouvelle
        header.className = 'modern-header';
        header.innerHTML = this.generateBannerHTML();
    }

    // Générer le HTML de la bannière
    generateBannerHTML() {
        const statusClass = this.currentUser.isOnline ? 'online' : 'offline';
        const statusText = this.currentUser.isOnline ? 'En ligne' : 'Hors ligne';
        const pageContextHTML = this.currentPage.subtitle ? 
            `<span class="page-context">${this.currentPage.icon} ${this.currentPage.subtitle}</span>` : '';

        return `
            <div class="header-brand">
                <div class="logo-container">
                    <span class="logo-icon">🍃</span>
                    <span class="logo-text">🪙</span>
                </div>
                <div class="brand-info">
                    <h1>Mon Cacao</h1>
                    <div class="brand-status">
                        <div class="status-dot ${statusClass}"></div>
                        <span class="status-text">${statusText}</span>
                        <span class="user-info">👤 ${this.currentUser.role}</span>
                        ${pageContextHTML}
                    </div>
                </div>
            </div>
            <div class="header-actions">
                <span class="user-display">👤 ${this.currentUser.username}</span>
                <a href="index.html" class="btn-modern">
                    <i class="fas fa-arrow-left"></i>
                    Retour
                </a>
            </div>
        `;
    }

    // Configurer les événements
    setupEventListeners() {
        // Gestion du bouton retour
        const backBtn = document.querySelector('.btn-modern');
        if (backBtn) {
            backBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation();
            });
        }

        // Animation au survol du logo
        const logoContainer = document.querySelector('.logo-container');
        if (logoContainer) {
            logoContainer.addEventListener('mouseenter', () => {
                this.animateLogo();
            });
        }
    }

    // Gérer la navigation
    handleNavigation() {
        // Animation de transition
        document.body.style.opacity = '0.8';
        document.body.style.transition = 'opacity 0.3s ease';
        
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 300);
    }

    // Animer le logo
    animateLogo() {
        const logoIcons = document.querySelectorAll('.logo-icon, .logo-text');
        logoIcons.forEach((icon, index) => {
            icon.style.transform = 'scale(1.2) rotate(5deg)';
            icon.style.transition = 'transform 0.3s ease';
            
            setTimeout(() => {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }, 300 + (index * 100));
        });
    }

    // Démarrer les animations
    startAnimations() {
        // Animation d'entrée de la bannière
        const banner = document.querySelector('.modern-header');
        if (banner) {
            banner.style.opacity = '0';
            banner.style.transform = 'translateY(-20px)';
            banner.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                banner.style.opacity = '1';
                banner.style.transform = 'translateY(0)';
            }, 100);
        }

        // Animation des éléments de statut
        const statusElements = document.querySelectorAll('.status-dot, .status-text, .user-info');
        statusElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateX(-10px)';
            element.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateX(0)';
            }, 500 + (index * 100));
        });
    }

    // Mettre à jour le statut utilisateur
    updateUserStatus(isOnline) {
        this.currentUser.isOnline = isOnline;
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        if (statusDot && statusText) {
            statusDot.className = `status-dot ${isOnline ? 'online' : 'offline'}`;
            statusText.textContent = isOnline ? 'En ligne' : 'Hors ligne';
        }
    }

    // Changer de page
    changePage(pageContext) {
        this.currentPage = pageContext;
        const pageContextElement = document.querySelector('.page-context');
        
        if (pageContextElement && pageContext.subtitle) {
            pageContextElement.innerHTML = `${pageContext.icon} ${pageContext.subtitle}`;
        }
    }
}

// Initialiser la bannière moderne quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    window.modernBanner = new ModernBanner();
});

// Exposer la classe pour utilisation externe
window.ModernBanner = ModernBanner;
