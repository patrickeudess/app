/**
 * Intégration API météo pour Mon Cacao
 */
class WeatherService {
    constructor() {
        this.apiKey = 'YOUR_OPENWEATHER_API_KEY'; // À configurer
        this.baseUrl = 'https://api.openweathermap.org/data/2.5';
        this.cache = new Map();
        this.cacheDuration = 3600000; // 1 heure
    }

    async getWeatherByRegion(region) {
        // Vérifier le cache
        const cached = this.getCachedWeather(region);
        if (cached) {
            return cached;
        }

        // Coordonnées approximatives des régions de Côte d'Ivoire
        const regionCoordinates = {
            'Abidjan': { lat: 5.3600, lon: -4.0083 },
            'Yamoussoukro': { lat: 6.8276, lon: -5.2893 },
            'Bouaké': { lat: 7.6944, lon: -5.0303 },
            'San-Pédro': { lat: 4.7485, lon: -6.6363 },
            'Daloa': { lat: 6.8774, lon: -6.4502 },
            'Korhogo': { lat: 9.4581, lon: -5.6296 },
            'Man': { lat: 7.4125, lon: -7.5533 },
            'Gagnoa': { lat: 6.1287, lon: -5.9506 },
            'Abengourou': { lat: 6.7297, lon: -3.4964 },
            'Divo': { lat: 5.8433, lon: -5.3617 },
            'Indenie-Djuablin': { lat: 6.7297, lon: -3.4964 }
        };

        const coords = regionCoordinates[region] || regionCoordinates['Abidjan'];

        try {
            // Essayer d'abord l'API backend
            const response = await fetch(`http://localhost:5000/api/weather/${region}`);
            const result = await response.json();

            if (result.success && result.data) {
                this.cacheWeather(region, result.data);
                return result;
            }

            // Sinon, utiliser OpenWeatherMap directement
            return await this.fetchFromOpenWeather(coords.lat, coords.lon, region);
        } catch (error) {
            console.error('Erreur météo:', error);
            return this.getWeatherOffline(region);
        }
    }

    async fetchFromOpenWeather(lat, lon, region) {
        if (!this.apiKey || this.apiKey === 'YOUR_OPENWEATHER_API_KEY') {
            // Mode simulation si pas d'API key
            return this.getSimulatedWeather(region);
        }

        const url = `${this.baseUrl}/weather?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric&lang=fr`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.cod === 200) {
                const weatherData = {
                    temperature: Math.round(data.main.temp),
                    humidity: data.main.humidity,
                    precipitation: data.rain ? data.rain['1h'] || 0 : 0,
                    windSpeed: data.wind ? data.wind.speed : 0,
                    description: data.weather[0].description,
                    icon: data.weather[0].icon,
                    forecast: {
                        min: Math.round(data.main.temp_min),
                        max: Math.round(data.main.temp_max),
                        feelsLike: Math.round(data.main.feels_like)
                    }
                };

                // Mettre en cache
                this.cacheWeather(region, weatherData);

                // Sauvegarder dans le backend
                await fetch('http://localhost:5000/api/weather/cache', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        region,
                        latitude: lat,
                        longitude: lon,
                        ...weatherData
                    })
                }).catch(() => {}); // Ignorer les erreurs

                return { success: true, data: weatherData, source: 'openweather' };
            }
        } catch (error) {
            console.error('Erreur OpenWeatherMap:', error);
        }

        return this.getSimulatedWeather(region);
    }

    getSimulatedWeather(region) {
        // Données météo simulées basées sur la région
        const baseTemp = 28; // Température de base en Côte d'Ivoire
        const variation = Math.random() * 4 - 2; // Variation de ±2°C
        
        const weatherData = {
            temperature: Math.round(baseTemp + variation),
            humidity: Math.round(70 + Math.random() * 20),
            precipitation: Math.random() * 5,
            windSpeed: Math.random() * 3,
            description: 'Partiellement nuageux',
            icon: '02d',
            forecast: {
                min: Math.round(baseTemp - 2),
                max: Math.round(baseTemp + 3),
                feelsLike: Math.round(baseTemp + variation)
            }
        };

        this.cacheWeather(region, weatherData);
        return { success: true, data: weatherData, source: 'simulation' };
    }

    async getForecast(lat, lon) {
        if (!this.apiKey || this.apiKey === 'YOUR_OPENWEATHER_API_KEY') {
            return { success: false, error: 'API key non configurée' };
        }

        const url = `${this.baseUrl}/forecast?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric&lang=fr`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.cod === '200') {
                return {
                    success: true,
                    forecast: data.list.slice(0, 5).map(item => ({
                        date: new Date(item.dt * 1000),
                        temperature: Math.round(item.main.temp),
                        description: item.weather[0].description,
                        icon: item.weather[0].icon,
                        precipitation: item.rain ? item.rain['3h'] || 0 : 0
                    }))
                };
            }
        } catch (error) {
            console.error('Erreur prévisions:', error);
        }

        return { success: false, error: 'Prévisions non disponibles' };
    }

    cacheWeather(region, data) {
        this.cache.set(region, {
            data,
            timestamp: Date.now()
        });
    }

    getCachedWeather(region) {
        const cached = this.cache.get(region);
        if (cached && (Date.now() - cached.timestamp) < this.cacheDuration) {
            return { success: true, data: cached.data, source: 'cache' };
        }
        return null;
    }

    getWeatherOffline(region) {
        // Vérifier localStorage
        const cached = localStorage.getItem(`weather_${region}`);
        if (cached) {
            const data = JSON.parse(cached);
            if (new Date(data.expires_at) > new Date()) {
                return { success: true, data: data.data, source: 'localStorage' };
            }
        }

        return this.getSimulatedWeather(region);
    }

    getWeatherRecommendations(weatherData) {
        const recommendations = [];

        if (weatherData.precipitation > 10) {
            recommendations.push('🌧️ Pluie prévue - Protégez vos récoltes');
        }

        if (weatherData.temperature > 32) {
            recommendations.push('☀️ Température élevée - Assurez-vous de l\'irrigation suffisante');
        }

        if (weatherData.humidity < 50) {
            recommendations.push('💧 Humidité faible - Surveillez l\'arrosage');
        }

        if (weatherData.precipitation === 0 && weatherData.temperature > 30) {
            recommendations.push('🌡️ Conditions sèches - Planifiez l\'irrigation');
        }

        return recommendations;
    }
}

// Instance globale
const weatherService = new WeatherService();
window.weatherService = weatherService;

