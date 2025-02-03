# Cloud Composer DAG for Snapshot Data Reconciliation

This Cloud Composer DAG handles the reconciliation of snapshot data in BigQuery. It compares incoming snapshot data and updates records in BigQuery that are no longer present in the latest snapshot, marking them as deleted.

## Steps for Reconciliation

1. The DAG queries BigQuery to find the latest snapshot.
2. It compares the existing records with the latest snapshot to identify records that should be marked as deleted.
3. The identified records are updated with the `deleted` flag set to `TRUE` and `deleted_snapshot_id` set to the most recent snapshot ID.

## DAG Structure

- **Task 1**: Run a query to identify records that should be marked as deleted.
- **Task 2**: Mark the identified records as deleted in BigQuery.

## BigQuery Schema

| Column               | Type         |
|----------------------|--------------|
| `snapshot_id`        | STRING       |
| `data_field`         | STRING       |
| `deleted`            | BOOLEAN      |
| `deleted_snapshot_id`| STRING       |
| `timestamp`          | TIMESTAMP    |

## Requirements

1. Install the required dependencies in the Composer environment via `requirements.txt`:
    ```
    apache-airflow[gcp]
    google-cloud-bigquery
    google-cloud-pubsub
    ```

2. Deploy the DAG to the Composer environment by uploading the script under the `dags` directory.

3. Ensure that the **IAM roles** are set up for the Composer environment to access **BigQuery** and **Pub/Sub**.

4. Monitor the DAG execution through the Airflow UI.

## Development and Deployment

1. **Development**: Create and test the DAG script locally.
2. **Deployment**: Upload the DAG to Composer, ensuring proper setup of IAM roles and BigQuery access.

## Troubleshooting

- Check Airflow logs for task failures or execution errors.
- Verify that the **BigQuery table schema** is correctly defined and aligns with the data being processed.

