#!/usr/bin/env python3
"""assets/css/game.css と assets/img/ を参照している index.html から、CSSと画像をすべて埋め込んだ単一HTMLを作る
（外部ファイルを読めないアプリ内ビューア等で遊ぶ用）。
使い方: python3 tools/build_standalone.py index.html standalone.html [--no-audio]
音声（assets/audio/）も既定で埋め込む（約+2.7MB）。--no-audio なら埋め込まず、ゲーム側は合成音・端末音声で鳴らす。"""
import base64, json, re, sys, pathlib
args = [a for a in sys.argv[1:] if not a.startswith('--')]
no_audio = '--no-audio' in sys.argv
sys.argv = [sys.argv[0]] + args
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
if not no_audio:
    audio_root = src.parent / 'assets' / 'audio'
    pack = {str(p.relative_to(audio_root)).replace('\\', '/'): 'data:audio/mpeg;base64,' + base64.b64encode(p.read_bytes()).decode()
            for p in sorted(audio_root.rglob('*.mp3'))}
    marker = '<script type="application/json" id="asset-pack">'
    assert html.count(marker) == 1
    html = html.replace(marker, '<script>window.AUDIO_PACK=' + json.dumps(pack) + '</script>' + marker)
dst.write_text(html, encoding='utf-8')
print(f'{dst}: {len(html.encode())/1e6:.2f}MB')
