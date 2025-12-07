// JavaScript pour la page d'accueil avec lecture vocale et offline-first

// Variables globales
let speechSynthesis = window.speechSynthesis;
let currentUtterance = null;

// Base de données locale (SQLite simulé avec localStorage)
const localDB = {
    // Sauvegarder des données localement
    saveData: function(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify({
                data: data,
                timestamp: new Date().toISOString(),
                synced: false
            }));
            console.log(`Données sauvegardées localement: ${key}`);
            return true;
        } catch (error) {
            console.error('Erreur sauvegarde locale:', error);
            return false;
        }
    },

    // Récupérer des données localement
    getData: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Erreur récupération locale:', error);
            return null;
        }
    },

    // Marquer comme synchronisé
    markSynced: function(key) {
        try {
            const item = this.getData(key);
            if (item) {
                item.synced = true;
                localStorage.setItem(key, JSON.stringify(item));
            }
        } catch (error) {
            console.error('Erreur marquage synced:', error);
        }
    },

    // Obtenir toutes les données non synchronisées
    getUnsyncedData: function() {
        const unsynced = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const item = this.getData(key);
            if (item && !item.synced) {
                unsynced.push({ key, data: item });
            }
        }
        return unsynced;
    }
};

// Fonction de lecture vocale
function speakText(text, options = {}) {
    // Arrêter la lecture en cours
    if (currentUtterance) {
        speechSynthesis.cancel();
    }

    // Créer un nouvel utterance
    currentUtterance = new SpeechSynthesisUtterance(text);
    
    // Configuration par défaut
    currentUtterance.lang = 'fr-FR';
    currentUtterance.rate = 0.9; // Vitesse légèrement ralentie
    currentUtterance.pitch = 1.0;
    currentUtterance.volume = 1.0;

    // Appliquer les options personnalisées
    Object.assign(currentUtterance, options);

    // Événements
    currentUtterance.onstart = () => {
        console.log('Lecture vocale démarrée');
        updateListenButton(true);
    };

    currentUtterance.onend = () => {
        console.log('Lecture vocale terminée');
        updateListenButton(false);
        currentUtterance = null;
    };

    currentUtterance.onerror = (event) => {
        console.error('Erreur lecture vocale:', event);
        updateListenButton(false);
        currentUtterance = null;
        showNotification('Erreur de lecture vocale', 'error');
    };

    // Démarrer la lecture
    speechSynthesis.speak(currentUtterance);
}

// Mettre à jour l'état des boutons d'écoute
function updateListenButton(isPlaying) {
    const buttons = document.querySelectorAll('.listen-btn, .listen-btn-small');
    buttons.forEach(btn => {
        const icon = btn.querySelector('i');
        if (isPlaying) {
            icon.className = 'fas fa-stop';
            btn.style.background = 'var(--danger-color)';
        } else {
            icon.className = 'fas fa-volume-up';
            btn.style.background = '';
        }
    });
}

// Arrêter la lecture vocale
function stopSpeaking() {
    if (currentUtterance) {
        speechSynthesis.cancel();
        currentUtterance = null;
        updateListenButton(false);
    }
}

// Navigation avec sauvegarde locale
function navigateTo(page) {
    // Sauvegarder la navigation actuelle
    localDB.saveData('lastPage', page);
    
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
        case 'submit-data':
            window.location.href = 'submit-data.html';
            break;
        case 'history':
            window.location.href = 'history.html';
            break;
        case 'ai-assistant':
            window.location.href = 'ai-assistant.html';
            break;
        case 'analysis':
            window.location.href = 'analysis.html';
            break;
        case 'revenue':
            window.location.href = 'revenus.html';
            break;
        case 'production':
            window.location.href = 'production.html';
            break;
        case 'tips':
            window.location.href = 'tips.html';
            break;
        case 'profile':
            window.location.href = 'profile.html';
            break;
        default:
            console.log('Page non trouvée:', page);
    }
}

// Synchronisation des données
async function syncData() {
    if (!navigator.onLine) {
        console.log('Pas de connexion, synchronisation différée');
        return;
    }

    const unsyncedData = localDB.getUnsyncedData();
    if (unsyncedData.length === 0) {
        console.log('Aucune donnée à synchroniser');
        return;
    }

    try {
        console.log(`Synchronisation de ${unsyncedData.length} éléments...`);
        
        for (const item of unsyncedData) {
            // Envoyer les données à l'API
            const response = await fetch('http://localhost:5000/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    key: item.key,
                    data: item.data.data,
                    timestamp: item.data.timestamp
                })
            });

            if (response.ok) {
                localDB.markSynced(item.key);
                console.log(`Données synchronisées: ${item.key}`);
            } else {
                console.error(`Erreur synchronisation: ${item.key}`);
            }
        }

        showNotification('Données synchronisées avec succès', 'success');
    } catch (error) {
        console.error('Erreur synchronisation:', error);
        showNotification('Erreur de synchronisation', 'error');
    }
}

// Vérifier le statut de connexion
function checkConnectionStatus() {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-indicator span');
    
    if (navigator.onLine) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'En ligne';
        
        // Synchroniser les données quand la connexion revient
        syncData();
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Hors ligne';
    }
}

// Charger les données du statut
function loadStatusData() {
    // Simuler le chargement des données de statut
    const statusData = localDB.getData('statusData') || {
        production: 'green',
        climate: 'orange',
        revenue: 'green'
    };

    updateStatusDisplay(statusData);
}

// Mettre à jour l'affichage du statut
function updateStatusDisplay(statusData) {
    const statusItems = document.querySelectorAll('.status-item');
    
    statusItems.forEach(item => {
        const icon = item.querySelector('i');
        const text = item.querySelector('span');
        
        if (icon.classList.contains('fa-seedling')) {
            updateStatusItem(item, statusData.production, 'Production OK', 'Production à surveiller', 'Production en alerte');
        } else if (icon.classList.contains('fa-thermometer-half')) {
            updateStatusItem(item, statusData.climate, 'Climat OK', 'Climat à surveiller', 'Climat en alerte');
        } else if (icon.classList.contains('fa-coins')) {
            updateStatusItem(item, statusData.revenue, 'Revenus stables', 'Revenus à surveiller', 'Revenus en alerte');
        }
    });
}

// Mettre à jour un élément de statut
function updateStatusItem(item, status, okText, warningText, alertText) {
    item.className = `status-item ${status}`;
    const text = item.querySelector('span');
    
    switch(status) {
        case 'green':
            text.textContent = okText;
            break;
        case 'orange':
            text.textContent = warningText;
            break;
        case 'red':
            text.textContent = alertText;
            break;
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
        font-size: 16px;
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

// Gestion des événements tactiles
function addTouchSupport() {
    // Empêcher le zoom sur double-tap
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (event) => {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);

    // Améliorer la réactivité tactile
    document.addEventListener('touchstart', () => {}, {passive: true});
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌱 Mon Cacao - Page d\'accueil chargée');
    
    // Charger les données de statut
    loadStatusData();
    
    // Vérifier le statut de connexion
    checkConnectionStatus();
    
    // Ajouter le support tactile
    addTouchSupport();
    
    // Événements de connexion
    window.addEventListener('online', () => {
        showNotification('Connexion rétablie', 'success');
        checkConnectionStatus();
    });
    
    window.addEventListener('offline', () => {
        showNotification('Mode hors ligne activé', 'warning');
        checkConnectionStatus();
    });
    
    // Synchronisation périodique
    setInterval(syncData, 30000); // Toutes les 30 secondes
    
    // Vérification du statut périodique
    setInterval(checkConnectionStatus, 10000); // Toutes les 10 secondes
    
    // Arrêter la lecture vocale quand on quitte la page
    window.addEventListener('beforeunload', stopSpeaking);
    
    // Gestion des erreurs globales
    window.addEventListener('error', (event) => {
        console.error('Erreur JavaScript:', event.error);
        showNotification('Une erreur est survenue', 'error');
    });
});

// Service Worker pour le cache (offline-first)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker enregistré:', registration);
            })
            .catch(registrationError => {
                console.log('Service Worker échec:', registrationError);
            });
    });
}

// Fonction de déconnexion
function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        // Sauvegarder les données avant déconnexion
        localDB.saveData('logoutTime', new Date().toISOString());
        
        // Synchroniser avant déconnexion
        syncData().then(() => {
            localStorage.removeItem('user_session');
            window.location.href = 'login.html';
        });
    }
}
