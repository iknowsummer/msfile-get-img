import zipfile
import io
import os

# Office拡張子とmediaディレクトリの対応表
OFFICE_MEDIA_MAP = {
    ".docx": "word/media/",
    ".xlsx": "xl/media/",
    ".pptx": "ppt/media/",
}


def is_office_file(filename):
    """
    ファイル名がOfficeファイルの拡張子で終わるかチェック
    """
    return filename.lower().endswith(tuple(OFFICE_MEDIA_MAP.keys()))


def office_media_to_zip_stream(file_stream):
    """
    file_streamのzipからmediaフォルダだけ新しいzipバイトストリームに詰める
    """
    output_stream = io.BytesIO()
    media_dirs = OFFICE_MEDIA_MAP.values()
    with (
        zipfile.ZipFile(file_stream, "r") as zin,
        zipfile.ZipFile(output_stream, "w") as zout,
    ):
        for name in zin.namelist():
            is_media_file = any(
                name.startswith(media_dir) and not name.endswith("/")
                for media_dir in media_dirs
            )
            if is_media_file:
                zout.writestr(os.path.basename(name), zin.read(name))
    output_stream.seek(0)
    return output_stream
