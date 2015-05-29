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
