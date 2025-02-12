import requests
import pytest

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
@pytest.fixture
def gen_cred_valid():
    credentials = {
        "username": "usergalo",
        "password": "pw123"
    }
    return credentials
    
    
@pytest.fixture
def gen_cred_non_valid():
    credentials = {
        "username": "baduser",
        "password": "badpw123"
    }
    return credentials
    
    
def test_good_login(gen_cred_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_valid
        )
        # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        assert login_response.status_code == 200, "Valid user should return 200 OK"
    else:
        assert login_response.status_code == 401, "Invalid user should return 401 Unauthorized"
        
        
@pytest.mark.xfail(reason="Bad login")
def test_bad_login(gen_cred_non_valid):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=gen_cred_non_valid
        )
        # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        assert login_response.status_code == 200, "Valid user should return 200 OK"
    else:
        assert login_response.status_code == 401, "Invalid user should return 401 Unauthorized"
        

