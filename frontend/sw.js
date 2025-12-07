/**
 * Service Worker pour Mon Cacao
 * Gère le mode hors ligne, le cache et les notifications push
 */

const CACHE_NAME = 'mon-cacao-v2.0';
const OFFLINE_URL = 'offline.html';

// Fichiers à mettre en cache (chemins relatifs pour fonctionner avec ou sans serveur)
const CACHE_FILES = [
    './',
    './index.html',
    './user-type-selection.html',
    './auth.html',
    './dashboard-professionnel.html',
    './mes-producteurs.html',
    './estimation-production.html',
    './analyse-conseils.html',
    './statistiques.html',
    './graphiques.html',
    './rapports.html',
    './css/style.css',
    './css/modern-banner.css',
    './js/script.js',
    './js/auth.js',
    './js/database-sync.js',
    './offline.html'
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installation...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Mise en cache des fichiers');
                return cache.addAll(CACHE_FILES);
            })
            .then(() => {
                return self.skipWaiting(); // Activer immédiatement
            })
    );
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activation...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Suppression ancien cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            return self.clients.claim(); // Prendre le contrôle immédiatement
        })
    );
});

// Interception des requêtes réseau
self.addEventListener('fetch', (event) => {
    // Ignorer les requêtes non-GET
    if (event.request.method !== 'GET') {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Retourner depuis le cache si disponible
                if (response) {
                    return response;
                }
                
                // Sinon, faire la requête réseau
                return fetch(event.request)
                    .then((response) => {
                        // Vérifier si la réponse est valide
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // Cloner la réponse pour le cache
                        const responseToCache = response.clone();
                        
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    })
                    .catch(() => {
                        // Si hors ligne et que c'est une page HTML, retourner la page offline
                        if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
                            return caches.match(OFFLINE_URL) || caches.match('./offline.html');
                        }
                    });
            })
    );
});

// Gestion des notifications push
self.addEventListener('push', (event) => {
    console.log('[Service Worker] Notification push reçue');
    
    let notificationData = {
        title: 'Mon Cacao',
        body: 'Vous avez une nouvelle notification',
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png',
        tag: 'mon-cacao-notification'
    };
    
    if (event.data) {
        try {
            const data = event.data.json();
            notificationData = {
                ...notificationData,
                ...data
            };
        } catch (e) {
            notificationData.body = event.data.text();
        }
    }
    
    event.waitUntil(
        self.registration.showNotification(notificationData.title, {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            tag: notificationData.tag,
            data: notificationData.data || {},
            requireInteraction: notificationData.requireInteraction || false,
            actions: notificationData.actions || []
        })
    );
});

// Gestion du clic sur les notifications
self.addEventListener('notificationclick', (event) => {
    console.log('[Service Worker] Clic sur notification');
    
    event.notification.close();
    
    const urlToOpen = event.notification.data.url || './index.html';
    
    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        }).then((clientList) => {
            // Si une fenêtre est déjà ouverte, la focus
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if (client.url === urlToOpen && 'focus' in client) {
                    return client.focus();
                }
            }
            
            // Sinon, ouvrir une nouvelle fenêtre
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen);
            }
        })
    );
});

// Synchronisation en arrière-plan
self.addEventListener('sync', (event) => {
    console.log('[Service Worker] Synchronisation:', event.tag);
    
    if (event.tag === 'sync-data') {
        event.waitUntil(syncPendingData());
    }
});

async function syncPendingData() {
    try {
        // Synchroniser les données en attente
        if (typeof dbSync !== 'undefined' && dbSync.syncPendingData) {
            await dbSync.syncPendingData();
        }
        
        // Notifier tous les clients
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'SYNC_COMPLETE',
                timestamp: new Date().toISOString()
            });
        });
    } catch (error) {
        console.error('[Service Worker] Erreur synchronisation:', error);
    }
}

// Gestion des messages depuis le client
self.addEventListener('message', (event) => {
    console.log('[Service Worker] Message reçu:', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});

