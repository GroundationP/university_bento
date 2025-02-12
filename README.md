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

#### Step 5 - Copy and paste the query.txt file available to test API
