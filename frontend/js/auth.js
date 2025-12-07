/**
 * Script d'authentification pour Mon Cacao
 * Vérifie l'authentification et le type d'utilisateur avant d'accéder aux pages
 */

function checkAuthentication(userTypeRequired) {
    const userAuthenticated = localStorage.getItem('user_authenticated');
    const userType = localStorage.getItem('user_type');
    const userTypeSelected = localStorage.getItem('user_type_selected');
    
    // Vérifier l'authentification
    if (!userAuthenticated || userAuthenticated !== 'true') {
        // Si pas authentifié, rediriger vers la sélection du type
        window.location.href = 'user-type-selection.html';
        return false;
    }
    
    // Vérifier le type d'utilisateur
    if (!userTypeSelected || userType !== userTypeRequired) {
        // Si c'est un professionnel et qu'on attend un producteur, rediriger
        if (userType === 'professionnel' && userTypeRequired === 'producteur') {
            window.location.href = 'dashboard-professionnel.html';
            return false;
        }
        // Si c'est un producteur et qu'on attend un professionnel, rediriger
        if (userType === 'producteur' && userTypeRequired === 'professionnel') {
            window.location.href = 'index.html';
            return false;
        }
        // Sinon, rediriger vers la page de sélection
        window.location.href = 'user-type-selection.html';
        return false;
    }
    
    return true;
}

function logout() {
    if (confirm('Voulez-vous vous déconnecter ?')) {
        // Supprimer toutes les données d'authentification
        localStorage.removeItem('user_type');
        localStorage.removeItem('user_type_selected');
        localStorage.removeItem('user_authenticated');
        localStorage.removeItem('current_user_id');
        localStorage.removeItem('current_user_name');
        localStorage.removeItem('selected_user_type_for_auth');
        
        // Rediriger vers la page de sélection
        window.location.href = 'user-type-selection.html';
    }
}

function changeUserType() {
    if (confirm('Voulez-vous changer de profil ? Vous serez déconnecté.')) {
        logout();
    }
}

// Fonction pour mettre à jour l'affichage du type d'utilisateur dans le header
function updateUserTypeDisplay() {
    const userType = localStorage.getItem('user_type');
    if (userType === 'producteur') {
        const userInfoSpan = document.querySelector('.user-info span');
        if (userInfoSpan) {
            userInfoSpan.textContent = 'Producteur';
        }
    } else if (userType === 'professionnel') {
        const userInfoSpan = document.querySelector('.user-info span');
        if (userInfoSpan) {
            userInfoSpan.textContent = 'Professionnel';
        }
    }
}

