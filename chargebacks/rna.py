import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Utiliser un chemin relatif pour les fichiers CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
X_train = pd.read_csv(os.path.join(base_dir, '../X_train.csv'))
y_train = pd.read_csv(os.path.join(base_dir, '../y_train.csv'))

# Assurez-vous que y_train est un tableau 1D
y_train = y_train.values.ravel()

# Créer et entraîner le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train[['authorization_number', 'amount', 'status_encoded', 'reason_encoded']], y_train)

# Sauvegarder le modèle entraîné
joblib.dump(model, 'chargeback_resolution_model_lr.pkl')
