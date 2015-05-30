import re
import os.path
import urllib as urlparse
from io import BytesIO
from gzip import GzipFile
import mimetypes
import hashlib
from base64 import urlsafe_b64encode as b64encode


class MissingAsset(Exception):
    pass


class Asset(object):
    """
    An object representing a static asset.

    """
    processed = False
    _content = None

    def __init__(self, path):
        self.path = path
        self.headers = dict()
        mtype, encoding = mimetypes.guess_type(path)
        if mtype is not None:
            self.headers['Content-Type'] = mtype

    def process(self, manifest):
        """
        Do any processing necessary to prepare the file for upload.

        """
        self.processed = True

    @property
    def content(self):
        if self._content is not None:
            return self._content
        with open(self.path, 'rb') as fh:
            self._content = fh.read()
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def filename(self):
        hash = hashlib.sha1(self.content).digest()
        return b64encode(hash).decode('ascii').rstrip('=')


class CompressedAsset(Asset):
    #: Compressable mimetypes, exclude text/* types (which are assumed)
    COMPRESSABLE = {
        'image/svg+xml',
        'application/javascript',
        'application/json',
        'application/xml',
        'application/xhtml+xml',
    }

    def process(self, manifest):
        if self.processed:
            return
        super(CompressedAsset, self).process(manifest)

        io = BytesIO()
        with GzipFile(fileobj=io, mode='wb') as gz:
            gz.write(self.content)
        self.content = io.getvalue()
        self.headers['Content-Encoding'] = 'gzip'


class StylesheetAsset(CompressedAsset):
    URL_REGEX = re.compile(r'url\([\'"]?([^\'"\)]*)[\'"]?\)', re.I)

    def process(self, manifest):
        if self.processed:
            return

        def sub_urls(match):
            url = match.group(1)
            if url.startswith('http://') or url.startswith('https://'):
                return 'url("{}")'.format(url)
            path = os.path.normpath(
                os.path.join(
                    os.path.dirname(self.path),
                    urlparse.unquote(url),
                )
            )
            try:
                asset = manifest[path]
                asset.process(manifest)
                # (We know the asset filename is URL safe, no need to quote
                return 'url("{}")'.format(asset.filename)
            except KeyError:
                raise MissingAsset('Could not find "{}" in "{}"'.format(
                    url, self.path,
                ))

        self.content = self.URL_REGEX.sub(
            sub_urls, self.content.decode('ascii')
        ).encode('ascii')

        super(StylesheetAsset, self).process(manifest)


def create_asset_from_path(path):
    """
    Given a filepath, create an appropriate asset object.

    :param path:  The file path.
    :type path:  str

    :returns:  The appropriate asset.
    :rtype:  :class:`Asset`

    """
    mtype, _ = mimetypes.guess_type(path)
    if mtype == 'text/css':
        return StylesheetAsset(path)
    elif mtype.startswith('text/') or mtype in CompressedAsset.COMPRESSABLE:
        return CompressedAsset(path)
    else:
        return Asset(path)
