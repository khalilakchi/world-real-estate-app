# Utilisation d'une image légère comme demandé dans les best practices 
FROM python:3.11-slim

# Définition du dossier de travail
WORKDIR /app

# Empêche Python de générer des fichiers .pyc et assure un log en temps réel 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances avant de copier le reste du code (optimisation du cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'intégralité du projet (incluant src/, app/, data/, etc.)
COPY . .

# Exposition du port par défaut de Streamlit 
EXPOSE 8501

# Lancement de ton dashboard final (au lieu de main.py)
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]