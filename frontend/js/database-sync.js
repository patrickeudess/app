/**
 * Système de synchronisation avec la base de données backend
 * Remplace progressivement localStorage par des appels API
 */
const API_BASE_URL = 'http://localhost:5000/api';

class DatabaseSync {
    constructor() {
        this.syncQueue = [];
        this.isOnline = navigator.onLine;
        this.setupOfflineHandling();
    }

    setupOfflineHandling() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.syncPendingData();
            this.showNotification('Connexion rétablie. Synchronisation en cours...', 'success');
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNotification('Mode hors ligne activé. Les données seront synchronisées plus tard.', 'info');
        });
    }

    // ========== AUTHENTIFICATION ==========

    async register(username, password, userType, email = null, phone = null, region = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, user_type: userType, email, phone, region })
            });

            const result = await response.json();
            
            if (result.success) {
                // Sauvegarder localement aussi pour mode hors ligne
                this.saveToLocalStorage('user_account', {
                    id: result.user_id,
                    username,
                    user_type: userType,
                    email,
                    phone,
                    region
                });
            }
            
            return result;
        } catch (error) {
            // Mode hors ligne - utiliser localStorage
            return this.registerOffline(username, password, userType, email, phone, region);
        }
    }

    async login(identifier, password, twoFactorToken = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ identifier, password, two_factor_token: twoFactorToken })
            });

            const result = await response.json();
            
            if (result.success) {
                localStorage.setItem('user_authenticated', 'true');
                localStorage.setItem('current_user_id', result.user.id);
                localStorage.setItem('user_type', result.user.user_type);
                localStorage.setItem('user_type_selected', result.user.user_type);
            }
            
            return result;
        } catch (error) {
            return this.loginOffline(identifier, password);
        }
    }

    async enable2FA(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/enable-2fa`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId })
            });

            return await response.json();
        } catch (error) {
            return { success: false, error: 'Erreur de connexion' };
        }
    }

    async resetPassword(identifier) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ identifier })
            });

            return await response.json();
        } catch (error) {
            return { success: false, error: 'Erreur de connexion' };
        }
    }

    // ========== PRODUCTEURS ==========

    async createProducer(professionalId, name, region, phone = null, email = null, notes = null) {
        const data = { professional_id: professionalId, name, region, phone, email, notes };
        
        try {
            const response = await fetch(`${API_BASE_URL}/producers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                // Sauvegarder localement aussi
                this.saveProducerToLocalStorage(result);
            }
            
            return result;
        } catch (error) {
            // Mode hors ligne
            return this.createProducerOffline(data);
        }
    }

    async getProducers(professionalId) {
        try {
            const response = await fetch(`${API_BASE_URL}/producers/${professionalId}`);
            const result = await response.json();
            
            if (result.success) {
                // Synchroniser avec localStorage
                localStorage.setItem('professional_producers', JSON.stringify(result.producers));
            }
            
            return result;
        } catch (error) {
            // Mode hors ligne - utiliser localStorage
            const producers = JSON.parse(localStorage.getItem('professional_producers') || '[]');
            return { success: true, producers };
        }
    }

    // ========== SOUMISSIONS ==========

    async saveSubmission(userId, producerId, submissionData) {
        const data = {
            user_id: userId,
            producer_id: producerId,
            submission_data: submissionData
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/submissions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                // Sauvegarder localement aussi
                this.saveSubmissionToLocalStorage(producerId || userId, submissionData);
            }
            
            return result;
        } catch (error) {
            // Mode hors ligne
            return this.saveSubmissionOffline(data);
        }
    }

    async getSubmissions(userId = null, producerId = null) {
        try {
            const params = new URLSearchParams();
            if (userId) params.append('user_id', userId);
            if (producerId) params.append('producer_id', producerId);
            
            const response = await fetch(`${API_BASE_URL}/submissions?${params}`);
            return await response.json();
        } catch (error) {
            // Mode hors ligne
            return this.getSubmissionsOffline(producerId);
        }
    }

    // ========== CONSEILS ==========

    async saveAdvice(producerId, userId, adviceText, category, adviceType, source) {
        const data = {
            producer_id: producerId,
            user_id: userId,
            advice_text: adviceText,
            category,
            advice_type: adviceType,
            source
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/advice`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                // Sauvegarder localement aussi
                this.saveAdviceToLocalStorage(producerId, data);
            }
            
            return result;
        } catch (error) {
            return this.saveAdviceOffline(data);
        }
    }

    // ========== NOTIFICATIONS ==========

    async getNotifications(userId, unreadOnly = false) {
        try {
            const response = await fetch(
                `${API_BASE_URL}/notifications/${userId}?unread_only=${unreadOnly}`
            );
            return await response.json();
        } catch (error) {
            return { success: false, notifications: [] };
        }
    }

    async markNotificationRead(notificationId, userId) {
        try {
            const response = await fetch(
                `${API_BASE_URL}/notifications/${notificationId}/read`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId })
                }
            );
            return await response.json();
        } catch (error) {
            return { success: false };
        }
    }

    // ========== GAMIFICATION ==========

    async addPoints(userId, points, reason = '') {
        try {
            const response = await fetch(`${API_BASE_URL}/gamification/points`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, points, reason })
            });
            return await response.json();
        } catch (error) {
            return { success: false };
        }
    }

    async awardBadge(userId, badgeType, badgeName) {
        try {
            const response = await fetch(`${API_BASE_URL}/gamification/badges`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, badge_type: badgeType, badge_name: badgeName })
            });
            return await response.json();
        } catch (error) {
            return { success: false };
        }
    }

    async getBadges(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/gamification/badges/${userId}`);
            return await response.json();
        } catch (error) {
            return { success: false, badges: [] };
        }
    }

    async getLeaderboard(limit = 10) {
        try {
            const response = await fetch(`${API_BASE_URL}/gamification/leaderboard?limit=${limit}`);
            return await response.json();
        } catch (error) {
            return { success: false, leaderboard: [] };
        }
    }

    // ========== MESSAGERIE ==========

    async sendMessage(senderId, receiverId, subject, content) {
        try {
            const response = await fetch(`${API_BASE_URL}/messages`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sender_id: senderId, receiver_id: receiverId, subject, content })
            });
            return await response.json();
        } catch (error) {
            return this.sendMessageOffline(senderId, receiverId, subject, content);
        }
    }

    async getMessages(userId, folder = 'inbox') {
        try {
            const response = await fetch(`${API_BASE_URL}/messages/${userId}?folder=${folder}`);
            return await response.json();
        } catch (error) {
            return this.getMessagesOffline(userId, folder);
        }
    }

    // ========== LOCALISATION ==========

    async saveLocation(userId, producerId, latitude, longitude, address = null, region = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/locations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    producer_id: producerId,
                    latitude,
                    longitude,
                    address,
                    region
                })
            });
            return await response.json();
        } catch (error) {
            return this.saveLocationOffline(userId, producerId, latitude, longitude, address, region);
        }
    }

    async getLocations(userId = null, producerId = null) {
        try {
            const params = new URLSearchParams();
            if (userId) params.append('user_id', userId);
            if (producerId) params.append('producer_id', producerId);
            
            const response = await fetch(`${API_BASE_URL}/locations?${params}`);
            return await response.json();
        } catch (error) {
            return this.getLocationsOffline(userId, producerId);
        }
    }

    // ========== MÉTÉO ==========

    async getWeather(region) {
        try {
            const response = await fetch(`${API_BASE_URL}/weather/${region}`);
            const result = await response.json();
            
            if (result.success && result.data) {
                return result;
            }
            
            // Si pas en cache, utiliser API externe
            return await this.fetchWeatherFromAPI(region);
        } catch (error) {
            return this.getWeatherOffline(region);
        }
    }

    async fetchWeatherFromAPI(region) {
        // Utiliser OpenWeatherMap ou WeatherAPI
        const API_KEY = 'YOUR_API_KEY'; // À configurer
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${region},CI&appid=${API_KEY}&units=metric&lang=fr`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.cod === 200) {
                const weatherData = {
                    temperature: data.main.temp,
                    humidity: data.main.humidity,
                    precipitation: data.rain ? data.rain['1h'] || 0 : 0,
                    forecast: {
                        description: data.weather[0].description,
                        icon: data.weather[0].icon
                    }
                };
                
                // Mettre en cache
                await fetch(`${API_BASE_URL}/weather/cache`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        region,
                        latitude: data.coord.lat,
                        longitude: data.coord.lon,
                        ...weatherData
                    })
                });
                
                return { success: true, data: weatherData, source: 'external' };
            }
        } catch (error) {
            console.error('Erreur API météo:', error);
        }
        
        return { success: false, error: 'Données météo non disponibles' };
    }

    // ========== FONCTIONS OFFLINE ==========

    registerOffline(username, password, userType, email, phone, region) {
        // Sauvegarder dans localStorage pour synchronisation ultérieure
        const userData = {
            username,
            password, // ⚠️ En production, ne jamais stocker le mot de passe en clair
            user_type: userType,
            email,
            phone,
            region,
            synced: false,
            timestamp: new Date().toISOString()
        };
        
        const pending = JSON.parse(localStorage.getItem('pending_registrations') || '[]');
        pending.push(userData);
        localStorage.setItem('pending_registrations', JSON.stringify(pending));
        
        return { success: true, offline: true, message: 'Inscription enregistrée localement. Synchronisation à la connexion.' };
    }

    loginOffline(identifier, password) {
        // Vérifier dans localStorage
        const accounts = JSON.parse(localStorage.getItem('user_accounts') || '[]');
        const account = accounts.find(a => 
            a.username === identifier || a.email === identifier || a.phone === identifier
        );
        
        if (account && account.password === password) {
            localStorage.setItem('user_authenticated', 'true');
            localStorage.setItem('current_user_id', account.id);
            localStorage.setItem('user_type', account.user_type);
            return { success: true, user: account, offline: true };
        }
        
        return { success: false, error: 'Identifiants invalides' };
    }

    createProducerOffline(data) {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 7).toUpperCase();
        const code = `PROD-${timestamp}-${random}`;
        
        const producer = {
            ...data,
            id: `offline_${timestamp}`,
            code,
            synced: false,
            timestamp: new Date().toISOString()
        };
        
        const pending = JSON.parse(localStorage.getItem('pending_producers') || '[]');
        pending.push(producer);
        localStorage.setItem('pending_producers', JSON.stringify(pending));
        
        // Ajouter aussi à la liste locale
        const producers = JSON.parse(localStorage.getItem('professional_producers') || '[]');
        producers.push(producer);
        localStorage.setItem('professional_producers', JSON.stringify(producers));
        
        return { success: true, producer_id: producer.id, code, offline: true };
    }

    saveSubmissionOffline(data) {
        const submission = {
            ...data.submission_data,
            user_id: data.user_id,
            producer_id: data.producer_id,
            synced: false,
            timestamp: new Date().toISOString()
        };
        
        const pending = JSON.parse(localStorage.getItem('pending_submissions') || '[]');
        pending.push(submission);
        localStorage.setItem('pending_submissions', JSON.stringify(pending));
        
        // Sauvegarder aussi localement
        this.saveSubmissionToLocalStorage(data.producer_id || data.user_id, data.submission_data);
        
        return { success: true, offline: true };
    }

    saveSubmissionToLocalStorage(producerId, submissionData) {
        const allData = JSON.parse(localStorage.getItem('all_producer_submissions') || '{}');
        if (!allData[producerId]) {
            allData[producerId] = [];
        }
        allData[producerId].push({
            ...submissionData,
            date_soumission: new Date().toISOString()
        });
        localStorage.setItem('all_producer_submissions', JSON.stringify(allData));
    }

    saveAdviceToLocalStorage(producerId, adviceData) {
        const adviceTracking = JSON.parse(localStorage.getItem('advice_tracking') || '{}');
        if (!adviceTracking[producerId]) {
            adviceTracking[producerId] = [];
        }
        adviceTracking[producerId].push({
            text: adviceData.advice_text,
            category: adviceData.category,
            type: adviceData.advice_type,
            source: adviceData.source,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('advice_tracking', JSON.stringify(adviceTracking));
    }

    getSubmissionsOffline(producerId) {
        const allData = JSON.parse(localStorage.getItem('all_producer_submissions') || '{}');
        const submissions = allData[producerId] || [];
        return { success: true, submissions };
    }

    saveAdviceOffline(data) {
        this.saveAdviceToLocalStorage(data.producer_id, data);
        return { success: true, offline: true };
    }

    sendMessageOffline(senderId, receiverId, subject, content) {
        const message = {
            sender_id: senderId,
            receiver_id: receiverId,
            subject,
            content,
            synced: false,
            timestamp: new Date().toISOString()
        };
        
        const pending = JSON.parse(localStorage.getItem('pending_messages') || '[]');
        pending.push(message);
        localStorage.setItem('pending_messages', JSON.stringify(pending));
        
        // Sauvegarder aussi localement
        const messages = JSON.parse(localStorage.getItem('messages') || '[]');
        messages.push(message);
        localStorage.setItem('messages', JSON.stringify(messages));
        
        return { success: true, offline: true };
    }

    getMessagesOffline(userId, folder) {
        const messages = JSON.parse(localStorage.getItem('messages') || '[]');
        const filtered = folder === 'inbox' 
            ? messages.filter(m => m.receiver_id === userId)
            : messages.filter(m => m.sender_id === userId);
        
        return { success: true, messages: filtered, unread_count: 0 };
    }

    saveLocationOffline(userId, producerId, latitude, longitude, address, region) {
        const location = {
            user_id: userId,
            producer_id: producerId,
            latitude,
            longitude,
            address,
            region,
            synced: false,
            timestamp: new Date().toISOString()
        };
        
        const pending = JSON.parse(localStorage.getItem('pending_locations') || '[]');
        pending.push(location);
        localStorage.setItem('pending_locations', JSON.stringify(pending));
        
        return { success: true, offline: true };
    }

    getLocationsOffline(userId, producerId) {
        const locations = JSON.parse(localStorage.getItem('locations') || '[]');
        const filtered = producerId
            ? locations.filter(l => l.producer_id === producerId)
            : locations.filter(l => l.user_id === userId);
        
        return { success: true, locations: filtered };
    }

    getWeatherOffline(region) {
        const cached = JSON.parse(localStorage.getItem(`weather_${region}`) || 'null');
        if (cached && new Date(cached.expires_at) > new Date()) {
            return { success: true, data: cached.data, source: 'cache' };
        }
        
        return { success: false, error: 'Données météo non disponibles hors ligne' };
    }

    // ========== SYNCHRONISATION ==========

    async syncPendingData() {
        if (!this.isOnline) return;
        
        // Synchroniser les inscriptions
        const pendingRegistrations = JSON.parse(localStorage.getItem('pending_registrations') || '[]');
        for (const reg of pendingRegistrations) {
            try {
                await this.register(reg.username, reg.password, reg.user_type, reg.email, reg.phone, reg.region);
                // Supprimer après succès
            } catch (error) {
                console.error('Erreur sync registration:', error);
            }
        }
        
        // Synchroniser les producteurs
        const pendingProducers = JSON.parse(localStorage.getItem('pending_producers') || '[]');
        for (const producer of pendingProducers) {
            try {
                await this.createProducer(
                    producer.professional_id,
                    producer.name,
                    producer.region,
                    producer.phone,
                    producer.email,
                    producer.notes
                );
            } catch (error) {
                console.error('Erreur sync producer:', error);
            }
        }
        
        // Synchroniser les soumissions
        const pendingSubmissions = JSON.parse(localStorage.getItem('pending_submissions') || '[]');
        for (const sub of pendingSubmissions) {
            try {
                await this.saveSubmission(sub.user_id, sub.producer_id, sub);
            } catch (error) {
                console.error('Erreur sync submission:', error);
            }
        }
        
        // Nettoyer après synchronisation
        localStorage.removeItem('pending_registrations');
        localStorage.removeItem('pending_producers');
        localStorage.removeItem('pending_submissions');
    }

    // ========== UTILITAIRES ==========

    saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('Erreur sauvegarde localStorage:', error);
        }
    }

    showNotification(message, type = 'info') {
        // Utiliser le système de notification existant
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
}

// Instance globale
const dbSync = new DatabaseSync();

// Exporter pour utilisation globale
window.dbSync = dbSync;

