import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv('weather_history_month.csv')

# Convert timestamp to datetime for potential feature engineering
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Feature engineering example:
# Extract hour and day of week which might affect weather patterns
df['hour'] = df['datetime'].dt.hour
df['dayofweek'] = df['datetime'].dt.dayofweek

# Define features and target
# Label 1 for heavy rain (502), 0 for everything else
df['storm'] = df['weather_code'].apply(lambda x: 1 if x == 502 else 0)

features = ['temp', 'pressure', 'humidity', 'wind_speed', 'hour', 'dayofweek']
X = df[features]
y = df['storm']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))


# Save model
joblib.dump(model, 'storm_rf_model.joblib')
print("Model saved as storm_rf_model.joblib")
print("Train storm distribution:\n", y_train.value_counts())
print("Test storm distribution:\n", y_test.value_counts())
print(df['storm'].value_counts())