import re

def clean_filename(name):
    """
    Nettoie le nom pour le rendre valide comme nom de fichier ou dossier sous Windows.
    Nettoie aussi les noms de dossiers des catégories.
    
    Args:
        name (str): Le nom du fichier ou dossier à nettoyer.
        
    Returns:
        str: Le nom nettoyé, sans caractères invalides et avec des espaces remplacés par des underscores.
    """
    # Caractères invalides à supprimer pour Windows. À adapter si besoin pour d'autres OS.
    invalid_chars = '[\\/*?:"<>|]'
    name = re.sub(invalid_chars, '', name)  # Supprime les caractères invalides.
    name = re.sub(r'\s+', '_', name)  # Remplace les espaces et les séquences d'espaces par des underscores.
    return name



