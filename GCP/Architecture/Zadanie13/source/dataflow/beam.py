from __future__ import absolute_import
import argparse
import logging
import json
import strict_rfc3339

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

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

class AddTimestampToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddTimestampToDict: %s %r' % (type(element), element))
        return [beam.window.TimestampedValue(
            element, element['timestamp'])]

class AddKeyToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddKeyToDict: %s %r' % (type(element), element))
        return [(element['deviceid'], element)]

class CountAverages(beam.DoFn):
    def process(self, element):
        logging.debug('CountAverages start: %s %r' % (type(element), element))
        stat_names = ["I",
                      "U",
                      "Tm"]

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
        '--output_bigquery',
        default='IoTData.engine',
        help=(
            'Output BigQuery table: '
            'PROJECT:DATASET.TABLE '
            'or DATASET.TABLE.'))
    args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions(pipeline_args)
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).streaming = True

    p = beam.Pipeline(options=options)
    pubsub_stream = ( p | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=args.topic))
    records = ( pubsub_stream | 'Parse JSON to Dict' >> beam.Map(lambda e: json.loads(e)))

    # stream to BigQuery
    (
      records | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
        args.output_bigquery,
        schema=Schema.get_bigquery_schema(),
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )

    # stream to Bucket
    ( pubsub_stream | 'Log element' >> beam.ParDo(LogElement())

    ( records | 'Add timestamp' >> beam.ParDo(AddTimestampToDict())
              | 'Window' >> beam.WindowInto(beam.window.SlidingWindows(30, 10, offset=0))
              | 'Dict to KeyValue' >> beam.ParDo(AddKeyToDict())
              | 'Group by Key' >> beam.GroupByKey()
              | 'Count average' >> beam.ParDo(CountAverages())
    )

    # log element
    # ( records | 'Log element' >> beam.ParDo(LogElement()))    

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
