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
    assert asset.content == b'Hello world!\n'
    assert asset.processed is True


def test_process_compressed_asset():
    """

    """
    asset = CompressedAsset('tests/static/hello.txt')
    asset.process(dict())
    with GzipFile(fileobj=BytesIO(asset.content)) as gz:
        assert gz.read() == b'Hello world!\n'
    assert asset.headers['Content-Encoding'] == 'gzip'
    assert asset.processed is True


def test_asset_filename():
    asset = Asset('tests/static/hello.txt')
    assert asset.filename == 'R6AT5mDUCGGdiUsggGsdUIaqsDs'


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

    with GzipFile(fileobj=BytesIO(maincss.content)) as gz:
        assert gz.read() == expected


def test_asset_stylesheet_noexist():
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write('@import url(noexist.css);\n')
        fn = tmp.name

    try:
        asset = StylesheetAsset(fn)
        with pytest.raises(MissingAsset):
            asset.process(dict())
    finally:
        os.remove(fn)
