import cv2
import numpy as np
from pathlib import Path
import shutil
import os

# 分類対象ファイルの一覧を取得
p_tmp = Path('detected')
file_list_tmp = sorted([int(p.stem) for p in p_tmp.iterdir() if p.suffix == '.jpg'])
file_list = ['detected/' + str(file) + '.jpg' for file in file_list_tmp]

file_count = len(file_list)  # 全ファイル数
i = 0  # 処理中の画像のインデックス

while i < file_count:
    # 画像の読み込み
    source_file = file_list[i]
    file_name = os.path.basename(source_file)
    source = cv2.imread(source_file)
    cv2.putText(source, '{0}/{1}'.format(i+1, file_count), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), thickness=2)

    # 画像を表示し、ユーザのキー入力を待つ
    cv2.imshow('img', source)
    cv2.moveWindow('img', 0, 0)
    key = cv2.waitKey(0)

    if key == 113:
        # qが押された場合、終了する
        break
    elif key == 112:
        # pが押された場合、先頭フレームでなければ、直前フレームに移動する
        if i > 0:
            i -= 1
    elif key == 10 or key == 13:
        # Enterが押された場合、CRITICALに分類する
        destination = 'detected/critical/' + file_name
        if source_file != destination:
            shutil.copy(source_file, destination)
            os.remove(source_file)
            file_list[i] = destination
        i += 1
    else:
        # 上記以外のキーが押された場合、GREATに分類する
        destination = 'detected/great/' + file_name
        if source_file != destination:
            shutil.copy(source_file, destination)
            os.remove(source_file)
            file_list[i] = destination
        i += 1
    
# 画像表示を閉じる
cv2.destroyAllWindows()