import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from joblib import dump

# Step 1: Load the dataset
df = pd.read_csv('hex_data.csv')  # Make sure hex_data.csv is in the same directory
print("Original data head:\n", df.head())

# Step 2: Print initial class distribution
initial_counts = df['Category'].value_counts()
print("Initial class distribution:")
print(initial_counts)

# Step 3: Filter out classes with fewer than 2 samples (since SMOTE requires at least 2)
classes_with_enough_samples = initial_counts[initial_counts >= 2].index
df_filtered = df[df['Category'].isin(classes_with_enough_samples)]
print("\nClass distribution after filtering:")
print(df_filtered['Category'].value_counts())

# Step 4: Convert HexData to a list of integers
def hex_to_int_list(hex_str):
    try:
        # Convert the hex string into a list of integers (2 characters per byte)
        return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    except ValueError:
        print(f"Error converting hex string: {hex_str}")
        return []  # Return an empty list if conversion fails

# Apply the conversion and print some results for debugging
X_series = df_filtered['HexData'].apply(hex_to_int_list)
print("\nConverted HexData (first 5 entries):")
print(X_series.head())

# Step 5: Convert the list of integers into a DataFrame and pad sequences to fixed length
max_length = max(X_series.apply(len))
X_df = pd.DataFrame([np.pad(x, (0, max_length - len(x)), 'constant') for x in X_series])
print("\nPadded HexData head:")
print(X_df.head())

# Step 6: Handle missing values (if any)
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X_df)

# Step 7: Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Step 8: Encode category labels
y = df_filtered['Category']
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Step 9: Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Step 10: Check training set class distribution
train_class_counts = pd.Series(y_train).value_counts()
print("\nTraining set class distribution:")
print(train_class_counts)

# Step 11: Decide whether to apply SMOTE
if train_class_counts.min() < 2:
    print("\nNot enough samples in one or more classes for SMOTE. Skipping SMOTE.")
    X_resampled, y_resampled = X_train, y_train
else:
    # Dynamically set k_neighbors to be less than or equal to the smallest class sample count - 1
    k_neighbors = min(5, train_class_counts.min() - 1)
    print(f"\nUsing {k_neighbors} neighbors for SMOTE.")
    smote = SMOTE(sampling_strategy='auto', k_neighbors=k_neighbors, random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Step 12: Train the model using Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_resampled, y_resampled)

# Step 13: Evaluate the model on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'\nModel Accuracy: {accuracy * 100:.2f}%')

# Step 14: Save the model, label encoder, and scaler for later use
dump(model, 'file_type_model.joblib')
dump(label_encoder, 'label_encoder.joblib')
dump(scaler, 'scaler.joblib')
print("\nModel, Label Encoder, and Scaler saved successfully.")
