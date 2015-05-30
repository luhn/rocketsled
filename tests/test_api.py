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
    output = generate_manifest_json('tests/static/', manifest)
    assert json.loads(output) == [
        ['css/main.css', u'2r15TxTEa1VqV0Ycsh8OlG5hBpc'],
        ['css/nav.css', u'37qyl7CEX5uGRXrB8M6txzUv8Yo'],
        ['hello.txt', u'R6AT5mDUCGGdiUsggGsdUIaqsDs'],
        ['images/blank.gif', u'1fzrZTJkPQ2E_-CcQMSB7N9Z4Vo'],
        ['images/subdir/blank.png', u'oBRw69w7ipXVXVj_h7fLacS834E'],
    ]
