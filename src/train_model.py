import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import bentoml
import numpy as np

# Read file
def read_data(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data


def trainAndTest(X_train, X_test, y_train, y_test):

    # Créer et entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prédictions sur le test set
    y_pred = model.predict(X_test)

    # Évaluation des performances
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"Performance du modèle :")
    print(f"  - MAE  : {mae:.4f}")
    print(f"  - RMSE : {rmse:.4f}")
    print(f"  - R²   : {r2:.4f}")
    
    return model


def saveToModelStore(model):
    # Enregistrer le modèle dans le Model Store de BentoML
    model_ref = bentoml.sklearn.save_model("admission_students_rf", model)
    print(f"Modèle enregistré sous : {model_ref}")

   
def main():
    # read the file
    X_train_file_path = "./data/processed/X_train.csv"
    X_test_file_path = "./data/processed/X_test.csv"
    y_train_file_path = "./data/processed/y_train.csv"
    y_test_file_path = "./data/processed/y_test.csv"
    X_train = read_data(X_train_file_path)
    X_test = read_data(X_test_file_path)
    y_train = read_data(y_train_file_path)
    y_test = read_data(y_test_file_path)
    
    # train and test
    model = trainAndTest(X_train, X_test, y_train, y_test)
    
    # save 
    saveToModelStore(model)
    

if __name__ == '__main__':
    
    main()