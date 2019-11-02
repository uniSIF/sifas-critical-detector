from pathlib import Path

# criticalフォルダの画像をカウントする
p_tmp_critical = Path('detected/critical')
count_critical = len([p for p in p_tmp_critical.iterdir() if p.suffix == '.jpg'])

# greatフォルダの画像をカウントする
p_tmp_great = Path('detected/great')
count_great = len([p for p in p_tmp_great.iterdir() if p.suffix == '.jpg'])

# クリティカル率を計算する
total_notes = count_critical + count_great
critical_rate = count_critical / total_notes

print('total notes: {0}'.format(total_notes))
print('CRITICAL: {0}'.format(count_critical))
print('CRITICAL rate: {0}'.format(critical_rate))