import requests
import pytest
from datetime import datetime, timedelta
import jwt
import time
import json

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/predict"

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# Function to create a JWT token
def create_jwt_token(user_id: str, time_sec: int):
    """Create JWT token."""
    expiration = datetime.utcnow() + timedelta(seconds=time_sec)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token
    
    
def verify_jwt(token):
    """Decode JWT and handle expiration."""
    valid = True
    time.sleep(3)
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        print("Token is valid:", decoded)
    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        valid = False
    except jwt.InvalidTokenError:
        print("Invalid token!")
        valid = False
    return valid

#validity = verify_jwt(create_jwt_token('usergalo', 100))
#print(validity)
    
# Données de connexion
@pytest.fixture
def gen_cred_valid(validity = verify_jwt(create_jwt_token('usergalo', 100))):
    if validity:
        credentials = {
            "username": "usergalo",
            "password": "pw123"
        }
    else:
        credentials = {
            "username": "",
            "password": ""
        }       
    return credentials
    
    
@pytest.fixture
def gen_cred_invalid(validity = verify_jwt(create_jwt_token('usergalo', 1))):
    if validity:
        credentials = {
            "username": "usergalo",
            "password": "pw123"
        }
    else:
        credentials = {
            "username": "",
            "password": ""
        }       
    return credentials

@pytest.mark.xfail(reason="Invalid token")
def test_predict_invalid_token(gen_cred_invalid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_invalid#()
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        # Data to be sent to the prediction endpoint
        data = {
      		  "GRE_Score": 0.2,
      		  "TOEFL_Score": 0.7,
      		  "University_Rating": 0.89,
      		  "SOP": -1.9,
      		  "LOR_": 1.02,
      		  "CGPA": -1.9,
      		  "Research": 1
        }
        # Send a POST request to the prediction
        response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=data
        )
        assert isinstance(json.loads(response.text)['prediction'][0], float)
        assert json.loads(response.text)['prediction'][0] > 0
    else:
        assert login_response.status_code == 401, "Invalid token should return 401 Unauthorized"
        

def test_predict_valid(gen_cred_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_valid#()
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        # Data to be sent to the prediction endpoint
        data = {
      		  "GRE_Score": 0.2,
      		  "TOEFL_Score": 0.7,
      		  "University_Rating": 0.89,
      		  "SOP": -1.9,
      		  "LOR_": 1.02,
      		  "CGPA": -1.9,
      		  "Research": 1
        }
        # Send a POST request to the prediction
        response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=data
        )
        assert isinstance(json.loads(response.text)['prediction'][0], float)
        assert json.loads(response.text)['prediction'][0] > 0
    else:
        assert login_response.status_code == 401, "Invalid format should return 401 Unauthorized"


@pytest.mark.xfail(reason="Invalid data format")
def test_predict_data_format(gen_cred_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_valid
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        # Data to be sent to the prediction endpoint
        data = {
      		  "GRE_Score": 0.2,
      		  "TOEFL_Score": 'casa',
      		  "University_Rating": 0.89,
      		  "SOP": -1.9,
      		  "LOR_": 1.02,
      		  "CGPA": -1.9,
      		  "Research": 1
        }
        # Send a POST request to the prediction
        response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=data
        )
        assert len(json.loads(response.text)['prediction']) > 0
    else:
        assert json.loads(response.text)['prediction'][0], "Invalid data format (string = 'casa')"
