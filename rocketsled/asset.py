

class Asset(object):
    """
    An object representing a static asset.

    """
    uploaded = False
    _contents = None

    def __init__(self, path):
        self.path = path

    @property
    def contents(self):
        pass

    @contents.setter
    def contents(self, name):
        pass

    @property
    def hash(self):
        pass
