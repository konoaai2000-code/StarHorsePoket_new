#!/usr/bin/env python3
"""assets/css/game.css と assets/img/ を参照している index.html から、CSSと画像をすべて埋め込んだ単一HTMLを作る
（外部ファイルを読めないアプリ内ビューア等で遊ぶ用）。
使い方: python3 tools/build_standalone.py index.html standalone.html"""
import base64, re, sys, pathlib
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'standalone.html')
html = src.read_text(encoding='utf-8')
mime = {'webp': 'image/webp', 'jpg': 'image/jpeg', 'png': 'image/png'}
def repl(m):
    p = src.parent / m.group(0)
    return f'data:{mime[m.group(2)]};base64,' + base64.b64encode(p.read_bytes()).decode()
css = (src.parent / 'assets/css/game.css').read_text(encoding='utf-8')
css = css.replace('../img/', 'assets/img/')
html = html.replace('<link rel="stylesheet" href="assets/css/game.css">', '<style>' + css + '</style>')
html = re.sub(r'assets/img/([0-9a-f]{12})\.(webp|jpg|png)', repl, html)
dst.write_text(html, encoding='utf-8')
print(f'{dst}: {len(html.encode())/1e6:.2f}MB')
