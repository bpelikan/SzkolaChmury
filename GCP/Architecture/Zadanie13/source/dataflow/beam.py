from __future__ import absolute_import
import argparse
import logging
import json
import strict_rfc3339

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.io import BigQueryDisposition
import apache_beam.transforms.window as window
# from apache_beam.io.gcp.bigtableio import WriteToBigTable
# from google.cloud.bigtable import row, column_family

class LogElement(beam.DoFn):
    def process(self, element):
        logging.info('ELEMENT: {0} {1}'.format(type(element), element))
        return [(element)]

class Schema(object):
    @staticmethod
    def get_bigquery_schema():
        schema_str = ('timestamp:TIMESTAMP, '
                      'deviceid:STRING, '
                      'I:FLOAT, '
                      'U:FLOAT, '
                      'Tm:FLOAT')
        return schema_str

    @staticmethod
    def get_bigquery_avg_schema():
        schema_avg = ('timestamp:TIMESTAMP, '
                      'deviceid:STRING, '
                      'I:FLOAT, '
                      'U:FLOAT, '
                      'Tm:FLOAT')
        return schema_avg

class AddTimestampToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddTimestampToDict: %s %r' % (type(element), element))
        return [beam.window.TimestampedValue(element, element['timestamp'])]

class AddKeyToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddKeyToDict: %s %r' % (type(element), element))
        return [(element['deviceid'], element)]

class CountAverages(beam.DoFn):
    def process(self, element):
        logging.debug('CountAverages start: %s %r' % (type(element), element))
        stat_names = ["I","U","Tm"]

        avg_e = {}
        aggr = {}
        for k in stat_names:
            aggr[k] = (0, 0)

        avg_e['deviceid'] = element[0]
        avg_e['timestamp'] = strict_rfc3339.now_to_rfc3339_localoffset()

        # Emit sum and count for each metric
        for elem_map in element[1]:
            for key in stat_names:
                if key in elem_map:
                    value = elem_map[key]
                    aggr[key] = (aggr[key][0] + value, aggr[key][1] + 1)

        # Calculate average and set in return map
        for key, value in aggr.items():
            if value[1] == 0:
                avg_e[key] = 0
            else:
                avg_e[key] = value[0] / value[1]
        logging.info('CountAverages end: {}'.format(avg_e))

        return [avg_e]

class WriteBatchesToGCS(beam.DoFn):
    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, batch, window=beam.DoFn.WindowParam):
        """Write one batch per file to a Google Cloud Storage bucket. """

        ts_format = "%Y%m%d%H%M"
        window_start = window.start.to_utc_datetime().strftime(ts_format)
        window_end = window.end.to_utc_datetime().strftime(ts_format)
        filename = "-".join([self.output_path, window_start, window_end])
        filename = filename + ".json"

        with beam.io.gcp.gcsio.GcsIO().open(filename=filename, mode="w") as f:
            for element in batch:
                f.write("{}\n".format(json.dumps(element)).encode("utf-8"))

# class AddBT(beam.DoFn):
#     def process(self, element):
#         logging.debug('AddKeyToDict: %s %r' % (type(element), element))
#         return row.DirectRow(row_key=str(element['timestamp']).encode("utf-8")).set_cell(
#                     "data", 
#                     "deviceid",
#                     element['deviceid'],
#                     datetime.datetime.now())

def run(argv=None):
    """Build and run the pipeline"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--topic",
        type=str,
        help='Pub/Sub topic to read from')
    parser.add_argument(
        "--output_bucket",
        help=('Output local filemane'))
    parser.add_argument(
        "--output_bucket_win",
        help=('Output local filemane for win'))
    parser.add_argument(
        '--output_bigquery',
        default='IoTData.engine',
        help=(
            'Output BigQuery table: '
            'PROJECT:DATASET.TABLE '
            'or DATASET.TABLE.'))
    parser.add_argument(
        '--output_bigquery_avg',
        default='DeviceData.engine_avr',
        help=(
            'Output BigQuery table for averages: '
            'PROJECT:DATASET.TABLE or DATASET.TABLE.'))
    args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions(pipeline_args)
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).streaming = True

    p = beam.Pipeline(options=options)
    pubsub_stream = ( p | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=args.topic))
    records = ( pubsub_stream | 'Parse JSON to Dict' >> beam.Map(lambda e: json.loads(e))
                              | 'Add timestamp' >> beam.ParDo(AddTimestampToDict())
                              )

    # stream to BigQuery
    (
      records | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
        args.output_bigquery,
        schema=Schema.get_bigquery_schema(),
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )

    # stream to Bucket
    # ( pubsub_stream | 'Write to file' >> beam.io.WriteToText(args.output_bucket))

    # averages
    ( records | "Window for avg" >> beam.WindowInto(window.FixedWindows(60))
              | 'Add deviceId Key' >> beam.ParDo(AddKeyToDict())
              | 'Group by Key' >> beam.GroupByKey()
              | 'Count average' >> beam.ParDo(CountAverages())
              | 'Write Avg to BigQuery' >> beam.io.WriteToBigQuery(
                    args.output_bigquery_avg,
                    schema=Schema.get_bigquery_avg_schema(),
                    create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=BigQueryDisposition.WRITE_APPEND)
    )

    ( records | "Window for bucket" >> beam.WindowInto(window.FixedWindows(60))
              | "Add Dummy Key" >> beam.Map(lambda elem: (None, elem))
              | "Group by Dummy Key" >> beam.GroupByKey()
              | "Abandon Dummy Key" >> beam.MapTuple(lambda _, val: val)
              | "Write to GCS" >> beam.ParDo(WriteBatchesToGCS(args.output_bucket_win))
    )

    # (
    #   records | 'Make row' >> beam.ParDo(AddBT())
    #           | "Write to bigtable" >> WriteToBigTable(
    #                 project_id="zadanie13", 
    #                 instance_id="btengineinstance", 
    #                 table_id="engine")
    # )

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
