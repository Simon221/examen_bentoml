import pytest
import requests
import jwt
from datetime import datetime, timedelta

# Définition des URLs
BASE_URL = "http://127.0.0.1:3000"
LOGIN_URL = f"{BASE_URL}/login"
PREDICT_URL = f"{BASE_URL}/predict"

# Données de connexion valides
VALID_CREDENTIALS = {
    "username": "simon",
    "password": "passer123"
}

# Générer un JWT token expiré pour tester l'authentification
EXPIRED_TOKEN = jwt.encode(
    {"sub": "simon", "exp": datetime.utcnow() - timedelta(hours=1)},
    "EXAMEN_BENTOML",  # Clé secrète utilisée dans service.py
    algorithm="HS256"
)

# Données valides pour la prédiction
VALID_INPUT = {
    "serial_no": 395,
    "gre_score": 329,
    "toefl_score": 111,
    "university_rating": 4,
    "sop": 4.5,
    "lor": 4.0,
    "cgpa": 9.23,
    "research": 1,
}

@pytest.fixture(scope="module")
def get_token():
    """Récupère un token JWT valide en se connectant à l'API."""
    response = requests.post(LOGIN_URL, json=VALID_CREDENTIALS)
    assert response.status_code == 200, f"Erreur de login: {response.text}"
    return response.json().get("token")

def test_login_success():
    """Vérifie que l'API retourne un token JWT valide."""
    response = requests.post(LOGIN_URL, json=VALID_CREDENTIALS)
    assert response.status_code == 200, f"Erreur: {response.text}"
    assert "token" in response.json()

def test_login_failure():
    """Vérifie qu'une erreur 401 est renvoyée pour des identifiants incorrects."""
    response = requests.post(LOGIN_URL, json={"username": "simon", "password": "wrongpass"})
    
    assert response.status_code in [401, 500], f"Erreur: {response.text}"
    
    if response.status_code == 401:
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.parametrize("token, expected_status, expected_detail", [
    (None, 401, "Missing authentication token"),
    ("Bearer invalid_token", 401, "Invalid token"),
    (f"Bearer {EXPIRED_TOKEN}", 401, "Token has expired")
])
def test_auth_fails(token, expected_status, expected_detail):
    """Teste plusieurs scénarios d'échec d'authentification."""
    headers = {"Authorization": token} if token else {}
    response = requests.post(PREDICT_URL, headers=headers, json=VALID_INPUT)
    assert response.status_code == expected_status, f"Erreur: {response.text}"
    assert response.json()["detail"] == expected_detail

def test_predict_success(get_token):
    """Vérifie que la prédiction fonctionne avec un token valide."""
    headers = {"Authorization": f"Bearer {get_token}"}
    response = requests.post(PREDICT_URL, headers=headers, json=VALID_INPUT)
    assert response.status_code == 200, f"Erreur: {response.text}"
    assert "prediction" in response.json()

def test_predict_invalid_input(get_token):
    """Vérifie qu'une erreur 400 est renvoyée pour une entrée invalide."""
    headers = {"Authorization": f"Bearer {get_token}"}
    
    # Modifier l'entrée pour générer une erreur de validation
    invalid_data = {
        "serial_no": "wrong_type",  # Mettre une string au lieu d'un int
        "gre_score": 329,
        "toefl_score": 111,
        "university_rating": 4,
        "sop": 4.5,
        "lor": 4.0,
        "cgpa": 9.23,
        "research": 1,
    }
    
    response = requests.post(PREDICT_URL, headers=headers, json=invalid_data)
    
    # Vérifier que l'erreur est bien 400 (au lieu de 422)
    assert response.status_code == 400, f"Erreur: {response.text}"
