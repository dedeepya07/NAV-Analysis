import json
import gzip

# Initialize dictionaries
scheme_code_to_name = {}
scheme_code_to_nav = {}

# Read the data from the extracted text file
with open('nav_data.txt', 'r') as file:
    lines = file.readlines()

# Process each line
for line in lines:
    # Split the line by semicolons
    parts = line.strip().split(';')
    
    # Ensure the line has the correct format and skip headers or invalid lines
    if len(parts) >= 7 and parts[0] != 'Scheme Code':
        scheme_code = parts[0].strip()
        scheme_name = parts[1].strip()
        nav_value = parts[4].strip()
        date = parts[7].strip() if len(parts) > 7 else None
        
        # Skip lines where NAV value is not a valid float
        try:
            nav_value = float(nav_value)
        except ValueError:
            continue  # Skip this line if NAV value is not a number
        
        # Add to scheme_code_to_name dictionary
        scheme_code_to_name[scheme_code] = scheme_name
        
        # Add to scheme_code_to_nav dictionary
        if scheme_code not in scheme_code_to_nav:
            scheme_code_to_nav[scheme_code] = {}
        if date:
            scheme_code_to_nav[scheme_code][date] = nav_value

# Write the scheme_code_to_name mapping to a JSON file (for reference)
with open('scheme_code_to_name.json', 'w') as outfile:
    json.dump(scheme_code_to_name, outfile, indent=4)

# Write the scheme_code_to_nav mapping to a compressed JSON file
with gzip.open('scheme_code_to_nav.json.gz', 'wt', encoding="utf-8") as outfile:
    json.dump(scheme_code_to_nav, outfile)

print("Compressed JSON file generated successfully!")