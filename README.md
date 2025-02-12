# Bento API deployment
Bento API to predict chances of admission in a university

#### Step 1 - Creating environment
python3 -m venv bentoml_env

cd  bentoml_env/bin

source activate bentoml_env


#### Step 2 - Install dependencies
pip3 install -r requirements.txt


#### Step 3 - Installing docker image
docker load -i bento_image.tar

docker images

docker run --rm -p 3000:3000 arde/rf_regressor_service


#### Step 4 - Open a new terminal to launch queries
cd  bentoml_env/bin
source activate bentoml_env

#### Paste the following example of query to test API

token=$(curl -s -X POST http://127.0.0.1:3000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "usergalo", "password": "pw123"}' | jq -r '.token')
curl -X POST http://127.0.0.1:3000/predict \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $token" \
     -d '{
  		  "GRE_Score": 0.2,
  		  "TOEFL_Score": -0.85,
  		  "University_Rating": 0.89,
  		  "SOP": -1.9,
  		  "LOR_": 1.02,
  		  "CGPA": -1.9,
  		  "Research": 1
}'
