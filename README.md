# 🌍 World Real Estate Analyzer

**M2 Software - 2025-2026 Group Members: [Rim Bouaouiss], [Khalil Akchi], [Sofiane Boucenna]
GitHub Repository: https://github.com/khalilakchi/world-real-estate-app
## 🎯 Overview
This is a global real estate market analysis application built with Python, Pandas, and Streamlit. The project features live REST API integration for exchange rates and is fully containerized using Docker

# 🛠️ Core Technologies: 
- Backend: Python 3.11+
- Data Processing: Pandas & NumPy
- Interface: Streamlit & Plotly
- Testing: Pytest
- Containerization: Docker & Docker Compose

# 🚀 Installation and Setup

### Via Docker 
1. Ensure you have Docker Desktop installed and running.
2. Launch the application using the following command:
```bash
docker-compose up --build
```
3. Access the interactive dashboard at: http://localhost:8501.


## Via Local Python Environment**

1. Create a virtual environment: 
```bash
python -m venv venv && source venv/bin/activate.
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the dashboard:
```bash
streamlit run app/streamlit_app.py
```


## 🧪 Quality & Best Practices
- Unit Testing: We use pytest to ensure the reliability of our analytical calculations. 
  Run tests with  ```bash python -m pytest.```
- Robustness: Implementation of Type Hints, Docstrings, and Logging to meet professional software standards.
- Resilience: The API client includes timeout management and error handling for external service interruptions.


###📂 Project Structure: 
world-real-estate-app/
├── app/                # Streamlit UI 
├── src/                # Business logic & API client 
├── data/               # Raw and Processed CSV files 
├── tests/              # Unit tests (Pytest) 
├── Dockerfile          # Container configuration
└── compose.yml         # Service orchestration


## NB : 
#### 📊 UI Innovation: Dynamic Feature Simulation

To demonstrate the full potential of the dashboard's filtering capabilities, we implemented a dynamic data enrichment layer:

- Synthetic Attribute Generation: Since the original dataset lacked specific granular details, we utilized NumPy to dynamically generate Surface (m²) and Rooms columns upon loading.

- Advanced Cross-Filtering: This enables real-time interaction where users can filter global indices based on property size and room count.

- Purpose: This serves as a Proof of Concept (PoC), showing that the frontend logic is ready to handle multi-dimensional data as soon as the backend provides it.




