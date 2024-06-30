import csv
import json

# Load the scraped data from the JSON file
with open('mytheresa_shoes_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The CSV headers based on the required format
headers = ["Sl. No", "Field Name", "Field Type", "Data"]

# The field names and types
fields = [
    ("1", "breadcrumbs", "list"),
    ("2", "image_url", "string"),
    ("3", "brand", "string"),
    ("4", "product_name", "string"),
    ("5", "listing_price", "string"),
    ("6", "offer_price", "string"),
    ("7", "discount", "string"),
    ("8", "product_id", "string"),
    ("9", "sizes", "list"),
    ("10", "description", "string"),
    ("11", "other_images", "list")
]

# Open the CSV file for writing
with open('mytheresa_shoes_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(headers)
    
    # Write the actual data rows
    for item in data:
        for sl_no, field_name, field_type in fields:
            value = item.get(field_name, "")
            if isinstance(value, list):
                value = json.dumps(value)  # Convert list to string
            writer.writerow([sl_no, field_name, field_type, value])
    
        # Add a blank line after each product set
        writer.writerow([])  

