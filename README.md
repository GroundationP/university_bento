# Bento API deployment
This is a Bento API to predict chances of admission in a university
The model was built using fictional data on students' grades and profiles to predict their chances of admission to a university. The variables included are:

GRE Score: Score obtained in the GRE test (out of 340)
TOEFL Score: Score obtained in the TOEFL test (out of 120)
University Rating: Rating of the university (out of 5)
SOP: Statement of Purpose score (out of 5)
LOR: Letter of Recommendation score (out of 5)
CGPA: Cumulative Grade Point Average (out of 10)
Research: Research experience (0 or 1)
Chance of Admit: Probability of admission (out of 1)

The dataset was normalized, and the model was trained using Random Forest with hyperparameter tuning via grid search. The main focus is on leveraging BentoML as a deployment solution for the machine learning model, with the goal of deploying it to a cloud platform like AWS.


#### Step 1 - Create env
python3 -m venv bentoml_env

cd  bentoml_env/bin

source activate bentoml_env


#### Step 2 - Instal dependencies
pip3 install -r requirements.txt


#### Step 3 - Instal docker image
docker load -i bento_image.tar

docker images

docker run --rm -p 3000:3000 arde/rf_regressor_service


#### Step 4 - Open a new terminal to launch queries
cd  bentoml_env/bin
source activate bentoml_env

#### Step 5 - Copy and paste the query.txt file available to get a prediction of chances of admission in a university

#### Step 6 - To perform unit tests
pytest tests/test_authentification.py

pytest tests/test_connexion.py

pytest tests/test_prediction.py
