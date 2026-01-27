# 🌍 World Real Estate Analyzer

**M2 Software - 2025-2026 Group Members: [Rim Bouaouiss], [Khalil Akchi], [Student 2 Name]

## 🎯 Overview
This is a global real estate market analysis application built with Python, Pandas, and Streamlit. The project features live REST API integration for exchange rates and is fully containerized using Docker


### Via Docker (Recommandé)
1. Assurez-vous d'avoir Docker installé.
2. Lancez l'application :
```bash
docker-compose up --build
Access the interactive dashboard at: http://localhost:8501.


## Via Local Python Environment**

Create a virtual environment: python -m venv venv && source venv/bin/activate.

Install dependencies:

Bash
pip install -r requirements.txt
Run the dashboard:

Bash
streamlit run app/streamlit_app.py
🧪 Quality Testing

We use pytest to ensure the reliability of our analytical calculations.

#### Run the Tests

To execute the unit test suite, ensure you are in your virtual environment and run:

Bash
python -m pytest



## 🧪 Tests de Qualité
Nous utilisons `pytest` pour garantir la fiabilité de nos calculs analytiques.

### Lancer les tests
Pour exécuter la suite de tests unitaires, assurez-vous d'être dans l'environnement virtuel et lancez :
```bash
python -m pytest

##  Frontend & Integration

### UI Features
***Global Interactive Map**: A world overview of the House Price Index using Plotly Choropleth.
* **Advanced Filtering**: Integrated a **Surface Area Slider** in the sidebar. 
    * *Note:* This feature is currently in "UI-Ready" mode.The logic is fully implemented to filter data once the `Surface` attribute is integrated into the core dataset.
* **Live Currency Conversion**: Integration of a REST API to convert housing indices from USD to EUR in real-time.

### Quality & Integration
* **Project Structure**: Organized the repository into `src/` (logic), `app/` (UI), and `data/` folders[cite: 1, 3].
**Robustness**: Implemented `pytest` for calculating analytics and handled library compatibility issues (e.g., NumPy < 2.0.0).
***Containerization**: Configured the `Dockerfile` and `compose.yml` to launch the Streamlit dashboard on port 8501.