from __future__ import absolute_import
import argparse

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

def run(argv=None):
    """Build and run the pipeline"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--topic",
        type=str,
        help='Pub/Sub topic to read from')
    parser.add_argument(
        "--output",
        help=('Output local filemane'))
    args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions(pipeline_args)
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).streaming = True

    p = beam.Pipeline(options=options)
    ( p | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=args.topic)
        | 'Write to file' >> beam.io.WriteToText(args.output)
    )

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__':
    run()
