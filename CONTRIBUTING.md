# 🤝 Guide de Contribution - Mon Cacao

Merci de votre intérêt pour contribuer à **Mon Cacao** ! Ce document vous guidera dans le processus de contribution.

## 📋 Table des Matières

- [Code de Conduite](#-code-de-conduite)
- [Comment Contribuer](#-comment-contribuer)
- [Processus de Développement](#-processus-de-développement)
- [Standards de Code](#-standards-de-code)
- [Tests](#-tests)
- [Pull Requests](#-pull-requests)

---

## 📜 Code de Conduite

En participant à ce projet, vous acceptez de respecter un environnement respectueux et inclusif pour tous.

---

## 🚀 Comment Contribuer

### Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/votre-username/mon-cacao/issues)
2. Si ce n'est pas le cas, créez une nouvelle issue avec :
   - Un titre clair et descriptif
   - Une description détaillée du problème
   - Les étapes pour reproduire le bug
   - Le comportement attendu vs le comportement actuel
   - Votre environnement (OS, version Python, navigateur)

### Proposer une Fonctionnalité

1. Vérifiez que la fonctionnalité n'a pas déjà été proposée
2. Créez une issue avec :
   - Une description claire de la fonctionnalité
   - L'utilité de cette fonctionnalité
   - Des exemples d'utilisation si possible

### Contribuer au Code

1. **Fork** le projet
2. **Clone** votre fork : `git clone https://github.com/votre-username/mon-cacao.git`
3. **Créez une branche** : `git checkout -b feature/ma-nouvelle-fonctionnalite`
4. **Faites vos modifications**
5. **Testez** vos modifications
6. **Commitez** : `git commit -m "Ajout: Description de la fonctionnalité"`
7. **Push** : `git push origin feature/ma-nouvelle-fonctionnalite`
8. **Ouvrez une Pull Request**

---

## 🔄 Processus de Développement

### Structure des Branches

- `main` : Branche principale (stable)
- `develop` : Branche de développement
- `feature/*` : Nouvelles fonctionnalités
- `bugfix/*` : Corrections de bugs
- `hotfix/*` : Corrections urgentes

### Workflow

1. Créez une branche depuis `main` ou `develop`
2. Développez votre fonctionnalité
3. Testez localement
4. Créez une Pull Request
5. Attendez la revue de code
6. Après approbation, votre code sera mergé

---

## 📝 Standards de Code

### Python

- Suivez [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilisez des noms de variables descriptifs
- Ajoutez des docstrings pour les fonctions et classes
- Limitez les lignes à 100 caractères

**Exemple :**
```python
def calculer_productivite(surface, production):
    """
    Calcule la productivité en kg/ha.
    
    Args:
        surface (float): Surface en hectares
        production (float): Production en kg
    
    Returns:
        float: Productivité en kg/ha
    """
    if surface <= 0:
        raise ValueError("La surface doit être positive")
    return production / surface
```

### JavaScript

- Utilisez ES6+ (let, const, arrow functions)
- Suivez les conventions camelCase
- Ajoutez des commentaires pour les fonctions complexes
- Utilisez des noms de variables descriptifs

**Exemple :**
```javascript
/**
 * Calcule la productivité du cacao
 * @param {number} surface - Surface en hectares
 * @param {number} production - Production en kg
 * @returns {number} Productivité en kg/ha
 */
const calculerProductivite = (surface, production) => {
    if (surface <= 0) {
        throw new Error("La surface doit être positive");
    }
    return production / surface;
};
```

### HTML/CSS

- Utilisez une indentation cohérente (2 ou 4 espaces)
- Utilisez des noms de classes descriptifs (BEM si possible)
- Organisez le CSS par sections logiques
- Commentez les sections complexes

---

## 🧪 Tests

### Avant de Soumettre

Assurez-vous que :

- [ ] Tous les tests passent : `python -m pytest tests/`
- [ ] Vous avez testé manuellement les nouvelles fonctionnalités
- [ ] Le code respecte les standards de style
- [ ] La documentation est à jour

### Écrire des Tests

- Créez des tests pour les nouvelles fonctionnalités
- Suivez la convention de nommage : `test_*.py`
- Utilisez des assertions claires
- Testez les cas limites et les erreurs

**Exemple :**
```python
def test_calculer_productivite():
    assert calculer_productivite(1, 100) == 100
    assert calculer_productivite(2, 200) == 100
    with pytest.raises(ValueError):
        calculer_productivite(0, 100)
```

---

## 🔀 Pull Requests

### Avant de Créer une PR

- [ ] Votre code est testé
- [ ] Les tests passent
- [ ] La documentation est à jour
- [ ] Le code respecte les standards
- [ ] Vous avez mis à jour le CHANGELOG si nécessaire

### Format de la PR

**Titre :**
```
Type: Description courte (ex: Feature: Ajout du score écologique)
```

**Types possibles :**
- `Feature` : Nouvelle fonctionnalité
- `Fix` : Correction de bug
- `Docs` : Documentation
- `Style` : Formatage
- `Refactor` : Refactorisation
- `Test` : Tests
- `Chore` : Maintenance

**Description :**
```markdown
## Description
Description détaillée des changements

## Type de changement
- [ ] Nouvelle fonctionnalité
- [ ] Correction de bug
- [ ] Documentation
- [ ] Autre

## Comment tester
1. Étape 1
2. Étape 2

## Checklist
- [ ] Code testé
- [ ] Documentation mise à jour
- [ ] Tests passent
```

---

## 📚 Ressources

- [Documentation du projet](README.md)
- [Guide de démarrage rapide](QUICKSTART.md)
- [Structure du projet](STRUCTURE.md)

---

## ❓ Questions ?

Si vous avez des questions :

1. Consultez la [documentation](README.md)
2. Cherchez dans les [Issues existantes](https://github.com/votre-username/mon-cacao/issues)
3. Créez une nouvelle issue avec la question

---

## 🙏 Remerciements

Merci de contribuer à **Mon Cacao** ! Chaque contribution, grande ou petite, est appréciée.

---

<div align="center">

**Fait avec ❤️ pour les producteurs de cacao**

*Dernière mise à jour : Décembre 2024*

</div>

