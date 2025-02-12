import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def prepare_data():
    d_student = pd.read_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/raw/admission.csv') 
    d_student = d_student.drop('Serial No.', axis=1)
    #### Floating columns
    for c in d_student.columns:
        d_student[c] = d_student[c].astype(float)
        d_student = d_student.rename(columns={c: c.replace(' ', '_')})
    #### Normalizing matrix
    d_student_scld = StandardScaler().fit(d_student.drop('Chance_of_Admit_', axis=1))
    d_student_scld = d_student_scld.transform(d_student.drop('Chance_of_Admit_', axis=1))
    d_student_scld = pd.DataFrame(d_student_scld, columns=d_student.drop('Chance_of_Admit_', axis=1).columns.tolist())
    X = d_student_scld
    y = d_student['Chance_of_Admit_']
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    print(f"Dataset shape: {X.shape}")
    print(f"Train set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    X_train.to_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/X_train.csv', index=False)
    X_test.to_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/X_test.csv', index=False)
    y_train.to_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/y_train.csv', index=False)
    y_test.to_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/processed/y_test.csv', index=False)
    
    
prepare_data()