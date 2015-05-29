from __future__ import absolute_import

import os
import os.path

from .asset import Asset


def load_assets(base_path):
    """
    Walk the directory and collect all static assets.

    :param base_path:  The path of the directory to walk.
    :type base_path:  str

    :returns:  A dictionary with the filepath as the keys and the corresponding
        :class:`rocksled.asset.Asset` object as the values.
    :rtype:  dict

    """
    manifest = dict()
    for dirname, subdirs, files in os.walk(base_path):
        for fn in files:
            if fn.startswith('.'):
                continue
            path = os.path.join(dirname, fn)
            path = os.path.relpath(path, base_path)
            manifest[path] = Asset(path)
    return manifest
