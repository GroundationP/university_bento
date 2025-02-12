import sklearn
import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error as MSE
import joblib
import numpy as np
import bentoml
from bentoml.io import NumpyNdarray

X_train = pd.read_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/X_train.csv')
X_test = pd.read_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/X_test.csv')
y_train = pd.read_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/y_train.csv')
y_test = pd.read_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/y_test.csv')
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

SEED = 42

# Instantiate a random forest regressor 'rf'
rf = RandomForestRegressor(random_state=SEED)

# Inspect rf's hyperparameters
rf.get_params()

# Define the dictionary 'params_rf'
params_rf = {
    'n_estimators': [10], # While a higher number of trees can improve performance, it also increases the risk of overfitting
    'max_depth': [2, 4], #Limit the maximum depth of each tree to control their complexity. Deeper trees are more likely to overfit, so finding the right maximum depth is essential.
    'max_features': ['sqrt'], # 'auto', Random Forest introduces randomness by considering only a subset of features for each split. Adjust the max_features parameter to control this randomness and potentially reduce overfitting.
    'min_samples_leaf': [5], # This can prevent the model from creating nodes with very few instances, which may capture noise.
    'min_samples_split': [5, 10],
    'criterion': ['poisson'], #'absolute_error',
    'warm_start': [False],
    'max_samples': [0.1, 0.5]
}

# Instantiate grid_rf
grid_rf = GridSearchCV(estimator=rf, param_grid=params_rf, scoring='neg_mean_squared_error', cv=3, verbose=1, n_jobs=-1) # Employ cross-validation to evaluate your model's performance on different subsets of the training data. This helps in identifying whether the model is overfitting and guides the selection of hyperparameters.

# Fit grid_rf to the training data
grid_rf.fit(X_train, y_train)

# Extract the best hyperparametres from grid_rf
best_hyperparams_rf = grid_rf.best_params_


#################################
########### Random Forest Optimized
#################################

# Instantiate rf
rfO = RandomForestRegressor(max_depth=best_hyperparams_rf['max_depth'], max_features = best_hyperparams_rf['max_features'], min_samples_leaf = best_hyperparams_rf['min_samples_leaf'], min_samples_split = best_hyperparams_rf['min_samples_split'], n_estimators = best_hyperparams_rf['n_estimators'], random_state=SEED) #

# Fit rf to the training set    
rfO.fit(X_train, y_train)


# Predict train set labels
y_pred_train_rfO = rfO.predict(X_train)

# Evaluate the training set RMSE of dt
R2_train_rfO = rfO.score(X_train, y_train)

# Print R2_train DTO
print(f'Random Forest optimal train R2: {round(R2_train_rfO, 2)}')

# Evaluate the training set RMSE of bc
RMSE_train_rfO = (MSE(y_train, y_pred_train_rfO))**(1/2)

# Print RMSE_train
print(f'Random Forest optimal train set RMSE: {round(RMSE_train_rfO, 2)}')

# predict test dataset
y_pred_test_rfO = rfO.predict(X_test)

# Evaluate the training set RMSE of dt
R2_test_rfO = rfO.score(X_test, y_test)

# Print R2_train DTO
print(f'Random Forest optimal test R2: {round(R2_test_rfO, 2)}')

# Evaluate the training set RMSE of dt
RMSE_test_rfO = (MSE(y_test, y_pred_test_rfO))**(1/2)

# Print rmse_test
print(f'Random Forest optimal test set RMSE: {round(RMSE_test_rfO, 2)}')

# Enregistrer le modèle dans le Model Store de BentoML
model_ref = bentoml.sklearn.save_model("university_rf", rfO)
print(f"Modèle enregistré sous : {model_ref}")