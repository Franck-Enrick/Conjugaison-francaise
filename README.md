# 🇫🇷 Conjugueur Français — Application Python (Nouvelle version)

Application desktop de conjugaison automatique des verbes français, développée en Python avec TKinter. Le projet ayant été réalisé bien auparavant (2021), ceci n'est qu'une mise à jour.

---

## ✨ Fonctionnalités

- **Détection automatique du groupe** (1er, 2ème, 3ème groupe) via expressions régulières (`re`)
- **Conjugaison des 6 temps simples** :
  - Présent
  - Imparfait
  - Futur simple
  - Conditionnel présent
  - Subjonctif présent
  - Passé simple
- **Verbes irréguliers** : être, avoir, aller, faire, pouvoir, vouloir, savoir, venir, prendre, mettre, partir, dire, voir…
- **Corrections orthographiques automatiques** : verbes en `-ger` (mangeons), en `-cer` (commençons)
- **Interface graphique TKinter** moderne avec thème sombre 
- **Conjugaison de tous les temps en un clic**
- **Exemples rapides** cliquables pour tester rapidement

---

## 🏗️ Architecture du projet

```
conjugaison_app/
│
├── main.py                  # Interface graphique TKinter
├── conjugation_engine.py    # Moteur de conjugaison (re + dictionnaires)
└── README.md
```

### `conjugation_engine.py`

Le cœur du projet. Il contient :

| Composant | Rôle |
|-----------|------|
| `TERMINAISONS` | Dictionnaire des terminaisons par groupe et par temps |
| `IRREGULIERS` | Dictionnaire complet des verbes irréguliers |
| `detecter_groupe()` | Détection du groupe via `re.search()` |
| `extraire_radical()` | Extraction du radical via `re.sub()` |
| `conjuguer()` | Fonction principale de conjugaison |
| `conjuguer_tous_les_temps()` | Conjugaison à tous les temps |
| `generer_forme()` | Gestion des corrections orthographiques |

### `main.py`

Interface TKinter structurée en classes :

| Classe / méthode | Rôle |
|------------------|------|
| `AppConjugaison` | Fenêtre principale (`tk.Tk`) |
| `_construire_panneau_gauche()` | Panneau de saisie et de configuration |
| `_construire_panneau_droit()` | Zone de résultats avec scroll |
| `_conjuguer()` | Déclenche la conjugaison et affiche les résultats |
| `_afficher_tableau()` | Génère un bloc de résultats pour un temps |

---

## 🚀 Installation & Lancement

---

## 🖥️ Utilisation

1. **Saisir un verbe** à l'infinitif dans le champ de texte (ex. `parler`, `finir`, `être`)
2. **Sélectionner un temps** dans la liste ou cocher **Tous les temps**
3. Cliquer sur **Conjuguer** ou appuyer sur **Entrée**

### Raccourcis clavier

| Touche | Action |
|--------|--------|
| `Entrée` | Conjuguer |
| `Ctrl+Entrée` | Conjuguer |
| `Échap` | Effacer |

---

## 🔧 Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| `Python 3` | Langage principal |
| `tkinter` | Interface graphique |
| `re` | Expressions régulières (détection de groupe, radical) |
| Dictionnaires Python | Stockage des terminaisons et formes irrégulières |

---

## 📚 Exemples de conjugaison

### Verbe régulier — 1er groupe : `parler`

| Pronom | Présent | Imparfait |
|--------|---------|-----------|
| je | parle | parlais |
| tu | parles | parlais |
| il/elle | parle | parlait |
| nous | parlons | parlions |
| vous | parlez | parliez |
| ils/elles | parlent | parlaient |

### Verbe irrégulier — 3ème groupe : `être`

| Pronom | Présent | Futur simple |
|--------|---------|--------------|
| je | suis | serai |
| tu | es | seras |
| il/elle | est | sera |
| nous | sommes | serons |
| vous | êtes | serez |
| ils/elles | sont | seront |

---

*Projet réalisé dans le cadre d'une formation en développement logiciel — CAYSTI 2021* (Ceci étant juste une mise à jour)
