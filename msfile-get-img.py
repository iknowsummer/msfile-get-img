import os
import shutil
import sys
import zipfile
import io

from office_media_utils import (
    OFFICE_MEDIA_MAP,
    office_media_to_zip_stream,
    is_office_file,
)


def save_and_extract_zip_stream(zip_stream, output_dir):
    # zip_streamをoutput_dirに解凍
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_stream) as zip_ref:
        zip_ref.extractall(output_dir)


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("ファイルパスを入力: ")

    # 対象ファイルかチェック
    if not is_office_file(file_path):
        exts = "、".join(ext.lstrip(".") for ext in OFFICE_MEDIA_MAP.keys())
        print(f"対象のOfficeファイル（{exts}）ではありません。")
        return

    # ファイルをzipストリームに変換
    with open(file_path, "rb") as f:
        zip_bytes = office_media_to_zip_stream(f)
        zip_stream = io.BytesIO(zip_bytes)

    # デスクトップにmsfilesディレクトリを作成し保存場所に設定
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    dir_output = os.path.join(desktop_path, "msfiles")

    # zipストリームを解凍して保存
    save_and_extract_zip_stream(zip_stream, dir_output)
    os.startfile(dir_output)


if __name__ == "__main__":
    main()
