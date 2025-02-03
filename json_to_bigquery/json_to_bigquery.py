
import json
from google.cloud import bigquery

# Load schema mappings
with open("schemas.json", "r") as f:
    SCHEMA_MAP = json.load(f)

client = bigquery.Client()

def get_object_type(json_obj):
    """Determine the object type based on a field or external logic."""
    return json_obj.get("type")  # Assuming JSON has a "type" field

def load_schema(object_type):
    """Fetch the schema and table name dynamically."""
    if object_type in SCHEMA_MAP:
        return SCHEMA_MAP[object_type]["table"], SCHEMA_MAP[object_type]["schema"]
    else:
        raise ValueError(f"Unknown object type: {object_type}")

def map_json_to_schema(json_obj, schema):
    """Map JSON keys to the correct schema fields, checking for required fields."""
    mapped_data = {}
    
    for field in schema:
        field_name = field["name"]
        required = field.get("required", False)
        field_type = field["type"]

        value = json_obj.get(field_name)

        # Handle missing required fields
        if required and value is None:
            raise ValueError(f"Mandatory field '{field_name}' is missing")
        
        # Assign default value for optional fields if missing
        if value is None:
            if field_type == "STRING":
                value = ""  # Default empty string for missing optional strings
            elif field_type == "TIMESTAMP":
                value = "1970-01-01T00:00:00Z"  # Default timestamp
            else:
                value = None  # For other types, you may handle defaults differently

        mapped_data[field_name] = value

    return mapped_data

def process_json(json_str):
    """Parse JSON, load schema, and insert into BigQuery."""
    json_obj = json.loads(json_str)
    object_type = get_object_type(json_obj)
    
    table_id, schema = load_schema(object_type)
    mapped_data = map_json_to_schema(json_obj, schema)

    # Insert into BigQuery
    errors = client.insert_rows_json(table_id, [mapped_data])
    if errors:
        print("BigQuery Insert Error:", errors)
    else:
        print(f"Inserted into {table_id}: {mapped_data}")

# Example JSON input (simulate gRPC response)
json_input = '{"type": "user", "user_id": "123", "name": "Alice", "email": "alice@example.com", "signup_date": "2025-02-03T10:00:00Z"}'
process_json(json_input)
