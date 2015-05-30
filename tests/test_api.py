import os.path

from rocketsled import load_assets
from rocketsled.asset import Asset, CompressedAsset, StylesheetAsset


def test_load_assets():
    assets = load_assets('tests/static/')
    assert set(assets.keys()) == {
        os.path.abspath(os.path.join('tests/static', path)) for path in [
            'hello.txt',
            'css/main.css',
            'css/nav.css',
            'images/blank.gif',
            'images/subdir/blank.png',
        ]
    }
    assert isinstance(
        assets[os.path.abspath('tests/static/css/main.css')],
        StylesheetAsset
    )
    assert isinstance(
        assets[os.path.abspath('tests/static/hello.txt')],
        CompressedAsset
    )
    assert isinstance(
        assets[os.path.abspath('tests/static/images/blank.gif')],
        Asset
    )
    for key, value in assets.items():
        assert value.path == key
