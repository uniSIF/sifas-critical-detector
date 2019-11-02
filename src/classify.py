import cv2
import numpy as np
from pathlib import Path
import shutil
import configparser

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('parameter.conf', encoding='utf-8')

x = int(config['CRITICAL']['AREA_X'])      # 検出領域の左上X座標
y = int(config['CRITICAL']['AREA_Y'])      # 検出領域の左上Y座標
w = int(config['CRITICAL']['AREA_WIDTH'])  # 検出領域の幅
h = int(config['CRITICAL']['AREA_HEIGHT']) # 検出領域の高さ
threshold = float(config['CRITICAL']['DETECT_THRESHOLD']) # 検出しきい値

# 検出対象ファイルの一覧を取得
p_tmp = Path('detected')
file_list = sorted([int(p.stem) for p in p_tmp.iterdir() if p.suffix == '.jpg'])

for i in file_list:
    # 画像の読み込み
    source = cv2.imread('detected/' + str(i) + '.jpg', 0)  # 判定画像
    great = cv2.imread('great.png', 0)  # GREATの画像
    critical = cv2.imread('critical.png', 0)  # CRITICALの画像

    source_cropped = source[y:y+h,x:x+w]

    #テンプレートマッチング
    match_result_great = cv2.matchTemplate(source_cropped, great, cv2.TM_CCOEFF_NORMED)
    match_result_critical = cv2.matchTemplate(source_cropped, critical, cv2.TM_CCOEFF_NORMED)

    # 検出結果の座標を取得する
    loc_great=np.where(match_result_great >= threshold)
    loc_critical=np.where(match_result_critical >= threshold)

    # 検出結果がある場合、GREAT/CRITICALを検出したとみなし、画像をgreat/ciritaclフォルダに保存する
    # 検出結果がない場合、検出に失敗したとみなし、何もしない
    if loc_great[0].size > 0 or loc_critical[0].size > 0:
        if loc_great[0].size > 0:
            print(str(i) + ': GREAT')
            output = str(i) + '.jpg'
            shutil.move('detected/' + output, 'detected/great/' + output)
        else:
            print(str(i) + ': CRITICAL')
            output = str(i) + '.jpg'
            shutil.move('detected/' + output, 'detected/critical/' + output)
    else:
        print(str(i) + ': unknown')