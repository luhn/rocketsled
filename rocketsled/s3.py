from boto.s3.connection import S3Connection
from boto.s3.key import Key


def upload_assets(manifest, bucket_name, prefix=None, progress=lambda _: None):
    b = S3Connection().get_bucket(bucket_name)

    to_upload = set()
    total = len(manifest)
    checked = 0
    for asset in manifest.values():
        progress('\rChecking S3:  {}% ({} / {})'.format(
            int(checked * 100 / total), checked, total,
        ))
        fn = (prefix or '') + asset.filename
        if b.get_key(fn) is None:
            to_upload.add(asset)
        checked += 1
    progress('\rChecking S3:  Done.      \n')

    total = len(to_upload)
    uploaded = 0
    if total == 0:
        progress('No files to upload.\n')
        return
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
