from datetime import datetime, timedelta
from airflow import models
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.operators.pubsub import PubSubPublishMessageOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

# Define the DAG
with models.DAG(
    'snapshot_data_reconciliation',
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'start_date': datetime(2025, 2, 3),
    },
    schedule_interval='@daily',  # This can be adjusted to your needs
    catchup=False,
) as dag:

    # Query to identify records that need to be marked as deleted
    delete_query = """
    WITH latest_snapshot AS (
        SELECT snapshot_id
        FROM `your_project.your_dataset.your_table`
        GROUP BY snapshot_id
        ORDER BY timestamp DESC
    )
    SELECT *
    FROM `your_project.your_dataset.your_table` AS data
    WHERE data.snapshot_id NOT IN (SELECT snapshot_id FROM latest_snapshot)
    """
    
    # Query to delete or mark records as deleted
    mark_deleted_query = """
    UPDATE `your_project.your_dataset.your_table`
    SET deleted = TRUE, deleted_snapshot_id = (SELECT snapshot_id FROM `your_project.your_dataset.your_table` ORDER BY timestamp DESC LIMIT 1)
    WHERE snapshot_id IN (SELECT snapshot_id FROM `your_project.your_dataset.your_table` WHERE deleted = FALSE)
    """

    # Task to run the deletion query on BigQuery
    run_delete_query = BigQueryExecuteQueryOperator(
        task_id='run_delete_query',
        sql=delete_query,
        use_legacy_sql=False,
        gcp_conn_id='google_cloud_default'
    )

    # Task to run the mark as deleted query
    run_mark_deleted_query = BigQueryExecuteQueryOperator(
        task_id='run_mark_deleted_query',
        sql=mark_deleted_query,
        use_legacy_sql=False,
        gcp_conn_id='google_cloud_default'
    )

    # The tasks are chained in a sequence
    run_delete_query >> run_mark_deleted_query

