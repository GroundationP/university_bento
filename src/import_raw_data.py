import pandas as pd


def main(url = "https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv", ):
    d_student = pd.read_csv(url)
    d_student.to_csv('/Users/terence/A_NOTEBOOKS/Datasciencetest/BENTOML/university/examen_bentoml/data/raw/admission.csv', index=False)


if __name__ == '__main__':
    main()