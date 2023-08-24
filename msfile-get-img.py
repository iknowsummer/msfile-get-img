import os
import sys
import zipfile
import shutil

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
dir_output = os.path.join(desktop_path,"msfiles")
dir_temp = os.path.join(dir_output,"temp")

def main():
    #対象のファイルパスを取得
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("ファイルパスを入力: ")

    # 作業用ディレクトリを作成し、対象をzipとして保存
    makeWorkfile(file_path)

    # mediaの中身をコピー
    getMadiafiles()

    # 終了処理
    # tempディレクトリ削除
    shutil.rmtree(dir_temp)

    #完了後にフォルダを開く
    os.startfile(dir_output)


def makeWorkfile(file_path):
    # デスクトップにディレクトリ"dir_output"を再作成
    if os.path.exists(dir_output): shutil.rmtree(dir_output)
    os.makedirs(dir_output, exist_ok=True)
    os.makedirs(dir_temp, exist_ok=True)

    #zipファイルとして複製して解凍
    zip_filepath = os.path.join(dir_temp,"ms.zip")
    shutil.copy(file_path, zip_filepath)
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dir_temp)

def getMadiafiles():
    #mediaディレクトリを取得
    dir_media = None
    for root, dirs, files in os.walk(dir_temp):
        if 'media' in dirs:
            dir_media =  os.path.join(root, 'media')
            break

    if dir_media is not None:
        #mediaディレクトリのファイルをoutputへコピー
        for file_name in os.listdir(dir_media):
            source = os.path.join(dir_media, file_name)
            destination = os.path.join(dir_output, file_name)
            shutil.copy2(source, destination) 
    else:
        with open(os.path.join(dir_output,'noMedia.txt'), 'w') as f:
            f.write('The directory "media" does not exist.\n')

if __name__ == '__main__':
    main()