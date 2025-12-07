// Fonctions pour la page des revenus

// Charger les données de revenus
function loadRevenueData() {
    // Simuler le chargement des données depuis l'API
    fetch('http://localhost:5000/revenue-stats')
        .then(response => response.json())
        .then(data => {
            updateRevenueDisplay(data);
        })
        .catch(error => {
            console.log('Utilisation des données par défaut');
            loadDefaultRevenueData();
        });
}

// Mettre à jour l'affichage des revenus
function updateRevenueDisplay(data) {
    document.getElementById('revenue-value').textContent = formatNumber(data.revenue) + ' FCFA';
    document.getElementById('benefit-value').textContent = formatNumber(data.benefit) + ' FCFA';
    document.getElementById('margin-value').textContent = data.margin + '%';
    document.getElementById('productivity-value').textContent = data.productivity + ' t/ha';
    document.getElementById('price-value').textContent = data.price + ' FCFA/kg';
    document.getElementById('cost-value').textContent = formatNumber(data.cost) + ' FCFA/ha';
}

// Charger les données par défaut
function loadDefaultRevenueData() {
    const defaultData = {
        revenue: 937500,
        benefit: 487500,
        margin: 52.0,
        productivity: 1.25,
        price: 750,
        cost: 450000
    };
    updateRevenueDisplay(defaultData);
}

// Calculer le ROI
function calculateROI() {
    const investment = parseFloat(document.getElementById('investment-amount').value) || 0;
    const increase = parseFloat(document.getElementById('expected-increase').value) || 0;
    
    if (investment <= 0 || increase <= 0) {
        showNotification('Veuillez entrer des valeurs valides', 'warning');
        return;
    }
    
    // Calculs basés sur les données actuelles
    const currentRevenue = 937500; // FCFA/ha
    const currentBenefit = 487500; // FCFA/ha
    
    // Calcul du gain supplémentaire
    const additionalRevenue = currentRevenue * (increase / 100);
    const additionalBenefit = additionalRevenue - (investment * 0.1); // Coût supplémentaire estimé
    
    // Calcul du ROI
    const roi = ((additionalBenefit / investment) * 100);
    
    // Temps de retour sur investissement
    const paybackMonths = Math.ceil(investment / (additionalBenefit / 12));
    
    // Afficher les résultats
    document.getElementById('roi-value').textContent = roi.toFixed(1) + '%';
    document.getElementById('additional-gain').textContent = formatNumber(additionalBenefit) + ' FCFA/an';
    document.getElementById('payback-time').textContent = paybackMonths + ' mois';
    
    // Animation des résultats
    animateROIResults();
    
    showNotification('ROI calculé avec succès !', 'success');
}

// Animer les résultats du ROI
function animateROIResults() {
    const results = document.querySelectorAll('.result-value');
    results.forEach((result, index) => {
        setTimeout(() => {
            result.style.transform = 'scale(1.1)';
            setTimeout(() => {
                result.style.transform = 'scale(1)';
            }, 200);
        }, index * 100);
    });
}

// Afficher les détails d'une amélioration
function showImprovementDetails(type) {
    const improvements = {
        fertilizer: {
            title: 'Optimisation des Engrais',
            description: 'Augmenter l\'utilisation d\'engrais organiques et optimiser les doses selon les besoins du sol.',
            steps: [
                'Analyse du sol pour déterminer les carences',
                'Utilisation d\'engrais organiques (compost, fumier)',
                'Application d\'engrais chimiques en doses optimales',
                'Rotation des types d\'engrais',
                'Suivi de l\'efficacité'
            ],
            benefits: [
                'Amélioration de la structure du sol',
                'Réduction des coûts à long terme',
                'Meilleure résistance des plants',
                'Augmentation de la productivité'
            ],
            timeline: '3-6 mois pour voir les premiers résultats'
        },
        agroforestry: {
            title: 'Agroforesterie',
            description: 'Introduire des arbres d\'ombrage pour améliorer la résilience et la biodiversité.',
            steps: [
                'Sélection d\'arbres d\'ombrage appropriés',
                'Planification de la disposition',
                'Plantation des arbres d\'ombrage',
                'Entretien et taille régulière',
                'Suivi de l\'impact sur le cacao'
            ],
            benefits: [
                'Protection contre le soleil et le vent',
                'Amélioration de la biodiversité',
                'Réduction de l\'érosion',
                'Source de revenus supplémentaires'
            ],
            timeline: '2-3 ans pour un impact significatif'
        },
        irrigation: {
            title: 'Irrigation Optimisée',
            description: 'Système d\'irrigation goutte-à-goutte pour les périodes sèches.',
            steps: [
                'Évaluation des besoins en eau',
                'Conception du système d\'irrigation',
                'Installation des équipements',
                'Programmation des cycles d\'irrigation',
                'Maintenance régulière'
            ],
            benefits: [
                'Production stable toute l\'année',
                'Réduction du stress hydrique',
                'Optimisation de l\'utilisation de l\'eau',
                'Augmentation du rendement'
            ],
            timeline: '6-12 mois pour l\'installation complète'
        },
        varieties: {
            title: 'Variétés Résistantes',
            description: 'Planter des variétés de cacao résistantes aux maladies.',
            steps: [
                'Identification des variétés résistantes',
                'Préparation du terrain',
                'Plantation des nouveaux plants',
                'Entretien et formation',
                'Suivi de la performance'
            ],
            benefits: [
                'Réduction des pertes dues aux maladies',
                'Meilleure qualité du cacao',
                'Réduction des traitements chimiques',
                'Augmentation de la productivité'
            ],
            timeline: '3-5 ans pour la première récolte'
        },
        'pest-control': {
            title: 'Gestion Intégrée des Ravageurs',
            description: 'Lutte biologique contre les ravageurs et maladies.',
            steps: [
                'Identification des ravageurs présents',
                'Introduction d\'agents de lutte biologique',
                'Mise en place de pièges',
                'Surveillance régulière',
                'Ajustement des stratégies'
            ],
            benefits: [
                'Réduction de l\'utilisation de pesticides',
                'Protection de l\'environnement',
                'Amélioration de la qualité',
                'Réduction des coûts de production'
            ],
            timeline: '6-12 mois pour un contrôle efficace'
        },
        training: {
            title: 'Formation Continue',
            description: 'Formation aux bonnes pratiques agricoles.',
            steps: [
                'Évaluation des besoins en formation',
                'Participation aux programmes de formation',
                'Application des nouvelles techniques',
                'Suivi et évaluation',
                'Formation continue'
            ],
            benefits: [
                'Amélioration des compétences',
                'Adoption de nouvelles technologies',
                'Meilleure gestion de la plantation',
                'Augmentation de la productivité'
            ],
            timeline: 'Formation continue tout au long de l\'année'
        }
    };
    
    const improvement = improvements[type];
    if (!improvement) return;
    
    // Créer la modal avec les détails
    const modal = document.createElement('div');
    modal.className = 'improvement-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${improvement.title}</h2>
                <button class="modal-close" onclick="this.parentElement.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <p class="modal-description">${improvement.description}</p>
                
                <div class="modal-section">
                    <h3><i class="fas fa-list-ol"></i> Étapes d'implémentation</h3>
                    <ol class="steps-list">
                        ${improvement.steps.map(step => `<li>${step}</li>`).join('')}
                    </ol>
                </div>
                
                <div class="modal-section">
                    <h3><i class="fas fa-check-circle"></i> Bénéfices attendus</h3>
                    <ul class="benefits-list">
                        ${improvement.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="modal-section">
                    <h3><i class="fas fa-clock"></i> Timeline</h3>
                    <p class="timeline">${improvement.timeline}</p>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">
                    Fermer
                </button>
                <button class="btn btn-primary" onclick="startImprovement('${type}')">
                    Commencer l'amélioration
                </button>
            </div>
        </div>
    `;
    
    // Styles pour la modal
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        padding: 1rem;
    `;
    
    document.body.appendChild(modal);
    
    // Animation d'entrée
    setTimeout(() => {
        modal.querySelector('.modal-content').style.transform = 'scale(1)';
        modal.querySelector('.modal-content').style.opacity = '1';
    }, 100);
}

// Commencer une amélioration
function startImprovement(type) {
    showNotification(`Amélioration "${type}" ajoutée à votre plan d'action !`, 'success');
    
    // Ici vous pouvez ajouter la logique pour sauvegarder l'amélioration
    const improvements = JSON.parse(localStorage.getItem('improvements') || '[]');
    improvements.push({
        type: type,
        startDate: new Date().toISOString(),
        status: 'planned'
    });
    localStorage.setItem('improvements', JSON.stringify(improvements));
    
    // Fermer la modal
    document.querySelector('.improvement-modal').remove();
}

// Formater les nombres avec des espaces
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
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
        z-index: 10001;
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

// Styles CSS pour la modal
const modalStyles = document.createElement('style');
modalStyles.textContent = `
    .modal-content {
        background: white;
        border-radius: 12px;
        max-width: 600px;
        width: 100%;
        max-height: 80vh;
        overflow-y: auto;
        transform: scale(0.9);
        opacity: 0;
        transition: all 0.3s ease;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .modal-header h2 {
        margin: 0;
        color: var(--text-primary);
    }
    
    .modal-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--text-secondary);
    }
    
    .modal-body {
        padding: 1.5rem;
    }
    
    .modal-description {
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .modal-section {
        margin-bottom: 1.5rem;
    }
    
    .modal-section h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .steps-list {
        padding-left: 1.5rem;
    }
    
    .steps-list li {
        margin-bottom: 0.5rem;
        color: var(--text-secondary);
    }
    
    .benefits-list {
        list-style: none;
        padding: 0;
    }
    
    .benefits-list li {
        padding: 0.5rem 0;
        color: var(--text-secondary);
        position: relative;
        padding-left: 1.5rem;
    }
    
    .benefits-list li:before {
        content: '✓';
        position: absolute;
        left: 0;
        color: var(--success-color);
        font-weight: bold;
    }
    
    .timeline {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .modal-footer {
        padding: 1.5rem;
        border-top: 1px solid #e9ecef;
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
    }
    
    .btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary {
        background: #6c757d;
        color: white;
    }
    
    .btn-primary {
        background: var(--gradient-primary);
        color: white;
    }
    
    .btn:hover {
        transform: translateY(-2px);
    }
    
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
`;
document.head.appendChild(modalStyles);

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    loadRevenueData();
    
    // Ajouter des événements pour les améliorations
    document.querySelectorAll('.improvement-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
        });
    });
});
