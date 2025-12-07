import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
import joblib

# Création de données synthétiques basées sur des patterns typiques de production de cacao
np.random.seed(42)

# Paramètres pour générer des données réalistes
n_samples = 1000

# Génération des données
data = {
    'Coût_production/ha': np.random.uniform(200000, 600000, n_samples),
    'Age_verger': np.random.uniform(1, 30, n_samples),
    'Région': np.random.choice(['Indenie-Djuablin', 'Yamoussoukro', 'La Me', 'San-Pedro', 'Grand-Ponts'], n_samples),
    'Pluviometrie': np.random.choice(['Faible', 'Moyenne', 'Élevée'], n_samples),
    'Sexe': np.random.choice(['Masculin', 'Feminin'], n_samples),
    'Niveau_education': np.random.choice(['Primaire', 'Secondaire', 'Supérieur', 'Non renseigné'], n_samples),
    'Competences': np.random.choice(['oui, lire et écrire', 'oui, lire seulement', 'non'], n_samples),
    'Engrais chimique': np.random.choice(['Oui', 'Non'], n_samples),
    'Agroforesterie': np.random.choice(['Oui', 'Non'], n_samples),
    'fumier/ compost': np.random.choice(['Oui', 'Non'], n_samples),
    'Herbicide': np.random.choice(['Oui', 'Non'], n_samples),
    'Insecticide': np.random.choice(['Oui', 'Non'], n_samples),
    'Fongicide': np.random.choice(['Oui', 'Non'], n_samples),
    'Maladie': np.random.choice(['Non', 'Un peu', 'Oui'], n_samples),
}

# Création du DataFrame
df = pd.DataFrame(data)

# Génération de la productivité basée sur des règles logiques
def generate_productivity(row):
    base_prod = 0.5  # Production de base
    
    # Effet de l'âge du verger (pic entre 8-15 ans)
    age_effect = 0.1 * np.exp(-0.1 * (row['Age_verger'] - 10)**2)
    
    # Effet des engrais
    engrais_effect = 0.2 if row['Engrais chimique'] == 'Oui' else 0
    
    # Effet de l'agroforesterie
    agro_effect = 0.15 if row['Agroforesterie'] == 'Oui' else 0
    
    # Effet du fumier
    fumier_effect = 0.1 if row['fumier/ compost'] == 'Oui' else 0
    
    # Effet des maladies (négatif)
    maladie_effect = -0.3 if row['Maladie'] == 'Oui' else (-0.1 if row['Maladie'] == 'Un peu' else 0)
    
    # Effet de la pluviométrie
    pluv_effects = {'Faible': -0.2, 'Moyenne': 0, 'Élevée': 0.1}
    pluv_effect = pluv_effects[row['Pluviometrie']]
    
    # Effet régional
    region_effects = {
        'Indenie-Djuablin': 0.1,
        'Yamoussoukro': 0.05,
        'La Me': 0.08,
        'San-Pedro': 0.15,
        'Grand-Ponts': 0.12
    }
    region_effect = region_effects[row['Région']]
    
    # Bruit aléatoire
    noise = np.random.normal(0, 0.1)
    
    # Calcul de la productivité finale
    productivity = base_prod + age_effect + engrais_effect + agro_effect + fumier_effect + maladie_effect + pluv_effect + region_effect + noise
    
    # Limiter entre 0.1 et 2.0 t/ha
    return max(0.1, min(2.0, productivity))

# Application de la fonction de génération
df['Productivite'] = df.apply(generate_productivity, axis=1)

# Séparation des features et target
X = df.drop('Productivite', axis=1)
y = df['Productivite']

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définition des colonnes numériques et catégorielles
numeric_features = ['Coût_production/ha', 'Age_verger']
categorical_features = ['Région', 'Pluviometrie', 'Sexe', 'Niveau_education', 'Competences', 
                       'Engrais chimique', 'Agroforesterie', 'fumier/ compost', 
                       'Herbicide', 'Insecticide', 'Fongicide', 'Maladie']

# Création du pipeline de préprocessing
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combinaison des transformers
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Création du pipeline complet
model = Pipeline([
    ('prep', preprocessor),
    ('model', XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    ))
])

# Entraînement du modèle
print("Entraînement du modèle...")
model.fit(X_train, y_train)

# Évaluation
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Score R² sur l'ensemble d'entraînement: {train_score:.4f}")
print(f"Score R² sur l'ensemble de test: {test_score:.4f}")

# Sauvegarde du modèle
print("Sauvegarde du modèle...")
joblib.dump(model, 'model_productivite_xgb.pkl')

print("Modèle sauvegardé avec succès dans 'model_productivite_xgb.pkl'")

# Test de chargement
print("Test de chargement du modèle...")
loaded_model = joblib.load('model_productivite_xgb.pkl')
print("Modèle chargé avec succès !")

# Test de prédiction
sample_data = pd.DataFrame({
    'Coût_production/ha': [400000],
    'Age_verger': [10],
    'Région': ['Indenie-Djuablin'],
    'Pluviometrie': ['Moyenne'],
    'Sexe': ['Masculin'],
    'Niveau_education': ['Primaire'],
    'Competences': ['oui, lire et écrire'],
    'Engrais chimique': ['Oui'],
    'Agroforesterie': ['Oui'],
    'fumier/ compost': ['Non'],
    'Herbicide': ['Non'],
    'Insecticide': ['Non'],
    'Fongicide': ['Non'],
    'Maladie': ['Non']
})

prediction = loaded_model.predict(sample_data)
print(f"Test de prédiction: {prediction[0]:.3f} t/ha")
