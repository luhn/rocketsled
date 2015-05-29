import os.path

from rocketsled import load_assets


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
    for key, value in assets.items():
        assert value.path == key
