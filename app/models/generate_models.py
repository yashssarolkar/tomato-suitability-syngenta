import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import joblib

# Load the dataset
file_path = 'Tomata Cultivation Suitability Dataset.xlsx'  # Adjust to your local path
data = pd.read_excel(file_path)

# Column mapping for consistency
column_mapping = {
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Altitude (m)": "altitude",
    "Temp (°C)": "temperature",
    "Rainfall (mm)": "rainfall",
    "Humidity (%)": "humidity",
    "Sunlight (hrs/day)": "sunlight",
    "Soil Type": "soil_type",
    "pH": "pH",
    "N (mg/kg)": "N",
    "P (mg/kg)": "P",
    "K (mg/kg)": "K",
    "Org Carbon (%)": "organic_carbon",
    "Region": "region",
    "Variety": "variety",
    "Season": "season",
    "Suitability Score": "suitability_score",
    "Suitability Label": "suitability_label",
    "Expected Yield (tons/ha)": "expected_yield",
}

# Rename dataset columns using the mapping
data = data.rename(columns=column_mapping)

# Drop rows where Suitability Label is 'Moderate'
data = data[data['suitability_label'] != 'Moderate']

# Separate features and target variables
features = data.drop(['suitability_score', 'suitability_label', 'expected_yield'], axis=1)
targets = data[['suitability_score', 'suitability_label', 'expected_yield']]

# Encode categorical variables
categorical_columns = ['region', 'soil_type', 'variety', 'season']
features = pd.get_dummies(features, columns=categorical_columns)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# Split targets for different models
y_train_score = y_train['suitability_score']
y_train_label = y_train['suitability_label']
y_train_yield = y_train['expected_yield']

# Train Suitability Score Model
print("Training Suitability Score Model...")
score_model = lgb.LGBMRegressor(random_state=42)
score_model.fit(X_train, y_train_score)

# Train Suitability Label Model
print("Training Suitability Label Model...")
label_model = lgb.LGBMClassifier(random_state=42)
label_model.fit(X_train, y_train_label)

# Train Expected Yield Model
print("Training Expected Yield Model...")
yield_model = lgb.LGBMRegressor(random_state=42)
yield_model.fit(X_train, y_train_yield)

# Save models to the 'models/' directory
joblib.dump(score_model, 'suitability_score_model.pkl')
joblib.dump(label_model, 'suitability_label_model.pkl')
joblib.dump(yield_model, 'expected_yield_model.pkl')

print("Models saved successfully in the 'models/' directory!")
