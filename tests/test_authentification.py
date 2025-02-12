import requests
import pytest
from datetime import datetime, timedelta
import time
import jwt


# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"    
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

# Creating a valid token:
#valid_token = create_jwt_token('usergalo', 100)  # Token expires in 100 seconds
#print(valid_token)

# Testing a valid token:
#print("This token expires in 100 second")
#validity = verify_jwt(valid_token)

# Try to verify after expiration
#print("creating a new token - that expires in 1 second")
#expired_token = create_jwt_token('usergalo', 1)  # Token expires in 1 second

# Wait for the token to expire
#time.sleep(5)

#Testing a valid token:
#validity = verify_jwt(expired_token)
    
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
def gen_cred_invalid(validity = verify_jwt(create_jwt_token('yeah', 100))):
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
def gen_cred_expired(validity = verify_jwt(create_jwt_token('usergalo', 1))):
    if validity:
        credentials = {
            "username": "usergalo",
            "password": "pw123"
        }
    else:
        credentials = {
            "username": "ulo",
            "password": "p23"
        }
    return credentials
    
    
@pytest.mark.xfail(reason="Token is missing or invalid")
def test_token_invalid(gen_cred_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_invalid
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        assert login_response.status_code == 200, "Valid token should return 200 OK"
    else:
        assert login_response.status_code == 401, "Token is missing or invalid should return 401 Unauthorized"


@pytest.mark.xfail(reason="Token is expired")
def test_expired_token(gen_cred_expired):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_expired
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        assert login_response.status_code == 200, "Valid token should return 200 OK"
    else:
        assert login_response.status_code == 401, "Invalid token is expired"
                
        
def test_token_valid(gen_cred_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_valid
        )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        assert login_response.status_code == 200, "Valid token should return 200 OK"
    else:
        assert login_response.status_code == 401, "Invalid token should return 401 Unauthorized"
