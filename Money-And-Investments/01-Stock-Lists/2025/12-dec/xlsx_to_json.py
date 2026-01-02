import pandas as pd

# Load the Excel file
file_path = 'path_to_your_file/NBFCsandARCs10012023.XLSX'

# Read each sheet
nbfc_data = pd.read_excel(file_path, sheet_name='NBFCs')  # replace with actual sheet name
arc_data = pd.read_excel(file_path, sheet_name='ARCs')    # replace with actual sheet name

# Convert to JSON
nbfc_json = nbfc_data.to_json(orient='records')
arc_json = arc_data.to_json(orient='records')

# Save to JSON files
with open('NBFCs.json', 'w') as nbfc_file:
    nbfc_file.write(nbfc_json)

with open('ARCs.json', 'w') as arc_file:
    arc_file.write(arc_json)
