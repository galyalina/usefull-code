
# JSON to BigQuery Data Loader

This project allows you to dynamically parse JSON data, map it to BigQuery schemas, and insert it into the appropriate tables. 
The fields in the JSON are mapped to the schema dynamically, with support for both **mandatory** and **optional** fields.

## Steps to Run

1. **Install Dependencies**: Install the required Python packages.

   ```bash
   pip install google-cloud-bigquery
   ```

2. **Configure Google Cloud Authentication**: Set up your Google Cloud credentials.

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
   ```

3. **Prepare the JSON Schema**: Define your schema in `schemas.json` as shown below.

   Example `schemas.json`:
   ```json
   {
     "user": {
       "table": "my_dataset.users",
       "schema": [
         {"name": "user_id", "type": "STRING", "required": true},
         {"name": "name", "type": "STRING", "required": true},
         {"name": "email", "type": "STRING", "required": false},
         {"name": "signup_date", "type": "TIMESTAMP", "required": true},
         {"name": "location_id", "type": "STRING", "required": false}
       ]
     },
     "location": {
       "table": "my_dataset.locations",
       "schema": [
         {"name": "location_id", "type": "STRING", "required": true},
         {"name": "city", "type": "STRING", "required": true},
         {"name": "country", "type": "STRING", "required": false}
       ]
     }
   }
   ```

4. **Run the Script**: Execute the script to process a JSON input and insert the data into BigQuery.

   Example JSON input (simulate gRPC response):
   ```json
   {"type": "user", "user_id": "123", "name": "Alice", "email": "alice@example.com", "signup_date": "2025-02-03T10:00:00Z"}
   ```

   ```bash
   python json_to_bigquery.py
   ```

5. **Check BigQuery**: After running the script, the data will be inserted into the corresponding BigQuery table.

## Notes
- The script will check for missing mandatory fields and raise an error if any are missing.
- Optional fields are filled with default values when they are missing in the input JSON.
