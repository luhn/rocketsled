import os.path

from rocketsled import load_assets, generate_manifest_json
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


def test_generate_manifest_json():
    import json
    manifest = load_assets('tests/static/')
    output = json.loads(generate_manifest_json('tests/static/', manifest))
    hello = Asset('tests/static/hello.txt')
    assert output[2][1] == hello.filename
    assert [row[0] for row in output] == [
        'css/main.css',
        'css/nav.css',
        'hello.txt',
        'images/blank.gif',
        'images/subdir/blank.png',
    ]
