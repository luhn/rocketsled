from rocketsled.asset import (
    Asset, CompressedAsset, StylesheetAsset, create_asset_from_path,
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
    from io import BytesIO
    from gzip import GzipFile
    asset = CompressedAsset('tests/static/hello.txt')
    asset.process(dict())
    with GzipFile(fileobj=BytesIO(asset.content)) as gz:
        assert gz.read() == b'Hello world!\n'
    assert asset.headers['Content-Encoding'] == 'gzip'
    assert asset.processed is True


def test_asset_filename():
    asset = Asset('tests/static/hello.txt')
    assert asset.filename == 'R6AT5mDUCGGdiUsggGsdUIaqsDs'
