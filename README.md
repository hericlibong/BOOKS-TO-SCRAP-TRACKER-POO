# Books to Scrape - Price Tracker - Version Programmation Orientée Objet

## Présentation
"Books to Scrape - Price Tracker" est un programme Python conçu pour extraire les données des livres à partir du site fictif "Books to Scrape". Utilisant une approche de **Programmation Orientée Objets (POO)**, le programme navigue à travers les pages du site, extrait les informations détaillées de chaque livre, incluant le titre, le prix, le stock, la catégorie, la note des utilisateurs, et l'URL de l'image de couverture. Les données extraites sont sauvegardées dans des fichiers CSV par catégorie et les images de couverture sont téléchargées localement.

## Fonctionnalités
- Extraction des données de tous les livres du site "Books to Scrape".
- Sauvegarde des données extraites dans des fichiers CSV organisés par catégorie.
- Téléchargement des images de couverture des livres.
- Gestion des erreurs de connexion et des délais d'attente avec des tentatives de reconnexion.

## Installation et Prérequis
Pour utiliser "Books to Scrape - Price Tracker", vous aurez besoin de :
- Python version 3.9 ou supérieure.
- Bibliothèques Python : `requests`, `BeautifulSoup4` (bs4), `unidecode`.

## Structure du Programme
Le programme suit une structure orientée objets pour une meilleure organisation et maintenabilité du code :
- `data_extractor.py` : Définit les classes `Scraper` et `DataExtractor` pour le scraping et l'extraction des données.
- `books.py` : Contient la classe `Book` pour représenter chaque livre et gérer la sauvegarde des données et des images.
- `scraper_manager.py` : Implémente la classe `ScraperManager` qui orchestre le processus d'extraction et de sauvegarde.
- `utils.py` : Fournit des fonctions utilitaires comme `clean_filename` pour nettoyer les noms de fichiers.
- `main.py` : Le point d'entrée du programme, qui utilise `ScraperManager` pour lancer l'extraction des données.


### Configuration de l'environnement et installation à partir du terminal

1. cloner le repo Github :
  ```
  git clone https://github.com/hericlibong/BOOKS-TO-SCRAP-TRACKER-POO.git
  ```

2. Allez dans dossier du projet
  ```
  cd BOOKS-TO-SCRAP-TRACKER-POO
  ```

3. Installez un environnement virtuel :
  ```
  python -m venv venv
  ```

4. Activez l'environnement virtuel :
- Sur Windows :
  ```
  venv\Scripts\activate
  ```
- Sur MacOS/Linux :
  ```
  source venv/bin/activate
  ```

5. Installez les dépendances :
  ```
  pip install -r requirements.txt
  ```


## Utilisation

Détails sur comment lancer le script pour récupérer les données.

1. Aller dans le dossier du scraper :
  ```
  cd ScrapingBooks
  ```

Pour lancer le script, exécutez dans le terminal :

``` 
python main.py
```
---
## Récupération des données

- Récupérer les fichiers csv dans `datas_csv`
- Récupérer les couvertures au format jpg dans `book_images`