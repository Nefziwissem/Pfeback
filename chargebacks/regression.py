import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Charger les données d'entraînement
X_train = pd.read_csv('../X_train.csv')
y_train = pd.read_csv('../y_train.csv')

# Créer et entraîner le modèle de régression linéaire
model_lr = LinearRegression()
model_lr.fit(X_train[['authorization_number', 'amount', 'status_encoded', 'reason_encoded']], y_train.values.ravel())

# Sauvegarder le modèle entraîné
joblib.dump(model_lr, 'chargeback_resolution_model_lr.pkl')
