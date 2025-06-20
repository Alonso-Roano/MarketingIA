from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

def entrenar_modelo_pokemon():
    df = pd.read_excel("app/common/data/pokemons.xlsx")
    X = df[['species_id', 'height', 'weight', 'base_experience', 'order']]
    y = df['is_default']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, "app/models/model_pokemon/current_model.pkl")
    return "modelo_pokemon actualizado"