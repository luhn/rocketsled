import sys
import re
import os.path
from io import BytesIO
from gzip import GzipFile
import mimetypes
import hashlib
from base64 import urlsafe_b64encode as b64encode

# Python 2/3 imports
if sys.version_info[0] < 3:
    from urllib import unquote
    from urlparse import urlsplit
else:
    from urllib.parse import unquote, urlsplit


class MissingAsset(Exception):
    pass


class Asset(object):
    """
    An object representing a static asset.

    """
    processed = False
    _content = None
    _encoded = None

    def __init__(self, path):
        self.path = path
        self.headers = {
            'Cache-Control': 'max-age=31556926',
        }
        mtype, encoding = mimetypes.guess_type(path)
        if mtype is not None:
            self.headers['Content-Type'] = mtype

    def process(self, manifest):
        """
        Do any processing necessary to prepare the file for upload.

        """
        self.processed = True

    def encode(self):
        """
        Encode the content.  (Compression, mainly.)

        """
        return self.content

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
    def encoded(self):
        if self._encoded is None:
            self._encoded = self.encode()
        return self._encoded

    @property
    def filename(self):
        hash = hashlib.sha1()
        for key, value in sorted(self.headers.items()):
            hash.update(key.encode('utf8'))
            hash.update(value.encode('utf8'))
        hash.update(self.content)
        return b64encode(hash.digest()).decode('ascii').rstrip('=')


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
        self.headers['Content-Encoding'] = 'gzip'
        super(CompressedAsset, self).process(manifest)

    def encode(self):
        encoded = super(CompressedAsset, self).encode()
        io = BytesIO()
        with GzipFile(fileobj=io, mode='wb') as gz:
            gz.write(encoded)
        return io.getvalue()


class StylesheetAsset(CompressedAsset):
    URL_REGEX = re.compile(r'url\([\'"]?([^\'"\)]*)[\'"]?\)', re.I)

    def process(self, manifest):
        if self.processed:
            return

        def sub_urls(match):
            url = match.group(1)
            if(
                    url.startswith('http://')
                    or url.startswith('https://')
                    or url.startswith('data:')
            ):
                return 'url("{}")'.format(url)
            path = os.path.normpath(
                os.path.join(
                    os.path.dirname(self.path),
                    unquote(
                        urlsplit(url).path
                    ),
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

        try:
            self.content = self.URL_REGEX.sub(
                sub_urls, self.content.decode('utf-8')
            ).encode('utf-8')
        except:
            print(self.path)
            raise

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
    if mtype is None:
        return Asset(path)
    elif mtype == 'text/css':
        return StylesheetAsset(path)
    elif mtype.startswith('text/') or mtype in CompressedAsset.COMPRESSABLE:
        return CompressedAsset(path)
    else:
        return Asset(path)
