import io
import zipfile
import pytest
from office_media_utils import office_media_to_zip_stream


DUMMY_PNG = b"\x89PNG\r\n\x1a\n" + b"dummy_png"
DUMMY_JPG = b"\xff\xd8\xff" + b"dummy_jpg"
DUMMY_MEDIA = b"dummy_mediafile"
DUMMY_TEXT = b"dummy_text"
MEDIA_FILES = ["img1.png", "img2.jpg"]


def create_fake_office_zip(media_dir, files):
    # 指定ディレクトリにファイルを格納したzip(officeファイル想定)を作成
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, "w") as zout:
        for fname in files:
            if fname.lower().endswith(".png"):
                data = DUMMY_PNG
            elif fname.lower().endswith(".jpg") or fname.lower().endswith(".jpeg"):
                data = DUMMY_JPG
            else:
                data = DUMMY_MEDIA
            zout.writestr(f"{media_dir}{fname}", data)
    mem_zip.seek(0)
    return mem_zip


def test_office_media_to_zip_stream_docx():
    # 正常系: docxファイルのmediaフォルダを抽出
    fake_zip = create_fake_office_zip("word/media/", MEDIA_FILES)
    result_bytes = office_media_to_zip_stream(fake_zip)
    with zipfile.ZipFile(io.BytesIO(result_bytes)) as zin:
        names = zin.namelist()
        assert set(names) == set(MEDIA_FILES)
        for name in names:
            if name.endswith(".png"):
                assert zin.read(name) == DUMMY_PNG
            elif name.endswith(".jpg"):
                assert zin.read(name) == DUMMY_JPG
            else:
                assert zin.read(name) == DUMMY_MEDIA


def test_office_media_to_zip_stream_no_media():
    # 異常系: mediaフォルダが無い
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, "w") as zout:
        zout.writestr("word/document.xml", b"dummy content")
    mem_zip.seek(0)
    with pytest.raises(RuntimeError, match="メディアを抽出できませんでした"):
        office_media_to_zip_stream(mem_zip)


def test_office_media_to_zip_stream_bad_zip():
    # 異常系: 壊れたzip
    bad_zip = io.BytesIO(b"not a zip file")
    with pytest.raises(RuntimeError, match="BadZipFile"):
        office_media_to_zip_stream(bad_zip)
