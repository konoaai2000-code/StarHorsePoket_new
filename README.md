# Thoroughbred Chronicle

競走馬育成ゲーム（ブラウザ版）。GitHub Pages で公開。

## ファイル構成（v4.3.2 第11弾〜）

| パス | 内容 |
| --- | --- |
| `index.html` | 本体（HTML＋JS） |
| `assets/css/game.css` | スタイル（旧 index.html 内の `<style>` 群を記述順のまま統合） |
| `assets/img/` | 画像（旧 base64 埋め込み。JPEG は WebP に変換済み） |
| `tools/extract_assets.py` | index.html 内の base64 画像を `assets/img/` に書き出すスクリプト |
| `tools/build_standalone.py` | CSS と画像を埋め込み直した単一HTMLを作るスクリプト（外部ファイルを読めないアプリ内ビューア用） |

公開時は `index.html` と `assets/` をセットで置くこと（`index.html` 単体では画像とスタイルが出ない）。

単一HTMLが必要な場合：

```
python3 tools/build_standalone.py index.html standalone.html
```
