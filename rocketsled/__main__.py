import argparse
import sys

from rocketsled import (
    load_assets, process_assets, generate_manifest_json, __version__,
)
from rocketsled.s3 import upload_assets


def main():
    parser = argparse.ArgumentParser(
        description='Upload static assets immutably to the cloud.'
    )
    parser.add_argument(
        'region', help='The S3 region of the bucket.',
    )
    parser.add_argument(
        'bucketname', help='The name of the bucket in S3 to upload to.',
    )
    parser.add_argument(
        '--prefix', help='The prefix for the S3 keys.  e.g., "static/"',
    )
    parser.add_argument(
        '--outfile', default='manifest.json',
        help='The file to output the manifest to.',
    )
    parser.add_argument(
        '--stdout', action='store_true',
        help='Output the manifest to stdout.',
    )
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {}'.format(__version__),
    )
    parser.add_argument(
        'path', nargs='+',
        help='Path to static files to upload.',
    )
    args = parser.parse_args()

    def output(text):
        if not args.stdout:
            sys.stdout.write(text)
            sys.stdout.flush()

    output('Collecting files... ')
    manifest = load_assets(*args.path)
    output('{}\n'.format(len(manifest)))
    output('Processing files... ')
    process_assets(manifest)
    output('Done.\n')
    upload_assets(manifest, args.region, args.bucketname, args.prefix,
                  progress=output)
    output = generate_manifest_json(args.path, manifest)
    if args.stdout:
        sys.stdout.write(output)
        sys.stdout.flush()
    else:
        with open(args.outfile, 'w') as fh:
            fh.write(output)


if __name__ == '__main__':
    main()
