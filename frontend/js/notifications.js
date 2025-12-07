/**
 * Système de notifications push pour Mon Cacao
 */
class NotificationManager {
    constructor() {
        this.permission = null;
        this.registration = null;
        this.init();
    }

    async init() {
        // Vérifier le support des notifications
        if (!('Notification' in window)) {
            console.log('Notifications non supportées');
            return;
        }

        // Vérifier le support du Service Worker
        if ('serviceWorker' in navigator) {
            try {
                this.registration = await navigator.serviceWorker.ready;
            } catch (error) {
                console.error('Erreur Service Worker:', error);
            }
        }

        // Demander la permission
        this.permission = Notification.permission;
        
        if (this.permission === 'default') {
            await this.requestPermission();
        }
    }

    async requestPermission() {
        if (!('Notification' in window)) {
            return false;
        }

        try {
            const permission = await Notification.requestPermission();
            this.permission = permission;
            return permission === 'granted';
        } catch (error) {
            console.error('Erreur demande permission:', error);
            return false;
        }
    }

    async showNotification(title, options = {}) {
        if (this.permission !== 'granted') {
            const granted = await this.requestPermission();
            if (!granted) {
                console.log('Permission de notification refusée');
                return;
            }
        }

        const defaultOptions = {
            body: '',
            icon: '/icon-192x192.png',
            badge: '/badge-72x72.png',
            tag: 'mon-cacao',
            requireInteraction: false,
            silent: false,
            ...options
        };

        // Utiliser Service Worker si disponible
        if (this.registration && 'showNotification' in this.registration) {
            await this.registration.showNotification(title, defaultOptions);
        } else {
            // Fallback sur Notification API
            new Notification(title, defaultOptions);
        }
    }

    async scheduleNotification(title, body, delay) {
        setTimeout(() => {
            this.showNotification(title, { body });
        }, delay);
    }

    async createNotificationFromAPI(notificationData) {
        const { title, message, type, url } = notificationData;
        
        await this.showNotification(title, {
            body: message,
            icon: this.getIconForType(type),
            data: { url: url || '/' },
            tag: `notification-${Date.now()}`
        });
    }

    getIconForType(type) {
        const icons = {
            'success': '/icon-success.png',
            'error': '/icon-error.png',
            'warning': '/icon-warning.png',
            'info': '/icon-info.png'
        };
        return icons[type] || '/icon-192x192.png';
    }

    // Écouter les notifications depuis le serveur
    async subscribeToPushNotifications() {
        if (!this.registration) {
            console.log('Service Worker non disponible');
            return null;
        }

        try {
            const subscription = await this.registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array('YOUR_VAPID_PUBLIC_KEY') // À configurer
            });

            // Envoyer la subscription au serveur
            await fetch('/api/notifications/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(subscription)
            });

            return subscription;
        } catch (error) {
            console.error('Erreur abonnement push:', error);
            return null;
        }
    }

    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
}

// Instance globale
const notificationManager = new NotificationManager();

// Exporter
window.notificationManager = notificationManager;

