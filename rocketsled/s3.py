from boto.s3.connection import S3Connection
from boto.s3.key import Key


def upload_assets(manifest, bucket_name, prefix=None):
    b = S3Connection().get_bucket(bucket_name)
    for asset in manifest.values():
        fn = asset.filename
        if prefix:
            fn = prefix + asset.filename
        if b.get_key(fn) is not None:
            continue
        k = Key(b)
        k.key = fn
        k.set_contents_from_string(asset.encoded, headers=asset.headers)
