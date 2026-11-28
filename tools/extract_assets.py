#!/usr/bin/env python3
"""index.html に埋め込まれた base64 画像を assets/img/ に書き出し、相対パス参照に置き換える。
JPEG/PNG は WebP（品質82）に変換、既に WebP のものはそのまま書き出す。
使い方: python3 tools/extract_assets.py index.html
逆変換（単一HTMLに戻す）は tools/build_standalone.py を使う。"""
import base64, hashlib, io, re, sys, pathlib
from PIL import Image

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
root = src.parent
out_dir = root / 'assets' / 'img'
out_dir.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding='utf-8')
MIN = 2000  # これより小さい画像（アイコン等）は埋め込みのまま
pat = re.compile(r'data:image/(jpeg|jpg|png|webp);base64,([A-Za-z0-9+/=]+)')
before = len(html.encode())

def repl(m):
    kind, b64 = m.group(1), m.group(2)
    if len(b64) < MIN:
        return m.group(0)
    raw = base64.b64decode(b64)
    digest = hashlib.sha1(raw).hexdigest()[:12]
    if kind == 'webp':
        data = raw
    else:
        im = Image.open(io.BytesIO(raw))
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'A' in im.getbands() else 'RGB')
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=82, method=6)
        data = buf.getvalue()
        if len(data) >= len(raw):  # 変換で大きくなる場合は元形式のまま
            ext = 'jpg' if kind in ('jpeg', 'jpg') else kind
            name = f'{digest}.{ext}'
            (out_dir / name).write_bytes(raw)
            return f'assets/img/{name}'
    name = f'{digest}.webp'
    (out_dir / name).write_bytes(data)
    return f'assets/img/{name}'

html = pat.sub(repl, html)
src.write_text(html, encoding='utf-8')
total = sum(p.stat().st_size for p in out_dir.iterdir())
print(f'index.html: {before/1e6:.2f}MB -> {len(html.encode())/1e6:.2f}MB, assets/img: {len(list(out_dir.iterdir()))} files {total/1e6:.2f}MB')
