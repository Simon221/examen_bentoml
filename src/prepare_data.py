import pandas as pd
from sklearn.model_selection import train_test_split
import os
from sklearn.preprocessing import StandardScaler


# Read file
def read_data(file_path):
    raw_data = pd.read_csv(file_path)
    return raw_data

# Fais le preprocessing et renvoie les données nettoyées
def preprocessing(df):
    # Nettoyage des noms de colonnes
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Vérifier et traiter les valeurs manquantes
    df = df.dropna()
    
    # Assurer que Serial No. est un entier et Assurer que Research est binaire
    df["serial_no."] = df["serial_no."].astype(int)  
    df["research"] = df["research"].astype(int)  
    
    return df


# Split data into training and testing sets
def split_data(df):
    target = df['chance_of_admit']
    data = df.drop(['chance_of_admit'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test

# Save dataframes to their respective output file paths
def save_dataframes(X_train, X_test, y_train, y_test, output_folderpath):
    for file, filename in zip([X_train, X_test, y_train, y_test], ['X_train', 'X_test', 'y_train', 'y_test']):
        output_filepath = os.path.join(output_folderpath, f'{filename}.csv')
        file.to_csv(output_filepath, index=False)
            
def main():
    # read the file
    input_file_path = "./data/raw/admission.csv"
    output_folder = "./data/processed"
    raw_data = read_data(input_file_path)
    
    df = preprocessing(raw_data)
    print(df.head())
    
    # split the file raw data
    X_train, X_test, y_train, y_test = split_data(df)
    
    # save the splitted file to the output folder
    save_dataframes(X_train, X_test, y_train, y_test, output_folder)


if __name__ == '__main__':
    
    main()