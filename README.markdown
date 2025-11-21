# Chess Tournament Manager

## Description
Chess Tournament Manager est une application locale qui vous permettra de :
- **Gérer les tournois** : Créer des tournois, générer des matchs et entrer les résultats dans l'application, toutes est stocké dans un fichier JSON, et le tournoi peut être repris à tout moments
- **Gérer les joueurs** : Enregistrer des joueurs et toute leurs informations dans une base de données JSON, les rapports sont consultable à tout moment dans l'application
- **RAPPORTS** : Consulter les détails des tournois enregistrés, l'historique des matchs, les joueurs ainsi que tout autres informations relatives aux tournois.

Chess Tournament Manager est programme python autonome et hors ligne qui peut être lancé depuis la console.

## Prérequis
Pour exécuter ce projet, vous devez avoir les outils suivants installés :
- **Python** : Version 3.8 ou supérieure.
- **Git** : Outil de contrôle de version pour cloner le dépaôt.
- **Terminal** : Un terminal comme Command Prompt (Windows), Terminal (macOS), ou un shell Linux.

### Installation de Python
- **Windows** :
  1. Téléchargez Python 3.8 ou supérieur depuis [https://www.python.org/downloads]
  2. Exécutez l'installateur et cochez l'option **"Add Python to PATH"** avant de cliquer sur "Install Now".

- **macOS** :
  1. Téléchargez Python depuis [https://www.python.org/downloads]
  2. Vérifiez avec `python3 --version` et `pip3 --version`.
- **Linux** :
  1. Installez Python avec votre gestionnaire de paquets, par exemple `sudo apt install python3 python3-pip` (Ubuntu).
  2. Vérifiez avec `python3 --version` et `pip3 --version`.

### Installation de Git
- **Windows** :
  1. Téléchargez Git depuis [https://git-scm.com/download/win]
  2. Exécutez l'installateur et acceptez les options par défaut.

- **macOS** :
  1. Installez Git depuis [https://git-scm.com/download/mac]
  2. Vérifiez avec `git --version`.
- **Linux** :
  1. Installez Git avec votre gestionnaire de paquets, par exemple `sudo apt install git` (Ubuntu).
  2. Vérifiez avec `git --version`.

## Installer, configurer et exécuter le projet
Une fois les prérequis complétés, nous pouvons passer à la configuration du script.

### 1. Cloner le dépôt Github en local
Ouvrez votre terminal de commande, déplacer-vous dans le dossier dans lequel vous souhaitez et tapez :
```bash
git clone https://github.com/redaa91ab/chess-tournament-manager
cd chess-tournament-manager
```

### 2. Créer un environnement virtuel
Créez un environnement virtuel nommé `.venv` dans le dossier du projet :
```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel
Activez l'environnement virtuel :
- Sur Windows :
```bash
  .venv\Scripts\activate
```

- Sur macOS/Linux :
```bash
  source .venv/bin/activate
```

Une fois activé, votre invite de commande affichera `(.venv)` pour indiquer que vous êtes dans l'environnement virtuel.

### 4. Installer les dépendances
Installez les bibliothèques nécessaires listées dans `requirements.txt` :
```bash
pip install -r requirements.txt
```
Le fichier `requirements.txt` contient :
```
requests==2.32.4
beautifulsoup4==4.13.4
```
Cela installe `tinydb`, `rich`, et leurs dépendances.

### 5. Exécuter l'application
Exécutez le script principal lancer l'application :
```bash
python main.py
```

## Structure du dépôt
- `main.py` : Le fichier initial du programme.
- `requirements.txt` : Liste des dépendances nécessaires.
- `README.md` : Ce fichier, expliquant l'installation et l'exécution.
- `.gitignore` : Exclut 

## Auteur
Réda Abdi pour le projet "Développez un programme logiciel en Python" dans la formation "Développeur d'applications python" de OpenClassrooms.