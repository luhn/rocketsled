import io
import os.path
import json
import hashlib

from boto.s3.connection import S3Connection
from boto.s3.key import Key


def _open_cache(bucket_name, prefix, mode):
    # Each bucket/prefix combo gets its own cache.
    path = os.path.expanduser('~/.rocketsled.{}'.format(
        hashlib.md5(
            bucket_name.encode('utf8') + (prefix or '').encode('utf8')
        ).hexdigest()
    ))
    if mode == 'r' and not os.path.exists(path):
        return io.StringIO(u'[]')
    return open(path, mode)


def upload_assets(manifest, bucket_name, prefix=None, progress=lambda _: None):
    b = S3Connection().get_bucket(bucket_name)

    progress('Checking cache...')
    with _open_cache(bucket_name, prefix, 'r') as fh:
        existing = set(json.load(fh))

    to_check = list()
    for asset in manifest.values():
        fn = asset.filename
        if fn not in existing:
            to_check.append(asset)
        existing.add(fn)

    to_upload = list()
    total = len(to_check)
    checked = 0
    for asset in to_check:
        progress('\rChecking S3:  {}% ({} / {})'.format(
            int(checked * 100 / total), checked, total,
        ))
        fn = (prefix or '') + asset.filename
        if b.get_key(fn) is None:
            to_upload.append(asset)
        checked += 1
    progress('\rChecking S3:  Done.      \n')

    total = len(to_upload)
    uploaded = 0
    for asset in to_upload:
        progress('\rUploading:  {}% ({} / {})'.format(
            int(uploaded * 100 / total), uploaded, total,
        ))
        fn = (prefix or '') + asset.filename
        k = Key(b)
        k.key = fn
        k.set_contents_from_string(asset.encoded, headers=asset.headers)
        uploaded += 1
    progress('\rUploading:  Done.       \n')

    with _open_cache(bucket_name, prefix, 'w') as fh:
        json.dump(list(existing), fh)
