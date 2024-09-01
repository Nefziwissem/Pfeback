import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Charger les données d'entraînement
X_train = pd.read_csv('./X_train.csv')
y_train = pd.read_csv('./y_train.csv')

# Créer et entraîner le modèle de forêt aléatoire
model_rf = RandomForestRegressor()
model_rf.fit(X_train[['authorization_number', 'amount', 'status_encoded', 'reason_encoded']], y_train.values.ravel())

# Sauvegarder le modèle entraîné
joblib.dump(model_rf, 'chargeback_resolution_model_rf.pkl')
