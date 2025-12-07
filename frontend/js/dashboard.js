// Navigation entre les pages
function navigateTo(page) {
    // Mettre à jour la navigation active
    updateActiveNavigation(page);
    
    // Navigation vers les différentes pages
    switch(page) {
        case 'dashboard':
            window.location.href = 'dashboard.html';
            break;
        case 'prediction':
            window.location.href = 'index.html#prediction';
            break;
        case 'production':
            window.location.href = 'production.html';
            break;
        case 'revenue':
            window.location.href = 'revenus.html';
            break;
        case 'ai-advice':
            window.location.href = 'ai-advice.html';
            break;
        case 'goals':
            window.location.href = 'goals.html';
            break;
        case 'tips':
            window.location.href = 'tips.html';
            break;
        case 'security':
            window.location.href = 'security.html';
            break;
        case 'badges':
            window.location.href = 'badges.html';
            break;
        case 'profile':
            window.location.href = 'profile.html';
            break;
        default:
            console.log('Page non trouvée:', page);
    }
}

// Mettre à jour la navigation active
function updateActiveNavigation(activePage) {
    // Mettre à jour la navigation bottom
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeNavItem = document.querySelector(`[onclick="navigateTo('${activePage}')"]`);
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
}

// Fonction de déconnexion
function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        // Ici vous pouvez ajouter la logique de déconnexion
        localStorage.removeItem('user_session');
        window.location.href = 'login.html';
    }
}

// Charger les données du dashboard
function loadDashboardData() {
    // Simuler le chargement des données depuis l'API
    fetch('http://localhost:5000/dashboard-stats')
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
        })
        .catch(error => {
            console.log('Utilisation des données par défaut');
            loadDefaultStats();
        });
}

// Mettre à jour les statistiques du dashboard
function updateDashboardStats(data) {
    // Mettre à jour les statistiques avec les vraies données
    document.querySelector('.stat-value').textContent = data.productivity + ' t/ha';
    document.querySelectorAll('.stat-value')[1].textContent = formatNumber(data.revenue) + ' FCFA';
    document.querySelectorAll('.stat-value')[2].textContent = formatNumber(data.benefit) + ' FCFA';
}

// Charger les statistiques par défaut
function loadDefaultStats() {
    // Données par défaut si l'API n'est pas disponible
    const defaultStats = {
        productivity: '1.25',
        revenue: '937,500',
        benefit: '487,500'
    };
    
    updateDashboardStats(defaultStats);
}

// Formater les nombres avec des espaces
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

// Animation des cartes au scroll
function animateCardsOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observer les cartes de fonctionnalités
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Observer les cartes de statistiques
    document.querySelectorAll('.stat-card').forEach(card => {
        observer.observe(card);
    });
}

// Vérifier le statut de connexion
function checkConnectionStatus() {
    fetch('http://localhost:5000/health')
        .then(response => {
            if (response.ok) {
                updateStatusIndicator('online');
            } else {
                updateStatusIndicator('offline');
            }
        })
        .catch(error => {
            updateStatusIndicator('offline');
        });
}

// Mettre à jour l'indicateur de statut
function updateStatusIndicator(status) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-indicator span');
    
    if (status === 'online') {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'En ligne';
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Hors ligne';
    }
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 1rem;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        warning: 'exclamation-triangle',
        error: 'times-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        success: '#28a745',
        warning: '#ffc107',
        error: '#dc3545',
        info: '#2E8B57'
    };
    return colors[type] || '#2E8B57';
}

// Animation CSS pour les notifications
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0;
        font-size: 1rem;
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
`;
document.head.appendChild(notificationStyle);

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Charger les données du dashboard
    loadDashboardData();
    
    // Animer les cartes au scroll
    animateCardsOnScroll();
    
    // Vérifier le statut de connexion
    checkConnectionStatus();
    
    // Vérifier le statut toutes les 30 secondes
    setInterval(checkConnectionStatus, 30000);
    
    // Ajouter des effets de hover aux cartes
    addHoverEffects();
    
    // Initialiser les tooltips
    initializeTooltips();
});

// Ajouter des effets de hover
function addHoverEffects() {
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialiser les tooltips
function initializeTooltips() {
    document.querySelectorAll('.feature-card').forEach(card => {
        const title = card.querySelector('h3').textContent;
        card.setAttribute('title', title);
    });
}

// Gestion des erreurs globales
window.addEventListener('error', (event) => {
    console.error('Erreur JavaScript:', event.error);
    showNotification('Une erreur est survenue. Veuillez rafraîchir la page.', 'error');
});

// Gestion de la connexion réseau
window.addEventListener('online', () => {
    showNotification('Connexion rétablie', 'success');
    checkConnectionStatus();
});

window.addEventListener('offline', () => {
    showNotification('Connexion perdue', 'warning');
    checkConnectionStatus();
});

// Service Worker pour le cache (optionnel)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW enregistré:', registration);
            })
            .catch(registrationError => {
                console.log('SW échec:', registrationError);
            });
    });
}
