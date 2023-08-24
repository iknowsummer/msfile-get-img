import os
import zipfile
import shutil

file_path = input("ファイルパスを入力: ")
# file_path = r"C:\Users\user\Desktop\20230823102930_attach\看護部-修正案2.pptx"


# デスクトップにディレクトリ"dir_output"を作成
# 残ってる場合は一旦中身を削除
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

dir_output = os.path.join(desktop_path,"msfiles")
if os.path.exists(dir_output): shutil.rmtree(dir_output)
os.makedirs(dir_output, exist_ok=True)

dir_temp = os.path.join(dir_output,"temp")
os.makedirs(dir_temp, exist_ok=True)


#zipファイルとして複製して解凍
zip_filepath = os.path.join(dir_temp,"ms.zip")
shutil.copy(file_path, zip_filepath)
with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
    zip_ref.extractall(dir_temp)

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

#tempディレクトリ削除
shutil.rmtree(dir_temp)

#完了後にフォルダを開く
os.startfile(dir_output)