import pandas as pd

# Correct data with matching lengths
data = {
    "HexData": [
        "4D5A90000300000004000000", "89504E470D0A1A0A0000000D", "FFD8FFE000104A4649460001",
        "255044462D312E350D0A25E2", "504B0304140000000800B7AC", "424D3E000000000000003E00",
        "7F454C460101010000000000", "47494638396126002600F7", "000001BA2100010001801194",
        "526172211A0700CF9073", "49492A0008000000E8030000", "1F8B0800000000000003",
        "435753050000000000000000", "3C21444F435459504520", "4D546864000000060001",
        "3026B2758E66CF11A6D900AA", "4F6767530002000000000000", "524946464645524D00000000",
        "89504E470D0A1A0A0000000D", "FFD8FFE000104A4649460001", "504B0304140000000800B7AC",
        "BADC0FFEE0D1A2200BC25A6", "1234567890ABCDEF", "ABCDEF1234567890"
    ],
    "Category": [
        "exe", "PNG", "JPG", "PDF", "ZIP", "BMP", "ELF", "GIF", "MPEG", "RAR", 
        "JPEG2000", "GZIP", "SWF", "HTML", "MIDI", "WMV", "OGG", "WAV", "DOC", "PNG", 
        "JPG", "ZIP", "XML", "MP4"
    ]
}

# Check lengths of both lists
print("Length of HexData:", len(data['HexData']))
print("Length of Category:", len(data['Category']))

# Create DataFrame if lengths match
if len(data['HexData']) == len(data['Category']):
    df = pd.DataFrame(data)
    df.to_csv('file_data.csv', index=False)
    print("file_data.csv created successfully.")
else:
    print("Error: The lengths of HexData and Category do not match.")
