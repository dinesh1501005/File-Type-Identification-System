import pandas as pd

# Sample data to add (various file types and their magic bytes)
data_to_add = [
    {'Filename': 'file1.exe', 'MagicBytes': '4d5a900003000000040000000000000000000000000000000000000000000000'},
    {'Filename': 'file2.zip', 'MagicBytes': '504b030414000800080000002d5e8c25000000000000000000000000000000'},
    {'Filename': 'file3.pdf', 'MagicBytes': '255044462d312e350d0a25e2e3cfdf5a6e2ec02080c2e'},
    {'Filename': 'file4.jpg', 'MagicBytes': 'ffd8ffe000104a464946000101010060006800060000ffdb0043000201010302020203030404030506040805060806070709070709090a0a'},
    {'Filename': 'file5.png', 'MagicBytes': '89504e470d0a1a0a0000000d49484452000000150000000f0802000000a1b0b7a70000000467414d410000b18f0c0200000049454e44ae426082'},
    {'Filename': 'file6.mp3', 'MagicBytes': '4944330300000000212d8f0100001c00d44c11007d46f90556f7d91316d61c01f470a4'},
    {'Filename': 'file7.docx', 'MagicBytes': '504b030414000600080000002d5e8c25000000000000000000000000000000'},
    {'Filename': 'file8.html', 'MagicBytes': '3c21444f4354595045202d2d0d0a3c68746d6c3e0d0a3c7469746c653e'},
    {'Filename': 'file9.rar', 'MagicBytes': '526172211a0700cf9073fcbf9cbd7404b050909f0'},
    {'Filename': 'file10.tar', 'MagicBytes': '7573746172000000000000000000000000000000000000000000000000000000'}
]


# Convert the data to a DataFrame
new_data_df = pd.DataFrame(data_to_add)

# Append the new data to the existing CSV file
new_data_df.to_csv('file_hex_data.csv', mode='a', header=False, index=False)

print("Data added successfully to the CSV file.")
