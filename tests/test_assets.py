import os
import os.path
from tempfile import NamedTemporaryFile
from io import BytesIO
from gzip import GzipFile

import pytest

from rocketsled import load_assets
from rocketsled.asset import (
    Asset, CompressedAsset, StylesheetAsset, create_asset_from_path,
    MissingAsset,
)


def test_asset_mime_type():
    asset = Asset('css/main.css')
    assert asset.headers['Content-Type'] == 'text/css'

    asset = Asset('foo.nonsense')
    assert 'Content-Type' not in asset.headers


def test_create_asset_from_path():
    assert isinstance(
        create_asset_from_path('images/blank.gif'),
        Asset
    )
    assert isinstance(
        create_asset_from_path('js/main.js'),
        CompressedAsset
    )
    assert isinstance(
        create_asset_from_path('images/blank.svg'),
        CompressedAsset
    )
    assert isinstance(
        create_asset_from_path('css/main.css'),
        StylesheetAsset
    )


def test_process_assset():
    """
    Does absolutely nothing.

    """
    asset = Asset('tests/static/hello.txt')
    asset.process(dict())
    assert asset.content == asset.encoded == b'Hello world!\n'
    assert asset.processed is True


def test_compressed_asset():
    asset = CompressedAsset('tests/static/hello.txt')
    asset.process(dict())
    assert asset.content == b'Hello world!\n'
    with GzipFile(fileobj=BytesIO(asset.encoded)) as gz:
        assert gz.read() == b'Hello world!\n'
    assert asset.headers['Content-Encoding'] == 'gzip'
    assert asset.processed is True


def test_compressed_asset_consistent_hash():
    """
    Make sure that assets with the same content always give the same hash.
    This initially wasn't working with the compressed assets because  gzip adds
    a timestamp when compressing the file.

    """
    import time
    asset1 = CompressedAsset('tests/static/hello.txt')
    asset1.process(dict())
    fn1 = asset1.filename

    time.sleep(1)
    asset2 = CompressedAsset('tests/static/hello.txt')
    asset2.process(dict())
    assert fn1 == asset2.filename


def test_asset_filename():
    asset1 = Asset('tests/static/hello.txt')
    asset2 = Asset('tests/static/hello.txt')

    # Same filename for same content
    asset1._content = b'Hello'
    asset2._content = b'Hello'
    assert asset1.filename == asset2.filename

    # Small change results in different filename
    asset2._content = b'hello'
    assert asset1.filename != asset2.filename

    # Change in headers results in different filename
    asset1._content = b'Hello'
    asset2._content = b'Hello'
    asset1.headers['X-Testing'] = 'Yes'
    assert asset1.filename != asset2.filename


def test_asset_stylesheet():
    manifest = load_assets('tests/static/')
    navcss = manifest[
        os.path.abspath('tests/static/css/nav.css')
    ]
    blankgif = manifest[
        os.path.abspath('tests/static/images/blank.gif')
    ]
    maincss = manifest[
        os.path.abspath('tests/static/css/main.css')
    ]
    maincss.process(manifest)

    assert navcss.processed
    assert blankgif.processed

    expected = (
        '@import url("{}");\n'
        '@import url("http://example.com/absolute.css");\n'
        '\n'
        'body {{\n'
        '\tbackground:url("{}");\n'
        '\tbackground-size:cover;\n'
        '}}\n'
    ).format(navcss.filename, blankgif.filename).encode('ascii')
    assert maincss.content == expected

    with GzipFile(fileobj=BytesIO(maincss.encoded)) as gz:
        assert gz.read() == expected


def test_asset_stylesheet_noexist():
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b'@import url(noexist.css);\n')
        fn = tmp.name

    try:
        asset = StylesheetAsset(fn)
        with pytest.raises(MissingAsset):
            asset.process(dict())
    finally:
        os.remove(fn)


def test_asset_stylesheet_url_params():
    """
    Sometimes URLs will include things like ``?#iefix`` which we don't care
    about.

    """
    asset = StylesheetAsset('test.css')
    other = StylesheetAsset('other.css')
    other._content = b'foo'
    asset._content = (
        b'@import url("other.css?version");\n'
        b'@import url("other.css#iefix");\n'
        b'@import url("other.css?#iefix");\n'
    )
    # Should not throw MissingAsset error.
    asset.process({
        'test.css': asset,
        'other.css': other,
    })
