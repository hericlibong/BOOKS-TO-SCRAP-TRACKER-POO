# Books to Scrape - Price Tracker

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

### Installation de Python
Assurez-vous d'avoir Python 3.9 ou une version ultérieure installée sur votre système. Vous pouvez le télécharger depuis le site officiel de Python : https://www.python.org/downloads/

### Installation des Dépendances
Après avoir cloné ou téléchargé le code source de "Books to Scrape - Price Tracker", installez les dépendances nécessaires en exécutant la commande suivante dans votre terminal :
