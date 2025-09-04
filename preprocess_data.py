import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('file_hex_data.csv')

# Convert hex values into numerical data
def hex_to_int(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

df['MagicBytes'] = df['MagicBytes'].apply(hex_to_int)

# Pad or truncate each list to a fixed length (e.g., first 16 bytes)
max_length = 16
df['MagicBytes'] = df['MagicBytes'].apply(lambda x: x[:max_length] + [0] * (max_length - len(x)) if len(x) < max_length else x)

# Convert list into separate columns
hex_features = pd.DataFrame(df['MagicBytes'].to_list())

# Encode file types as labels
df['Label'] = df['Filename'].apply(lambda x: x.split('.')[-1])  # Extract extension as label
label_encoder = LabelEncoder()
df['Label'] = label_encoder.fit_transform(df['Label'])

# Split the data
X = hex_features
y = df['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save processed data
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("Data preprocessing complete. Files saved: X_train.csv, X_test.csv, y_train.csv, y_test.csv.")
