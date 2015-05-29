from rocketsled import load_assets


def test_load_assets():
    assets = load_assets('tests/static/')
    assert set(assets.keys()) == {
        'hello.txt',
        'css/main.css',
        'css/nav.css',
        'images/blank.gif',
        'images/subdir/blank.png',
    }
    for key, value in assets.items():
        assert value.path == key
