import mimetypes


class Asset(object):
    """
    An object representing a static asset.

    """
    processed = False
    _contents = None

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
        return

    @property
    def content(self):
        pass

    @content.setter
    def content(self, name):
        pass

    @property
    def hash(self):
        pass


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
        super(CompressedAsset, self).process()
        # TODO:  gzip content


class StylesheetAsset(CompressedAsset):
    def process(self, manifest):
        if self.processed:
            return
        # TODO:  Process URLs in stylesheet
        super(StylesheetAsset, self).process()


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
