import os
import zipfile
import io
import shutil
import sys

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
dir_output = os.path.join(desktop_path, "msfiles")


def extract_media_to_zip_stream(file_stream):
    # file_streamのzipからmediaフォルダだけ新しいzipバイトストリームに詰める
    output_stream = io.BytesIO()
    with (
        zipfile.ZipFile(file_stream, "r") as zin,
        zipfile.ZipFile(output_stream, "w") as zout,
    ):
        for name in zin.namelist():
            if name.startswith("word/media/") and not name.endswith("/"):
                zout.writestr(os.path.basename(name), zin.read(name))
    output_stream.seek(0)
    return output_stream


def save_and_extract_zip_stream(zip_stream, output_dir):
    # zip_streamをoutput_dirに解凍
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_stream) as zip_ref:
        zip_ref.extractall(output_dir)


def save_zip_stream(zip_stream, output_zip_path):
    # zip_streamをoutput_zip_pathにzipファイルとして保存
    with open(output_zip_path, "wb") as f:
        f.write(zip_stream.getbuffer())


def main(zipsave=False):
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("ファイルパスを入力: ")

    with open(file_path, "rb") as f:
        zip_stream = extract_media_to_zip_stream(f)

    if zipsave:
        output_zip_path = os.path.join(dir_output, "media_files.zip")
        os.makedirs(dir_output, exist_ok=True)
        save_zip_stream(zip_stream, output_zip_path)
        os.startfile(dir_output)
    else:
        save_and_extract_zip_stream(zip_stream, dir_output)
        os.startfile(dir_output)


if __name__ == "__main__":
    main()
