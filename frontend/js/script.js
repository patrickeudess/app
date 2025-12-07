// Navigation mobile
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
});

// Fermer le menu mobile quand on clique sur un lien
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// Navigation smooth scroll
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Animation au scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observer les éléments à animer
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.prediction-form, .result-card, .chart-card, .stat-card, .about-card');
    animatedElements.forEach(el => observer.observe(el));
});

// Fonction de prédiction avec les mêmes paramètres que Streamlit
async function predictProductivity() {
    // Récupérer les valeurs des champs - Mêmes paramètres que Streamlit
    const age_verger = parseFloat(document.getElementById('age_verger').value) || 0;
    const agroforest = document.getElementById('agroforest').value;
    const engrais = document.getElementById('engrais').value;
    const fumier = document.getElementById('fumier').value;
    const maladie = document.getElementById('maladie').value;
    const herbicide = document.getElementById('herbicide').value;
    const insecticide = document.getElementById('insecticide').value;
    const fongicide = document.getElementById('fongicide').value;
    const cout_prod = parseFloat(document.getElementById('cout_prod').value) || 0;
    // Le prix est saisi en FCFA/kg, mais l'API attend FCFA/tonne, donc on multiplie par 1000
    const prix_a_kg = parseFloat(document.getElementById('prix_a').value) || 1000; // FCFA/kg
    const prix_a = prix_a_kg * 1000; // Conversion en FCFA/tonne pour l'API
    const region = document.getElementById('region').value;
    const pluviometrie = document.getElementById('pluviometrie').value;
    const sexe = document.getElementById('sexe').value;
    const competences = document.getElementById('competences').value;

    // Validation des données
    if (!age_verger || !cout_prod) {
        showNotification('Veuillez remplir au minimum l\'âge du verger et le coût de production', 'warning');
        return;
    }
    
    // Utiliser des valeurs par défaut si certains champs sont vides
    const finalAgeVerger = age_verger || 15;
    const finalCoutProd = cout_prod || 450000;

    // Afficher un indicateur de chargement
    showNotification('Calcul en cours avec le modèle XGBoost...', 'info');
    
    try {
        // Appel à l'API avec les mêmes paramètres que Streamlit
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                age_verger: age_verger,
                agroforest: agroforest,
                engrais: engrais,
                fumier: fumier,
                maladie: maladie,
                herbicide: herbicide,
                insecticide: insecticide,
                fongicide: fongicide,
                cout_prod: cout_prod,
                prix_a: prix_a,
                region: region,
                pluviometrie: pluviometrie,
                sexe: sexe,
                competences: competences
            })
        });

        const result = await response.json();
        
        if (result.success) {
            // Afficher le résultat
            displayPredictionResult(result.prediction);
            
            // Mettre à jour les détails des calculs (qui mettra aussi à jour les cartes)
            updateCalculationDetails(result.prediction);
            
            // Mettre à jour l'analyse et recommandations
            updateAnalysisAndRecommendations(result.prediction);
            
            // Créer les graphiques
            createComparisonChart(result.prediction);
            createFinancialChart(result.prediction);
            
            // Mettre à jour les suggestions d'optimisation
            updateOptimizationSuggestions(result.prediction);
            
            showNotification('Prédiction XGBoost calculée avec succès !', 'success');
        } else {
            showNotification('Erreur lors de la prédiction: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Erreur API:', error);
        showNotification('Erreur de connexion à l\'API. Vérifiez que le serveur API est démarré.', 'error');
        
        // Fallback vers la simulation si l'API n'est pas disponible
        showNotification('Utilisation de la simulation en mode dégradé...', 'warning');
        const productivity = simulatePrediction(finalAgeVerger, finalCoutProd, region);
        const predictionResult = {
            productivity_t_ha: productivity.value / 1000, // Conversion kg/ha vers t/ha
            confidence: productivity.confidence,
            recommendation: productivity.recommendation,
            revenue_fcfa: productivity.revenue,
            benefit_fcfa: productivity.benefit
        };
        
        // Afficher le résultat avec les nouvelles fonctions
        displayPredictionResult(predictionResult);
        updateCalculationDetails(predictionResult);
        updateAnalysisAndRecommendations(predictionResult);
        createComparisonChart(predictionResult);
        createFinancialChart(predictionResult);
        updateOptimizationSuggestions(predictionResult);
    }
}

// Simulation de prédiction (fallback si l'API n'est pas disponible)
function simulatePrediction(age_verger, cout_prod, region) {
    // Algorithme simplifié pour la démonstration
    let baseProductivity = 1000; // kg/ha de base
    
    // Facteurs d'influence basés sur les paramètres Streamlit
    const ageFactor = age_verger >= 5 && age_verger <= 20 ? 1.2 : 0.8;
    const regionFactor = region === "Indenie-Djuablin" ? 1.1 : 1.0;
    const costFactor = cout_prod >= 400000 && cout_prod <= 500000 ? 1.1 : 0.9;
    
    // Calcul de la productivité
    const productivity = Math.round(baseProductivity * ageFactor * regionFactor * costFactor);
    
    // Calcul de la confiance
    const confidence = Math.round(85 + Math.random() * 10);
    
    // Calculs financiers
    const prix_kg = parseFloat(document.getElementById('prix_a').value) || 1000; // FCFA/kg
    const revenue = productivity * prix_kg;
    const benefit = revenue - cout_prod;
    
    // Recommandation
    let recommendation = 'Optimale';
    if (productivity < 800) recommendation = 'Amélioration nécessaire';
    else if (productivity < 1000) recommendation = 'Bonne';
    else if (productivity > 1200) recommendation = 'Excellente';
    
    return {
        value: productivity,
        confidence: confidence,
        recommendation: recommendation,
        revenue: revenue,
        benefit: benefit
    };
}

// Fonction pour formater les nombres
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

// Afficher le résultat de prédiction
function displayPredictionResult(prediction) {
    const resultCard = document.getElementById('prediction-result');
    if (resultCard) {
        resultCard.style.display = 'block';
        
        // Animation d'apparition
        resultCard.style.opacity = '0';
        resultCard.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            resultCard.style.transition = 'all 0.5s ease';
            resultCard.style.opacity = '1';
            resultCard.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Animation du compteur
function animateCounter(elementId, targetValue, suffix = '') {
    const element = document.getElementById(elementId);
    const startValue = 0;
    const duration = 2000;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = startValue + (targetValue - startValue) * progress;
        
        if (typeof targetValue === 'number') {
            element.textContent = currentValue.toFixed(3) + suffix;
        } else {
            element.textContent = targetValue;
        }
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Mettre à jour le compteur circulaire
function updateMeter(value) {
    const meter = document.getElementById('productivity-meter');
    const maxValue = 2000; // Valeur maximale pour 100%
    const percentage = Math.min((value / maxValue) * 100, 100);
    const circumference = 339.292; // 2 * π * r (r = 54)
    const offset = circumference - (percentage / 100) * circumference;
    
    meter.style.strokeDashoffset = offset;
}

// Contrôles des graphiques
document.querySelectorAll('.btn-chart').forEach(btn => {
    btn.addEventListener('click', () => {
        // Retirer la classe active de tous les boutons
        document.querySelectorAll('.btn-chart').forEach(b => b.classList.remove('active'));
        // Ajouter la classe active au bouton cliqué
        btn.classList.add('active');
        
        // Mettre à jour le graphique (à implémenter avec Chart.js)
        updateChart(btn.dataset.period);
    });
});

// Mettre à jour le graphique
function updateChart(period) {
    // Simulation de mise à jour de graphique
    console.log(`Mise à jour du graphique pour la période: ${period}`);
    
    // Ici vous pouvez intégrer Chart.js pour afficher les vraies données
    // Exemple avec Chart.js:
    /*
    if (window.productivityChart) {
        window.productivityChart.destroy();
    }
    
    const ctx = document.getElementById('productivity-chart').getContext('2d');
    window.productivityChart = new Chart(ctx, {
        type: 'line',
        data: getChartData(period),
        options: getChartOptions()
    });
    */
}

// Notifications
function showNotification(message, type = 'info') {
    // Créer l'élément de notification
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
    
    // Styles pour la notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 1rem;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    // Ajouter au DOM
    document.body.appendChild(notification);
    
    // Supprimer automatiquement après 5 secondes
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
        success: 'var(--success-color)',
        warning: 'var(--warning-color)',
        error: 'var(--danger-color)',
        info: 'var(--primary-color)'
    };
    return colors[type] || 'var(--primary-color)';
}

// Animation CSS pour les notifications
const style = document.createElement('style');
style.textContent = `
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
document.head.appendChild(style);

// Validation des formulaires
document.querySelectorAll('.form-group input, .form-group select').forEach(input => {
    input.addEventListener('blur', validateField);
    input.addEventListener('input', clearFieldError);
});

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    // Supprimer les erreurs précédentes
    clearFieldError(event);
    
    // Validation selon le type de champ
    let isValid = true;
    let errorMessage = '';
    
    switch (field.id) {
        case 'age_verger':
            if (value && (value < 0 || value > 50)) {
                isValid = false;
                errorMessage = 'L\'âge du verger doit être entre 0 et 50 ans';
            }
            break;
        case 'cout_prod':
            if (value && value < 0) {
                isValid = false;
                errorMessage = 'Le coût de production ne peut pas être négatif';
            }
            break;
        case 'prix_a':
            if (value && value < 0) {
                isValid = false;
                errorMessage = 'Le prix d\'achat ne peut pas être négatif';
            }
            break;
    }
    
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
}

function showFieldError(field, message) {
    field.style.borderColor = 'var(--danger-color)';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: var(--danger-color);
        font-size: 0.8rem;
        margin-top: 0.25rem;
        animation: fadeIn 0.3s ease;
    `;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(event) {
    const field = event.target;
    field.style.borderColor = '#e9ecef';
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Animation CSS pour les erreurs de champ
const errorStyle = document.createElement('style');
errorStyle.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(errorStyle);

// Initialisation des graphiques (à implémenter avec Chart.js)
function initializeCharts() {
    // Exemple d'initialisation de graphique avec Chart.js
    /*
    const ctx1 = document.getElementById('productivity-chart').getContext('2d');
    const ctx2 = document.getElementById('factors-chart').getContext('2d');
    
    // Graphique de productivité
    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Productivité (t/ha)',
                data: [1.2, 1.35, 1.1, 1.4, 1.3, 1.5],
                borderColor: 'var(--primary-color)',
                backgroundColor: 'rgba(46, 139, 87, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Graphique des facteurs
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Âge du verger', 'Région', 'Engrais', 'Coût de production', 'Pluviométrie'],
            datasets: [{
                data: [25, 20, 15, 20, 20],
                backgroundColor: [
                    '#2E8B57',
                    '#1a472a',
                    '#FFD700',
                    '#28a745',
                    '#ffc107'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    */
}

// Fonctions pour ouvrir les modals des fonctionnalités
function openPrediction() {
    document.getElementById('prediction-modal').style.display = 'block';
}

function openDashboard() {
    window.location.href = 'dashboard.html';
}

function openAnalytics() {
    // Rediriger vers la page analytics ou ouvrir un modal
    showNotification('Fonctionnalité Analytics en cours de développement', 'info');
}

function openData() {
    showNotification('Gestion des données agronomiques en cours de développement', 'info');
}

function openAIAssistant() {
    showNotification('Assistant IA en cours de développement', 'info');
}

function openRevenue() {
    window.location.href = 'revenus.html';
}

function openTips() {
    showNotification('Conseils et astuces en cours de développement', 'info');
}

function openSecurity() {
    showNotification('Paramètres de sécurité en cours de développement', 'info');
}

function openBadges() {
    showNotification('Système de badges en cours de développement', 'info');
}

// Fonction pour fermer les modals
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Fermer les modals en cliquant à l'extérieur
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Fonctions pour les nouvelles fonctionnalités



// Fonction pour sauvegarder les données de plantation
function savePlantationData() {
    const name = document.getElementById('plantation_name').value;
    const size = document.getElementById('plantation_size').value;
    const trees = document.getElementById('tree_count').value;
    const date = document.getElementById('planting_date').value;
    const soil = document.getElementById('soil_type').value;
    
    if (!name || !size || !trees) {
        showNotification('Veuillez remplir les champs obligatoires', 'warning');
        return;
    }
    
    // Récupérer les plantations existantes
    const plantations = JSON.parse(localStorage.getItem('plantations')) || [];
    
    // Ajouter la nouvelle plantation
    const newPlantation = {
        id: Date.now(),
        name: name,
        size: parseFloat(size),
        trees: parseInt(trees),
        date: date,
        soil: soil,
        createdAt: new Date().toISOString()
    };
    
    plantations.push(newPlantation);
    localStorage.setItem('plantations', JSON.stringify(plantations));
    
    // Mettre à jour le résumé
    updatePlantationSummary();
    
    showNotification('Plantation enregistrée avec succès !', 'success');
    
    // Vider le formulaire
    document.getElementById('plantation_name').value = '';
    document.getElementById('plantation_size').value = '';
    document.getElementById('tree_count').value = '';
    document.getElementById('planting_date').value = '';
    document.getElementById('soil_type').value = 'Argileux';
}

// Fonction pour mettre à jour le résumé des plantations
function updatePlantationSummary() {
    const plantations = JSON.parse(localStorage.getItem('plantations')) || [];
    
    const totalPlantations = plantations.length;
    const totalSurface = plantations.reduce((sum, p) => sum + p.size, 0);
    const totalTrees = plantations.reduce((sum, p) => sum + p.trees, 0);
    
    document.getElementById('total-plantations').textContent = totalPlantations;
    document.getElementById('total-surface').textContent = totalSurface.toFixed(1) + ' hectares';
    document.getElementById('total-trees-data').textContent = totalTrees.toLocaleString();
}

// Fonction pour gérer l'Assistant IA
function sendMessage() {
    const input = document.getElementById('user-message');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Ajouter le message de l'utilisateur
    addMessage(message, 'user');
    input.value = '';
    
    // Simuler une réponse de l'IA
    setTimeout(() => {
        const response = generateAIResponse(message);
        addMessage(response, 'ai');
    }, 1000);
}

// Fonction pour ajouter un message dans le chat
function addMessage(text, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'ai' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = `<p>${text}</p>`;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    
    // Scroll vers le bas
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Fonction pour gérer l'appui sur Entrée dans le chat
function handleChatEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Fonction pour poser une question rapide
function askQuestion(question) {
    addMessage(question, 'user');
    
    setTimeout(() => {
        const response = generateAIResponse(question);
        addMessage(response, 'ai');
    }, 1000);
}

// Fonction pour générer une réponse IA simple
function generateAIResponse(question) {
    const responses = {
        'arrosage': 'Pour bien arroser tes cacaoyers :\n• Arrose le matin ou le soir\n• Donne de l\'eau 2-3 fois par semaine en saison sèche\n• Évite de trop arroser pour ne pas pourrir les racines\n• Utilise un arrosoir ou un système d\'irrigation simple',
        'récolte': 'Pour récolter au bon moment :\n• Les cabosses sont mûres quand elles sont jaunes ou oranges\n• Récolte tous les 15-20 jours pendant la saison\n• Coupe les cabosses avec un couteau propre\n• Évite de blesser l\'arbre',
        'maladies': 'Pour lutter contre les maladies :\n• Surveille régulièrement tes arbres\n• Enlève les feuilles malades\n• Utilise des produits naturels si possible\n• Demande conseil à un expert si nécessaire',
        'engrais': 'Pour bien nourrir tes cacaoyers :\n• Utilise du fumier de vache ou de poule\n• Ajoute des feuilles mortes au pied des arbres\n• Évite trop d\'engrais chimiques\n• Donne de l\'engrais 2-3 fois par an'
    };
    
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('arroser') || lowerQuestion.includes('eau')) {
        return responses.arrosage;
    } else if (lowerQuestion.includes('récolter') || lowerQuestion.includes('récolte')) {
        return responses.récolte;
    } else if (lowerQuestion.includes('maladie') || lowerQuestion.includes('maladies')) {
        return responses.maladies;
    } else if (lowerQuestion.includes('engrais') || lowerQuestion.includes('nourrir')) {
        return responses.engrais;
    } else {
        return 'Je peux t\'aider avec l\'arrosage, la récolte, les maladies et les engrais. Pose-moi une question plus précise !';
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Initialiser les graphiques
    initializeCharts();
    
    // Charger les données du profil
    const profileData = JSON.parse(localStorage.getItem('userProfile'));
    if (profileData) {
        updateProfileDisplay(profileData);
    }
    
    // Mettre à jour le résumé des plantations
    updatePlantationSummary();
    
    // Ajouter la classe active au lien de navigation actuel
    const currentSection = window.location.hash || '#home';
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentSection) {
            link.classList.add('active');
        }
    });
    
    // Observer le scroll pour mettre à jour la navigation active
    window.addEventListener('scroll', updateActiveNavigation);
    
    // Animation des cartes au chargement
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
});

// Nouvelles fonctions pour la prédiction améliorée

// Mettre à jour les cartes d'estimation
function updateEstimationCards(prediction) {
    const production = prediction.productivity_t_ha;
    const revenue = prediction.revenue_fcfa;
    const benefit = prediction.benefit_fcfa;
    
    if (document.getElementById('production-estimated')) {
        document.getElementById('production-estimated').textContent = production.toFixed(3);
    }
    if (document.getElementById('revenue-potential')) {
        document.getElementById('revenue-potential').textContent = formatNumber(revenue);
    }
    if (document.getElementById('benefit-estimated')) {
        document.getElementById('benefit-estimated').textContent = formatNumber(benefit);
    }
}

// Mettre à jour les détails des calculs
function updateCalculationDetails(prediction) {
    const production = prediction.productivity_t_ha;
    const productionKg = production * 1000;
    
    // Récupérer les vraies valeurs saisies par l'utilisateur
    const price = parseFloat(document.getElementById('prix_a').value) || 1000; // FCFA/kg
    const cost = parseFloat(document.getElementById('cout_prod').value) || 450000; // FCFA/ha
    
    const revenue = productionKg * price;
    const benefit = revenue - cost;
    
    const detailsHtml = `
        <ul>
            <li><strong>Prix de vente du cacao (FCFA/Kg) :</strong> ${formatNumber(price)} FCFA/kg</li>
            <li><strong>Production :</strong> ${production.toFixed(3)} t/ha = ${productionKg.toFixed(0)} kg/ha</li>
            <li><strong>Revenu = Production × Prix =</strong> ${productionKg.toFixed(0)} × ${formatNumber(price)} = ${formatNumber(revenue)} FCFA/ha</li>
            <li><strong>Coût de production :</strong> ${formatNumber(cost)} FCFA/ha</li>
            <li><strong>Bénéfice = Revenu – Coût =</strong> ${formatNumber(revenue)} – ${formatNumber(cost)} = ${formatNumber(benefit)} FCFA/ha</li>
        </ul>
    `;
    
    document.getElementById('calculation-details').innerHTML = detailsHtml;
    
    // Mettre à jour les cartes d'estimation avec les mêmes valeurs calculées
    updateEstimationCards({
        productivity_t_ha: production,
        revenue_fcfa: revenue,
        benefit_fcfa: benefit
    });
}

// Mettre à jour l'analyse et recommandations
function updateAnalysisAndRecommendations(prediction) {
    const production = prediction.productivity_t_ha;
    const regionalAverage = 0.850;
    const cost = parseFloat(document.getElementById('cout_prod').value) || 450000;
    const regionalCost = 450000;
    
    // Mettre à jour l'analyse de productivité
    document.getElementById('user-production').textContent = production.toFixed(3);
    
    // Générer les recommandations
    const recommendations = [];
    
    if (production < regionalAverage) {
        recommendations.push({
            text: "Si la production est inférieure à la moyenne, envisagez d'optimiser l'utilisation des engrais et de vérifier l'état sanitaire des plants.",
            category: 'Productivité',
            type: 'Optimisation engrais'
        });
    }
    
    if (cost > regionalCost) {
        recommendations.push({
            text: "Si le coût de production est élevé, analysez la répartition des coûts et optimisez l'utilisation des intrants.",
            category: 'Coûts',
            type: 'Optimisation coûts'
        });
    }
    
    recommendations.push({
        text: "Pour améliorer le bénéfice, cherchez des circuits de vente plus avantageux et réduisez les coûts non essentiels.",
        category: 'Revenus',
        type: 'Optimisation bénéfices'
    });
    
    // Afficher les recommandations
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = recommendations.map(rec => `<li>${rec.text}</li>`).join('');
    
    // Enregistrer les conseils consultés
    trackAdviceGiven(recommendations, 'prediction');
}

// Créer le graphique comparatif
function createComparisonChart(prediction) {
    const ctx = document.getElementById('comparison-chart').getContext('2d');
    
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
    }
    
    const production = prediction.productivity_t_ha;
    const cost = (parseFloat(document.getElementById('cout_prod').value) || 450000) / 10000; // Divisé par 10000 pour l'affichage
    const regionalProduction = 0.850;
    const regionalCost = 450000 / 10000;
    
    window.comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Production (t/ha)', 'Coût (FCFA/ha/10000)'],
            datasets: [
                {
                    label: 'Votre exploitation',
                    data: [production, cost],
                    backgroundColor: '#2E8B57',
                    borderColor: '#2E8B57',
                    borderWidth: 1
                },
                {
                    label: 'Moyenne Indenie-Djuablin',
                    data: [regionalProduction, regionalCost],
                    backgroundColor: '#90EE90',
                    borderColor: '#90EE90',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#000000',
                        font: {
                            weight: 'bold',
                            size: 11
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    },
                    ticks: {
                        color: '#000000',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#000000',
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#000000',
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}

// Créer le graphique de répartition financière
function createFinancialChart(prediction) {
    const ctx = document.getElementById('financial-chart').getContext('2d');
    
    if (window.financialChart) {
        window.financialChart.destroy();
    }
    
    const revenue = prediction.revenue_fcfa;
    const cost = parseFloat(document.getElementById('cout_prod').value) || 450000;
    const benefit = revenue - cost;
    
    const benefitPercentage = ((benefit / revenue) * 100).toFixed(1);
    const costPercentage = ((cost / revenue) * 100).toFixed(2);
    
    window.financialChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bénéfice', 'Coût de production'],
            datasets: [{
                data: [benefit, cost],
                backgroundColor: ['#90EE90', '#2E8B57'],
                borderColor: ['#90EE90', '#2E8B57'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#000000',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const percentage = context.parsed === benefit ? benefitPercentage : costPercentage;
                            return `${label}: ${formatNumber(value)} FCFA (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Mettre à jour les suggestions d'optimisation
// Fonction pour enregistrer les conseils donnés
function trackAdviceGiven(advices, source) {
    const currentProducerId = localStorage.getItem('current_producer_id');
    if (!currentProducerId) return; // Pas de producteur associé
    
    const adviceLog = JSON.parse(localStorage.getItem('advice_tracking') || '{}');
    if (!adviceLog[currentProducerId]) {
        adviceLog[currentProducerId] = [];
    }
    
    const timestamp = new Date().toISOString();
    advices.forEach(advice => {
        adviceLog[currentProducerId].push({
            text: advice.text || advice,
            category: advice.category || 'Général',
            type: advice.type || 'Autre',
            source: source, // 'prediction', 'conseils', 'assistant', 'score-ecologique'
            timestamp: timestamp
        });
    });
    
    localStorage.setItem('advice_tracking', JSON.stringify(adviceLog));
}

function updateOptimizationSuggestions(prediction) {
    const production = prediction.productivity_t_ha;
    const regionalAverage = 0.850;
    
    const suggestions = [
        "Envisagez l'utilisation d'engrais adaptés",
        "Vérifiez l'état sanitaire des plants",
        "Optimisez la densité de plantation"
    ];
    
    if (production < regionalAverage) {
        suggestions.push("Améliorez les pratiques culturales pour atteindre la moyenne régionale");
    }
    
    const optimizationList = document.getElementById('optimization-list');
    optimizationList.innerHTML = suggestions.map(suggestion => `<li>${suggestion}</li>`).join('');
}

// Fonctions pour le modal de données amélioré

// Changer d'onglet
function switchTab(tabName) {
    // Masquer tous les onglets
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    // Désactiver tous les boutons d'onglet
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Activer l'onglet sélectionné
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Activer le bouton correspondant
    event.target.classList.add('active');
}

// Incrémenter une valeur
function incrementValue(inputId) {
    const input = document.getElementById(inputId);
    const currentValue = parseFloat(input.value) || 0;
    const step = parseFloat(input.step) || 0.1;
    input.value = (currentValue + step).toFixed(1);
}

// Décrémenter une valeur
function decrementValue(inputId) {
    const input = document.getElementById(inputId);
    const currentValue = parseFloat(input.value) || 0;
    const step = parseFloat(input.step) || 0.1;
    const newValue = Math.max(0, currentValue - step);
    input.value = newValue.toFixed(1);
}

// Calculer le revenu total automatiquement
function calculateRevenue() {
    const production = parseFloat(document.getElementById('production_reelle_data').value) || 0;
    const prix = parseFloat(document.getElementById('prix_vente_data').value) || 0;
    const revenu = production * prix;
    document.getElementById('revenu_total_data').value = revenu.toFixed(0);
}

// Soumettre les données annuelles
function submitAnnualData() {
    // Récupérer toutes les données
    const data = {
        // Données agronomiques
        age_verger: parseFloat(document.getElementById('age_verger_data').value) || 0,
        agroforest: document.getElementById('agroforest_data').value,
        engrais: document.getElementById('engrais_data').value,
        fumier: document.getElementById('fumier_data').value,
        maladie: document.getElementById('maladie_data').value,
        herbicide: document.getElementById('herbicide_data').value,
        insecticide: document.getElementById('insecticide_data').value,
        fongicide: document.getElementById('fongicide_data').value,
        
        // Données économiques
        cout_prod: parseFloat(document.getElementById('cout_prod_data').value) || 0,
        prix_vente: parseFloat(document.getElementById('prix_vente_data').value) || 0,
        production_reelle: parseFloat(document.getElementById('production_reelle_data').value) || 0,
        revenu_total: parseFloat(document.getElementById('revenu_total_data').value) || 0,
        
        // Données géographiques
        region: document.getElementById('region_data').value,
        pluviometrie: document.getElementById('pluviometrie_data').value,
        temperature: parseFloat(document.getElementById('temperature_data').value) || 0,
        humidite: parseFloat(document.getElementById('humidite_data').value) || 0,
        
        // Métadonnées
        date_soumission: new Date().toISOString(),
        type: 'donnees_annuelles'
    };
    
    // Validation
    if (!data.age_verger || !data.cout_prod || !data.production_reelle) {
        showNotification('Veuillez remplir au minimum l\'âge du verger, le coût de production et la production réelle', 'warning');
        return;
    }
    
    // Sauvegarder dans localStorage
    const annualData = JSON.parse(localStorage.getItem('annualData')) || [];
    annualData.push(data);
    localStorage.setItem('annualData', JSON.stringify(data));
    
    showNotification('Données annuelles enregistrées avec succès !', 'success');
    closeModal('data-modal');
    
    // Mettre à jour la date de soumission
    updateSubmissionDate();
}

// Mettre à jour la date de soumission
function updateSubmissionDate() {
    const today = new Date();
    const dateString = today.getFullYear() + '/' + 
                      String(today.getMonth() + 1).padStart(2, '0') + '/' + 
                      String(today.getDate()).padStart(2, '0');
    document.getElementById('submission-date').textContent = dateString;
}

// Initialiser les événements pour le calcul automatique
document.addEventListener('DOMContentLoaded', function() {
    // Calculer le revenu quand la production ou le prix change
    const productionInput = document.getElementById('production_reelle_data');
    const prixInput = document.getElementById('prix_vente_data');
    
    if (productionInput) {
        productionInput.addEventListener('input', calculateRevenue);
    }
    if (prixInput) {
        prixInput.addEventListener('input', calculateRevenue);
    }
    
    // Mettre à jour la date de soumission
    updateSubmissionDate();
});

// Fonction de test pour vérifier que la prédiction fonctionne
function testPrediction() {
    console.log('Test de la prédiction...');
    
    // Vérifier que les éléments existent
    const elements = [
        'production-estimated',
        'revenue-potential', 
        'benefit-estimated',
        'calculation-details',
        'user-production',
        'recommendations-list',
        'optimization-list'
    ];
    
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            console.log(`✓ Élément ${id} trouvé`);
        } else {
            console.log(`✗ Élément ${id} manquant`);
        }
    });
    
    // Test avec des valeurs par défaut
    const testPrediction = {
        productivity_t_ha: 0.634,
        confidence: 94,
        recommendation: 'Optimale',
        revenue_fcfa: 633772,
        benefit_fcfa: 578772
    };
    
    console.log('Test avec des valeurs:', testPrediction);
    
    // Tester les fonctions
    try {
        updateEstimationCards(testPrediction);
        updateCalculationDetails(testPrediction);
        updateAnalysisAndRecommendations(testPrediction);
        updateOptimizationSuggestions(testPrediction);
        console.log('✓ Toutes les fonctions de mise à jour fonctionnent');
    } catch (error) {
        console.error('✗ Erreur dans les fonctions:', error);
    }
}

// Appeler le test au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Attendre un peu que tout soit chargé
    setTimeout(testPrediction, 1000);
});

// Fonctions pour la section de soumission de données principale
function switchTabMain(tabName) {
    // Masquer tous les onglets
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => pane.classList.remove('active'));
    
    // Désactiver tous les boutons d'onglets
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => btn.classList.remove('active'));
    
    // Activer l'onglet sélectionné
    const activePane = document.getElementById(tabName + '-tab-main');
    if (activePane) {
        activePane.classList.add('active');
    }
    
    // Activer le bouton correspondant
    const activeBtn = event.target.closest('.tab-btn');
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

function incrementValueMain(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        const currentValue = parseFloat(input.value) || 0;
        input.value = (currentValue + 0.1).toFixed(1);
    }
}

function decrementValueMain(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        const currentValue = parseFloat(input.value) || 0;
        const newValue = Math.max(0, currentValue - 0.1);
        input.value = newValue.toFixed(1);
    }
}

function submitAnnualDataMain() {
    // Récupérer toutes les données du formulaire
    const formData = {
        // Données agronomiques
        age_verger: parseFloat(document.getElementById('age_verger_main').value) || 0,
        agroforest: document.getElementById('agroforest_main').value,
        engrais: document.getElementById('engrais_main').value,
        fumier: document.getElementById('fumier_main').value,
        maladie: document.getElementById('maladie_main').value,
        herbicide: document.getElementById('herbicide_main').value,
        insecticide: document.getElementById('insecticide_main').value,
        fongicide: document.getElementById('fongicide_main').value,
        
        // Données économiques
        cout_prod: parseFloat(document.getElementById('cout_prod_main').value) || 0,
        prix_vente: parseFloat(document.getElementById('prix_vente_main').value) || 0,
        production_reelle: parseFloat(document.getElementById('production_reelle_main').value) || 0,
        revenu_total: parseFloat(document.getElementById('revenu_total_main').value) || 0,
        
        // Données géographiques
        region: document.getElementById('region_main').value,
        pluviometrie: document.getElementById('pluviometrie_main').value,
        temperature: parseFloat(document.getElementById('temperature_main').value) || 0,
        humidite: parseFloat(document.getElementById('humidite_main').value) || 0,
        
        // Date de soumission
        date_soumission: document.getElementById('submission-date-main').textContent || new Date().toISOString()
    };
    
    // Sauvegarder dans localStorage (ancien format pour compatibilité)
    localStorage.setItem('annualData', JSON.stringify(formData));
    
    // Récupérer l'ID du producteur actuel (si défini par un professionnel)
    const currentProducerId = localStorage.getItem('current_producer_id');
    
    // Si un producteur est associé, sauvegarder ses données pour le professionnel
    if (currentProducerId) {
        const allProducerData = JSON.parse(localStorage.getItem('all_producer_submissions')) || {};
        if (!allProducerData[currentProducerId]) {
            allProducerData[currentProducerId] = [];
        }
        allProducerData[currentProducerId].push(formData);
        localStorage.setItem('all_producer_submissions', JSON.stringify(allProducerData));
        console.log('✅ Données associées au producteur ID:', currentProducerId);
    } else {
        console.log('ℹ️ Aucun code producteur associé. Les données seront sauvegardées localement uniquement.');
    }
    
    // Afficher une notification de succès
    showNotification('✅ Vos données ont été enregistrées avec succès !', 'success');
    
    // Mettre à jour la date de soumission
    updateSubmissionDateMain();
    
    console.log('Données soumises:', formData);
    if (currentProducerId) {
        console.log('Données associées au producteur:', currentProducerId);
    }
}

function updateSubmissionDateMain() {
    const today = new Date();
    const dateString = today.getFullYear() + '/' + 
                      String(today.getMonth() + 1).padStart(2, '0') + '/' + 
                      String(today.getDate()).padStart(2, '0');
    
    const dateElement = document.getElementById('submission-date-main');
    if (dateElement) {
        dateElement.textContent = dateString;
    }
}

function showNotification(message, type = 'info') {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Ajouter au body
    document.body.appendChild(notification);
    
    // Afficher avec animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Masquer après 5 secondes
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les graphiques
    initializeCharts();
    
    // Charger les données du profil
    const profileData = JSON.parse(localStorage.getItem('userProfile'));
    if (profileData) {
        updateProfileDisplay(profileData);
    }
    
    // Mettre à jour le résumé des plantations
    updatePlantationSummary();
    
    // Ajouter la classe active au lien de navigation actuel
    const currentSection = window.location.hash || '#home';
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentSection) {
            link.classList.add('active');
        }
    });
    
    // Observer le scroll pour mettre à jour la navigation active
    window.addEventListener('scroll', updateActiveNavigation);
    
    // Animation des cartes au chargement
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Initialiser la date de soumission
    updateSubmissionDateMain();
    
    // Charger les données existantes si disponibles
    const savedData = localStorage.getItem('annualData');
    if (savedData) {
        const data = JSON.parse(savedData);
        
        // Remplir les champs avec les données sauvegardées
        Object.keys(data).forEach(key => {
            const element = document.getElementById(key + '_main');
            if (element) {
                if (element.type === 'number') {
                    element.value = data[key] || '';
                } else {
                    element.value = data[key] || '';
                }
            }
        });
    }
    
    // Ajouter des écouteurs d'événements pour le calcul automatique du revenu
    const productionInput = document.getElementById('production_reelle_main');
    const prixInput = document.getElementById('prix_vente_main');
    const revenuInput = document.getElementById('revenu_total_main');
    
    if (productionInput && prixInput && revenuInput) {
        function calculateRevenue() {
            const production = parseFloat(productionInput.value) || 0;
            const prix = parseFloat(prixInput.value) || 0;
            const revenu = production * prix;
            revenuInput.value = revenu.toFixed(0);
        }
        
        productionInput.addEventListener('input', calculateRevenue);
        prixInput.addEventListener('input', calculateRevenue);
    }
});

// Fonctions pour gérer l'affichage des sections
function showPredictionSection() {
    const featuresSection = document.querySelector('.features-section');
    const currentStatusSection = document.querySelector('.current-status-section');
    const predictionSection = document.getElementById('prediction-section');
    
    if (featuresSection) featuresSection.style.display = 'none';
    if (currentStatusSection) currentStatusSection.style.display = 'none';
    if (predictionSection) {
        predictionSection.style.display = 'block';
        // Faire défiler vers le haut de la section prédiction
        predictionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function showHomeSection() {
    const featuresSection = document.querySelector('.features-section');
    const currentStatusSection = document.querySelector('.current-status-section');
    const predictionSection = document.getElementById('prediction-section');
    
    if (featuresSection) featuresSection.style.display = 'block';
    if (currentStatusSection) currentStatusSection.style.display = 'block';
    if (predictionSection) {
        predictionSection.style.display = 'none';
        // Faire défiler vers le haut de la page
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Fonction améliorée pour le bouton de retour
function handleBackButton() {
    // Si on est sur index.html, ne rien faire ou fermer l'application
    if (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/')) {
        // Optionnel : demander confirmation pour quitter
        if (confirm('Voulez-vous vraiment quitter l\'application ?')) {
            window.close();
        }
        return;
    }
    
    // Sinon, retourner à la page d'accueil
    window.location.href = 'index.html';
}

// Améliorer les boutons de retour avec fonctionnalité intelligente
document.addEventListener('DOMContentLoaded', function() {
    const backButtons = document.querySelectorAll('.btn-back');
    backButtons.forEach(btn => {
        // Si le bouton n'a pas déjà un href, ajouter la fonctionnalité
        if (!btn.getAttribute('href')) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                handleBackButton();
            });
        } else {
            // Améliorer l'animation au clic
            btn.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        }
    });
    
    // Améliorer le bouton Quitter sur index.html
    const disconnectBtn = document.querySelector('.btn-disconnect');
    if (disconnectBtn) {
        disconnectBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Voulez-vous vraiment quitter l\'application ?')) {
                // Optionnel : effacer les données de session
                localStorage.clear();
                window.close();
            }
        });
    }
});
