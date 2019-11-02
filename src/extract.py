import cv2
import numpy as np
import configparser
import sys
import os

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('parameter.conf', encoding='utf-8')

# 結果出力フォルダの作成
os.makedirs('detected', exist_ok=True)
os.makedirs('detected/critical', exist_ok=True)
os.makedirs('detected/great', exist_ok=True)

last_detected = (0,0) # 前回検出フレームの情報
detect_count = 0

src_video = cv2.VideoCapture(sys.argv[1])  # 読み込む動画ファイル
template = cv2.imread('icon.png', 0)       # 検出したいカードアイコン

if src_video.isOpened:
    frame_count = round(src_video.get(cv2.CAP_PROP_FRAME_COUNT))   # 総フレーム数
    interval = round(30 / (60 / src_video.get(cv2.CAP_PROP_FPS)))  # コンボ数が切り替わるまでのフレーム数（経験則）
    x = int(config['CARD']['AREA_X'])      # 検出領域の左上X座標
    y = int(config['CARD']['AREA_Y'])      # 検出領域の左上Y座標
    w = int(config['CARD']['AREA_WIDTH'])  # 検出領域の幅
    h = int(config['CARD']['AREA_HEIGHT']) # 検出領域の高さ
    threshold = float(config['CARD']['DETECT_THRESHOLD'])  # 検出しきい値
    while True:
        in_progress, frame = src_video.read()  # 1フレーム読み込む
        if in_progress:
            i = int(src_video.get(cv2.CAP_PROP_POS_FRAMES))  # 現在フレーム数
            print('\r{0}/{1}({2:.1%}) detect:{3}'.format(i, frame_count, i/frame_count, detect_count), end='')

            # 検出のために、画像をグレースケール化し、検出領域のみ切り取る
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_cropped = frame_gray[y:y+h,x:x+w]

            # テンプレートマッチング
            match_result = cv2.matchTemplate(frame_cropped, template, cv2.TM_CCOEFF_NORMED)

            # 検出結果の座標を取得する
            loc=np.where(match_result >= threshold)

            # 検出結果がある場合、カードアイコンを検出したとみなし、検出フレームを記憶する
            if loc[0].size > 0:
                last_detected = (i, frame)

            # 前回の検出から間がある場合、コンボ数が変わったとみなし、前回検出フレームを画像出力する
            if last_detected[0] > 0 and i > last_detected[0] + interval:
                output = 'detected/' + str(last_detected[0]) + '.jpg'
                cv2.imwrite(output, last_detected[1])
                last_detected = (0, 0)
                detect_count += 1
        else:
            break

print('\n#### finish! ####')