
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.PipelineOptionsFactory;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.schemas.utils.DataflowSchema;
import org.apache.beam.sdk.values.TypeDescriptor;
import org.apache.beam.sdk.schemas.Schema;

import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableSchema;

import java.util.Arrays;

public class DataflowPipeline {

    public static void main(String[] args) {
        PipelineOptions options = PipelineOptionsFactory.fromArgs(args).withValidation().create();
        options.setJobName("snapshot-data-ingestion");

        Pipeline p = Pipeline.create(options);

        PCollection<DataRecord> inputStream = p.apply("Read from PubSub", 
            PubsubIO.readMessages().fromSubscription("projects/your-project/subscriptions/your-subscription"));

        inputStream.apply("Process Data", ParDo.of(new SnapshotProcessingFn("your_project:your_dataset.your_table")));

        inputStream.apply("Write to BigQuery", 
            BigQueryIO.writeTableRows()
            .to("your_project:your_dataset.your_table")
            .withSchema(getTableSchema())
            .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
            .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_IF_NEEDED));

        p.run().waitUntilFinish();
    }

    private static TableSchema getTableSchema() {
        return new TableSchema()
            .setFields(Arrays.asList(
                new TableFieldSchema().setName("snapshot_id").setType("STRING"),
                new TableFieldSchema().setName("data_field").setType("STRING"),
                new TableFieldSchema().setName("deleted").setType("BOOLEAN"),
                new TableFieldSchema().setName("deleted_snapshot_id").setType("STRING"),
                new TableFieldSchema().setName("timestamp").setType("TIMESTAMP")
            ));
    }
}
