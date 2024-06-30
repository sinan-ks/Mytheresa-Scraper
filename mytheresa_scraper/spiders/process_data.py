# import csv
# import json

# # Load the scraped data from the JSON file
# with open('mytheresa_shoes_data.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # CSV headers 
# headers = ["Sl. No", "Field Name", "Field Type", "Example"]

# # The field names and types
# fields = [
#     ("1", "breadcrumbs", "list"),
#     ("2", "image_url", "string"),
#     ("3", "brand", "string"),
#     ("4", "product_name", "string"),
#     ("5", "listing_price", "string"),
#     ("6", "offer_price", "string"),
#     ("7", "discount", "string"),
#     ("8", "product_id", "string"),
#     ("9", "sizes", "list"),
#     ("10", "description", "string"),
#     ("11", "other_images", "list")
# ]

# # Open the CSV file for writing
# with open('mytheresa_shoes_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write the header
#     writer.writerow(headers)
    
#     # Write the data rows
#     for field in fields:
#         sl_no, field_name, field_type = field
#         example_value = data[0][field_name] if field_name in data[0] else ""
#         writer.writerow([sl_no, field_name, field_type, json.dumps(example_value) if isinstance(example_value, list) else example_value])
