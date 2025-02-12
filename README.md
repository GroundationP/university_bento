# Bento API deployment
Bento API to predict chances of admission in a university

#### Step 1 - Creating environment
python3 -m venv bentoml_env

cd  bentoml_env/bin

source activate bentoml_env


#### Step 2 - Install dependencies
pip3 install -r requirements.txt

#### Step 3 - Unzip docker image
tar -xvf ./docker/bento_image.tar
