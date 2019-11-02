import cv2
import numpy as np
import configparser
import sys
import os

# 結果出力フォルダの作成
os.makedirs('source', exist_ok=True)

src_video = cv2.VideoCapture(sys.argv[1])  # 読み込む動画ファイル

if src_video.isOpened:
    frame_count = round(src_video.get(cv2.CAP_PROP_FRAME_COUNT))   # 総フレーム数
    while True:
        in_progress, frame = src_video.read()  # 1フレーム読み込む
        if in_progress:
            i = int(src_video.get(cv2.CAP_PROP_POS_FRAMES))  # 現在フレーム数
            print('\r{0}/{1}({2:.1%})'.format(i, frame_count, i/frame_count), end='')

            output = 'source/' + str(i) + '.jpg'
            cv2.imwrite(output, frame)
        else:
            break

print('\n#### finish! ####')