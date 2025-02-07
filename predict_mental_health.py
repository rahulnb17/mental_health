# -*- coding: utf-8 -*-
"""predict_mental_health.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IqyJoGE2ymo3UIHM6TpLSLJUGOEsAQzk
"""

import os
import shutil

# Create .kaggle directory if it doesn't exist
os.makedirs("/root/.kaggle", exist_ok=True)

# Move kaggle.json to the correct directory
shutil.move("/content/kaggle.json", "/root/.kaggle/kaggle.json")

# Set permissions to secure the file
os.chmod("/root/.kaggle/kaggle.json", 600)

# Verify by listing datasets
!kaggle datasets list | head -n 10

!pip install -q kaggle

# Verify Kaggle authentication
!kaggle datasets list | head -n 10

!kaggle datasets download -d shahzadahmad0402/depression-and-anxiety-data

import zipfile

# Unzip the downloaded file
!unzip -q depression-and-anxiety-data.zip

import os

# List all files in the current directory
os.listdir()

import pandas as pd

# Replace 'your_file.csv' with the actual CSV filename
df = pd.read_csv("depression_anxiety_data.csv")

# Display first 5 rows
df.head()

# Get dataset information
df.info()

# Check missing values
df.isnull().sum()

# Fill missing categorical values with mode
categorical_cols = ['depression_severity', 'depressiveness', 'suicidal',
                    'depression_diagnosis', 'depression_treatment', 'anxiousness',
                    'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']

for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Fill missing categorical values with mode
categorical_cols = ['depression_severity', 'depressiveness', 'suicidal',
                    'depression_diagnosis', 'depression_treatment', 'anxiousness',
                    'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']

df[categorical_cols] = df[categorical_cols].apply(lambda x: x.fillna(x.mode()[0]))

# Fill missing numerical values with median
numerical_cols = ['epworth_score']
df[numerical_cols] = df[numerical_cols].apply(lambda x: x.fillna(x.median()))

# Check if any missing values remain
print(df.isnull().sum())

# Normalize text columns: convert to lowercase and strip spaces
text_cols = ['gender', 'who_bmi', 'depression_severity', 'depressiveness',
             'suicidal', 'depression_diagnosis', 'depression_treatment',
             'anxiety_severity', 'anxiousness', 'anxiety_diagnosis',
             'anxiety_treatment', 'sleepiness']

df[text_cols] = df[text_cols].apply(lambda x: x.str.lower().str.strip())

# Convert non-string values to string and fill NaN values with 'unknown'
df[text_cols] = df[text_cols].apply(lambda x: x.fillna('unknown').astype(str).str.lower().str.strip())

# Check unique values for categorical columns
for col in text_cols:
    print(f"{col}: {df[col].unique()}")

# Binary encoding for boolean columns
boolean_cols = ['depressiveness', 'suicidal', 'depression_diagnosis',
                'depression_treatment', 'anxiousness', 'anxiety_diagnosis',
                'anxiety_treatment', 'sleepiness']

df[boolean_cols] = df[boolean_cols].apply(lambda x: x.map({'false': 0, 'true': 1}))

# Mapping ordinal columns to integers based on severity
bmi_mapping = {
    'underweight': 1,
    'normal': 2,
    'overweight': 3,
    'class i obesity': 4,
    'class ii obesity': 5,
    'class iii obesity': 6,
    'not availble': 0  # Treat 'not available' as 0
}

severity_mapping = {
    'none-minimal': 0,
    'mild': 1,
    'moderate': 2,
    'moderately severe': 3,
    'severe': 4
}

# Apply the mappings
df['who_bmi'] = df['who_bmi'].map(bmi_mapping)
df['depression_severity'] = df['depression_severity'].map(severity_mapping)
df['anxiety_severity'] = df['anxiety_severity'].map(severity_mapping)

# Correlation matrix for numerical features
import seaborn as sns
import matplotlib.pyplot as plt

# Select numerical columns for correlation matrix
numerical_cols = ['age', 'bmi', 'phq_score', 'gad_score', 'epworth_score']

# Calculate correlation matrix
correlation_matrix = df[numerical_cols].corr()

# Plot heatmap of correlations
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

from sklearn.feature_selection import chi2
from sklearn.preprocessing import LabelEncoder

# Convert categorical target column to numeric (0/1 for binary classification)
label_encoder = LabelEncoder()
df['depression_diagnosis'] = label_encoder.fit_transform(df['depression_diagnosis'])

# Convert categorical features into numeric using LabelEncoder
categorical_cols = ['gender', 'who_bmi', 'depression_severity', 'depressiveness',
                    'suicidal', 'depression_treatment', 'anxiety_severity',
                    'anxiousness', 'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']

for col in categorical_cols:
    df[col] = label_encoder.fit_transform(df[col])

# Create feature matrix X and target vector y
X = df[categorical_cols]
y = df['depression_diagnosis']

# Apply chi-square test
chi2_values, p_values = chi2(X, y)

# Display results
chi2_results = pd.DataFrame({
    'Feature': categorical_cols,
    'Chi2 Value': chi2_values,
    'P Value': p_values
})

print(chi2_results)

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Summary Statistics for Numerical Data
print("Summary Statistics for Numerical Columns")
print(df.describe())

# 2. Distribution of Numerical Columns (e.g., age, BMI, scores)
numerical_cols = ['age', 'bmi', 'phq_score', 'gad_score', 'epworth_score']
plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[col], kde=True)
    plt.title(f'{col} Distribution')
plt.tight_layout()
plt.show()

# 3. Distribution of Categorical Data using Bar Plots
categorical_cols = ['gender', 'who_bmi', 'depression_severity', 'depressiveness',
                    'suicidal', 'depression_treatment', 'anxiety_severity',
                    'anxiousness', 'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']

plt.figure(figsize=(15, 12))
for i, col in enumerate(categorical_cols, 1):
    plt.subplot(3, 4, i)
    sns.countplot(x=df[col])
    plt.title(f'{col} Count Plot')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Correlation Heatmap for Numerical Features
correlation_matrix = df[numerical_cols].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Correlation Heatmap for Numerical Features")
plt.show()

# 5. Pairplot for Numerical Features (for relationship analysis)
sns.pairplot(df[numerical_cols])
plt.suptitle("Pairwise Relationships Between Numerical Features", y=1.02)
plt.show()

# 6. Investigating Relationships Between Features (Depression Diagnosis vs. Other Features)
plt.figure(figsize=(15, 8))
sns.countplot(x='depression_diagnosis', hue='gender', data=df)
plt.title('Depression Diagnosis vs Gender')
plt.show()

# Visualize relationship between depression severity and other features
plt.figure(figsize=(15, 8))
sns.countplot(x='depression_severity', hue='anxiety_severity', data=df)
plt.title('Depression Severity vs Anxiety Severity')
plt.show()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("depression_anxiety_data.csv")

# Encode categorical features
categorical_cols = ['gender', 'who_bmi', 'depression_severity', 'depressiveness',
                    'suicidal', 'depression_treatment', 'anxiety_severity',
                    'anxiousness', 'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders for later use

# Define target variable
target = 'depression_diagnosis'  # You can change this to another mental health condition
df[target] = LabelEncoder().fit_transform(df[target])

# Split dataset
X = df.drop(columns=['id', target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# Train Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

# Train XGBoost Model
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)

# Evaluate Models
print("Random Forest Results:")
print(classification_report(y_test, rf_preds))
print("ROC-AUC:", roc_auc_score(y_test, rf_model.predict_proba(X_test), multi_class='ovr'))

print("\nXGBoost Results:")
print(classification_report(y_test, xgb_preds))
print("ROC-AUC:", roc_auc_score(y_test, xgb_model.predict_proba(X_test), multi_class='ovr'))

from sklearn.preprocessing import label_binarize

# Binarize the labels for multi-class ROC-AUC calculation
y_test_binarized = label_binarize(y_test, classes=np.unique(y_train))

# Evaluate Models
print("Random Forest Results:")
print(classification_report(y_test, rf_preds))
print("ROC-AUC:", roc_auc_score(y_test_binarized, rf_model.predict_proba(X_test), multi_class='ovr'))

print("\nXGBoost Results:")
print(classification_report(y_test, xgb_preds))
print("ROC-AUC:", roc_auc_score(y_test_binarized, xgb_model.predict_proba(X_test), multi_class='ovr'))

pip install shap

import shap

# Create SHAP Explainer
explainer = shap.TreeExplainer(rf_model)
shap_values = explainer.shap_values(X_test)

# Plot Summary
shap.summary_plot(shap_values, X_test)

import joblib

# Save the model
joblib.dump(rf_model, "mental_health_rf_model.pkl")

import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load("mental_health_rf_model.pkl")

def predict_mental_health(symptoms):
    """
    Predict mental health condition based on input symptoms.

    Args:
        symptoms (list): A list of symptom values corresponding to model features.

    Returns:
        int: Predicted mental health condition (e.g., 0 = No diagnosis, 1 = Depression).
    """
    # Convert input to numpy array and reshape for model
    symptoms_array = np.array(symptoms).reshape(1, -1)

    # Make prediction
    prediction = model.predict(symptoms_array)

    return int(prediction[0])  # Convert numpy int to Python int

if __name__ == "__main__":
    # Example input (adjust according to your dataset's feature format)
    example_input = [0.5, 1, 3, 2, 0, 1]  # Replace with real feature values
    result = predict_mental_health(example_input)
    print(f"Predicted Mental Health Condition: {result}")

def predict_mental_health(symptoms):
    if len(symptoms) != 17:
        raise ValueError(f"Expected 17 features, but got {len(symptoms)}")

    symptoms_array = np.array(symptoms).reshape(1, -1)
    prediction = model.predict(symptoms_array)

    return int(prediction[0])

print(f"Model was trained on {rf_model.n_features_in_} features.")

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

# Ensure y is 1D and merge rare class (if applicable)
y = np.ravel(y)  # Flatten the target variable if it's a 2D array

y = np.where(y == 2, 1, y)  # Convert class 2 → class 1

# Train-Test Split with Stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training feature shape: {X_train.shape}")  # Ensure X_train has the correct feature count

# ✅ Train Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)
rf_probs = rf_model.predict_proba(X_test)

# ✅ Train XGBoost Model
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
xgb_probs = xgb_model.predict_proba(X_test)

# ✅ Evaluate Models
print("Random Forest Results:")
print(classification_report(y_test, rf_preds))
if len(np.unique(y_test)) > 1:
    print("ROC-AUC:", roc_auc_score(y_test, rf_probs[:, 1]))  # Fix: Ensure more than one class exists

print("\nXGBoost Results:")
print(classification_report(y_test, xgb_preds))
if len(np.unique(y_test)) > 1:
    print("ROC-AUC:", roc_auc_score(y_test, xgb_probs[:, 1]))  # Fix: Ensure more than one class exists

import joblib

# Save the trained Random Forest model
joblib.dump(rf_model, 'rf_model.pkl')

# Save the trained XGBoost model
joblib.dump(xgb_model, 'xgb_model.pkl')

import shap

# SHAP for Random Forest Model
explainer_rf = shap.TreeExplainer(rf_model)
shap_values_rf = explainer_rf.shap_values(X_test)

# SHAP for XGBoost Model
explainer_xgb = shap.TreeExplainer(xgb_model)
shap_values_xgb = explainer_xgb.shap_values(X_test)

# Visualizing SHAP summary for Random Forest Model
shap.summary_plot(shap_values_rf, X_test)

# Visualizing SHAP summary for XGBoost Model
shap.summary_plot(shap_values_xgb, X_test)

"""Inference Script"""

import pandas as pd
import joblib

# Load the trained Random Forest model
rf_model = joblib.load('rf_model.pkl')

def predict_mental_health(symptom_data):
    """
    Function to predict mental health diagnosis based on symptom data.
    :param symptom_data: pandas DataFrame, should match the features used during training.
    :return: predicted class
    """
    # Ensure symptom_data is in the correct format (it must be a DataFrame)
    prediction = rf_model.predict(symptom_data)  # Or use xgb_model.predict(symptom_data)
    return prediction

# Example usage:
# Prepare some sample new data with the correct features
new_data = pd.DataFrame({
    'age': [30],  # Example: Age of the person
    'school_year': [2],  # Example: School year (1-12)
    'gender': [1],  # Example: 1 for male, 0 for female (or other encoding)
    'bmi': [23],  # Example: BMI value
    'who_bmi': ['Normal'],  # Example: WHO BMI classification ('Normal', 'Overweight', etc.)
    'phq_score': [12],  # Example: PHQ score (for depression screening)
    'depression_severity': [2],  # Example: Depression severity (1-5 scale)
    'depressiveness': [3],  # Example: Level of depressiveness (1-5 scale)
    'suicidal': [1],  # Example: 1 for suicidal thoughts, 0 for no
    'depression_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'gad_score': [10],  # Example: GAD score (for anxiety)
    'anxiety_severity': [3],  # Example: Anxiety severity (1-5 scale)
    'anxiousness': [4],  # Example: Level of anxiousness (1-5 scale)
    'anxiety_diagnosis': [1],  # Example: 1 for diagnosed with anxiety, 0 for not
    'anxiety_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'epworth_score': [9],  # Example: Epworth score for sleepiness
    'sleepiness': [3],  # Example: Sleepiness level (1-5 scale)
})
# Make the prediction
prediction = predict_mental_health(new_data)
print(f"Predicted mental health diagnosis: {prediction}")

# Assuming X_train is your training data
print(X_train.columns)

# Assuming you have used RandomForestClassifier
# Get the feature order from the trained model
feature_order = X_train.columns  # X_train is the training dataset

# Now ensure new_data has columns in the same order
new_data = new_data[feature_order]

Infernce Script Results

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the trained Random Forest model
rf_model = joblib.load('rf_model.pkl')

# Define the exact feature order used during training
feature_order = [
    'school_year', 'age', 'gender', 'bmi', 'who_bmi', 'phq_score',
    'depression_severity', 'depressiveness', 'suicidal', 'depression_treatment',
    'gad_score', 'anxiety_severity', 'anxiousness', 'anxiety_diagnosis',
    'anxiety_treatment', 'epworth_score', 'sleepiness'
]

# Example of new symptom data (ensure the data has the same features in the same order)
new_data = pd.DataFrame({
    'school_year': [2],  # Example: Year in school
    'age': [30],  # Example: Age of the person
    'gender': [1],  # Example: 1 for male, 0 for female
    'bmi': [23],  # Example: BMI value
    'who_bmi': ['Normal'],  # Example: WHO BMI category (categorical)
    'phq_score': [12],  # Example: PHQ score
    'depression_severity': [2],  # Example: Depression severity level
    'depressiveness': [3],  # Example: Level of depressiveness
    'suicidal': [1],  # Example: 1 for suicidal thoughts, 0 for no suicidal thoughts
    'depression_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'gad_score': [10],  # Example: GAD score
    'anxiety_severity': [3],  # Example: Anxiety severity level
    'anxiousness': [4],  # Example: Level of anxiousness
    'anxiety_diagnosis': [1],  # Example: 1 for diagnosed, 0 for not diagnosed
    'anxiety_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'epworth_score': [9],  # Example: Epworth score
    'sleepiness': [3],  # Example: Sleepiness level
})

# Initialize label encoder for 'who_bmi'
label_encoder = LabelEncoder()

# Fit and transform 'who_bmi' column to convert categorical string to numeric values
new_data['who_bmi'] = label_encoder.fit_transform(new_data['who_bmi'])

# Ensure the new data has the columns in the correct order, as the model expects
new_data = new_data[feature_order]

# Make the prediction using the trained Random Forest model
prediction = rf_model.predict(new_data)

# Output the prediction result
print(f"Predicted mental health diagnosis: {prediction[0]}")

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the trained Random Forest model
rf_model = joblib.load('xgb_model.pkl')

# Define the exact feature order used during training
feature_order = [
    'school_year', 'age', 'gender', 'bmi', 'who_bmi', 'phq_score',
    'depression_severity', 'depressiveness', 'suicidal', 'depression_treatment',
    'gad_score', 'anxiety_severity', 'anxiousness', 'anxiety_diagnosis',
    'anxiety_treatment', 'epworth_score', 'sleepiness'
]

# Example of new symptom data (ensure the data has the same features in the same order)
new_data = pd.DataFrame({
    'school_year': [2],  # Example: Year in school
    'age': [30],  # Example: Age of the person
    'gender': [1],  # Example: 1 for male, 0 for female
    'bmi': [23],  # Example: BMI value
    'who_bmi': ['Normal'],  # Example: WHO BMI category (categorical)
    'phq_score': [12],  # Example: PHQ score
    'depression_severity': [2],  # Example: Depression severity level
    'depressiveness': [3],  # Example: Level of depressiveness
    'suicidal': [1],  # Example: 1 for suicidal thoughts, 0 for no suicidal thoughts
    'depression_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'gad_score': [10],  # Example: GAD score
    'anxiety_severity': [3],  # Example: Anxiety severity level
    'anxiousness': [4],  # Example: Level of anxiousness
    'anxiety_diagnosis': [1],  # Example: 1 for diagnosed, 0 for not diagnosed
    'anxiety_treatment': [1],  # Example: 1 for treatment, 0 for no treatment
    'epworth_score': [9],  # Example: Epworth score
    'sleepiness': [3],  # Example: Sleepiness level
})

# Initialize label encoder for 'who_bmi'
label_encoder = LabelEncoder()

# Fit and transform 'who_bmi' column to convert categorical string to numeric values
new_data['who_bmi'] = label_encoder.fit_transform(new_data['who_bmi'])

# Ensure the new data has the columns in the correct order, as the model expects
new_data = new_data[feature_order]

# Make the prediction using the trained Random Forest model
prediction = rf_model.predict(new_data)

# Output the prediction result
print(f"Predicted mental health diagnosis: {prediction[0]}")

"""1 is for depression and 0 is for no diagnosis"""