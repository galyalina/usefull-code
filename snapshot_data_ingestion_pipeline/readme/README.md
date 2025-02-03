
# Data Ingestion Pipeline for Snapshot Data

This Dataflow pipeline is responsible for ingesting snapshot data into BigQuery. The data is streamed from Pub/Sub, and each record is added to BigQuery with an associated `snapshot_id`. There are no deletion or reconciliation operations in this pipeline.

## Architecture Overview

- **Dataflow**: Ingests data from a gRPC stream (via Pub/Sub) and writes it into BigQuery.
- **BigQuery**: Stores data records with a `snapshot_id` to keep track of snapshots.
  
## BigQuery Schema

| Column               | Type         |
|----------------------|--------------|
| `snapshot_id`        | STRING       |
| `data_field`         | STRING       |
| `deleted`            | BOOLEAN      |
| `deleted_snapshot_id`| STRING       |
| `timestamp`          | TIMESTAMP    |

### Steps for Data Ingestion

1. **Dataflow Pipeline**:
   - The pipeline listens for stream data from **Pub/Sub**.
   - It processes the records and writes them into BigQuery, keeping the `snapshot_id` and marking the `deleted` flag as `false`.

2. **Pub/Sub**:
   - A gRPC stream publishes messages to Pub/Sub, which are consumed by the Dataflow pipeline.

### Running the Pipeline

1. Set up the **gRPC client** to stream data into **Pub/Sub**.
2. Deploy the **Dataflow pipeline** to Google Cloud.
3. Ensure the appropriate IAM roles are granted for Dataflow, BigQuery, and Pub/Sub access.

## Configuration

- **BigQuery Table**: `your_project:your_dataset.your_table`
- **Pub/Sub Subscription**: `projects/your-project/subscriptions/your-subscription`

## Development and Deployment

1. Compile and deploy the **Dataflow pipeline** using the Google Cloud SDK.
2. Verify that **Pub/Sub** is correctly receiving and passing messages from the gRPC stream.
3. Monitor Dataflow job execution for performance.

## Troubleshooting

- Check Dataflow logs for any issues with data streaming or processing.
- Verify that the **BigQuery table schema** is aligned with the data being processed.
