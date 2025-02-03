
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.io.gcp.bigquery.TableRow;

public class SnapshotProcessingFn extends DoFn<DataRecord, TableRow> {

    private final String bigQueryTable;

    public SnapshotProcessingFn(String bigQueryTable) {
        this.bigQueryTable = bigQueryTable;
    }

    @ProcessElement
    public void processElement(@Element DataRecord record, OutputReceiver<TableRow> out) {
        TableRow row = new TableRow();
        row.set("snapshot_id", record.getSnapshotId());
        row.set("data_field", record.getDataField());
        row.set("deleted", false); 
        row.set("deleted_snapshot_id", null); 
        row.set("timestamp", record.getTimestamp());  

        out.output(row);
    }
}
