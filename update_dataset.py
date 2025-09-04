import pandas as pd

# Load hex data
hex_data = pd.read_csv('file_hex_data.csv')

# Load label mapping
labels = pd.read_csv('dataset_labels.csv')

# Debug: Print column names
print("Hex Data Columns:", hex_data.columns)
print("Labels Columns:", labels.columns)

# Ensure column names match
labels.columns = labels.columns.str.strip()  # Remove hidden spaces
labels.rename(columns={'filename': 'Filename'}, inplace=True)  # Rename if needed

# Merge datasets
merged_data = hex_data.merge(labels, on='Filename', how='left')

# Save updated dataset
merged_data.to_csv('updated_dataset.csv', index=False)

print("Dataset updated successfully!")
