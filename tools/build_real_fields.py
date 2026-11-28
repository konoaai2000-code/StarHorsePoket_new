#!/usr/bin/env python3
"""research/real_fields/real_fields_all.csv から assets/data/real_fields.js を生成する。
使い方: python3 tools/build_real_fields.py
キーはゲーム側の historicRaceKey と同じ正規化（NFKC＋表記ゆれ統一）をしたレース名 → 年 → [馬名, 毛色, 強さ]（強さ順）。"""
import csv, json, pathlib, unicodedata
root = pathlib.Path(__file__).resolve().parent.parent
alias = {'ヴィクトリアM': 'ヴィクトリアマイル', '日本ダービー': '東京優駿', 'オークス': '優駿牝馬', 'ジャパンカップ': 'ジャパンC',
         'マイルチャンピオンシップ': 'マイルCS', 'フェブラリーステークス': 'フェブラリーS'}
out = {}
for row in csv.DictReader(open(root / 'research/real_fields/real_fields_all.csv', encoding='utf-8')):
    name = unicodedata.normalize('NFKC', row['レース名'].strip())
    key = alias.get(name, name)
    try:
        strength = int(row['強さ'])
    except ValueError:
        strength = 85
    out.setdefault(key, {}).setdefault(row['年'].strip(), []).append([row['馬名'].strip(), row['毛色'].strip(), strength])
for years in out.values():
    for y in years:
        seen, uniq = set(), []
        for e in sorted(years[y], key=lambda e: -e[2]):
            if e[0] not in seen:
                seen.add(e[0]); uniq.append(e)
        years[y] = uniq
dst = root / 'assets/data/real_fields.js'
dst.write_text('/* 自動生成：tools/build_real_fields.py（元データ research/real_fields/real_fields_all.csv） */\nwindow.REAL_FIELDS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print(dst, sum(len(v) for y in out.values() for v in y.values()), 'entries,', len(out), 'races')
