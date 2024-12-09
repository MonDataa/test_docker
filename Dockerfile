# Utiliser l'image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY app.py requirements.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000
EXPOSE 5000

# Spécifier le volume pour les données persistantes
VOLUME /data

# Commande pour exécuter l'application
CMD ["python", "app.py"]

