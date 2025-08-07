import os
import shutil
import requests

# テスト用ファイルのパス
file_path = r"backend/office-samples/sample.docx"

# FastAPIサーバーのURL
url = "http://localhost:8000/extract-office-media"

with open(file_path, "rb") as f:
    files = {
        "file": (
            file_path,
            f,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    response = requests.post(url, files=files)

    if response.status_code == 200:
        # 出力ディレクトリを指定
        out_dir = "backend/tmp"

        # 出力ディレクトリを削除して再作成
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir, exist_ok=True)

        # 保存パスを設定
        out_path = os.path.join(out_dir, "mediafiles.zip")

        # zipファイルとして保存
        with open(out_path, "wb") as out:
            out.write(response.content)

        # 成功メッセージと保存先を表示
        print(f"ダウンロード成功: {out_path}")
        print(f"保存先ディレクトリ: {os.path.abspath(out_dir)}")
    else:
        print(f"エラー: {response.status_code}")
        print(response.text)
