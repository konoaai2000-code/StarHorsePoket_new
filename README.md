# Thoroughbred Chronicle

競走馬育成ゲーム（ブラウザ版）。GitHub Pages で公開。

## ファイル構成（v4.3.2 第11弾〜）

| パス | 内容 |
| --- | --- |
| `index.html` | 本体（HTML＋JS） |
| `assets/css/game.css` | スタイル（旧 index.html 内の `<style>` 群を記述順のまま統合） |
| `assets/img/` | 画像（旧 base64 埋め込み。JPEG は WebP に変換済み） |
| `assets/audio/sfx/` | 実録音の効果音。読み込めない環境では合成音で代用 |
| `assets/data/real_fields.js` | 実在馬の出走データ（`tools/build_real_fields.py` で `research/real_fields/real_fields_all.csv` から生成） |
| `CREDITS.md` | 音源クレジット（CC BY 素材を含むため削除しないこと） |
| `tools/extract_assets.py` | index.html 内の base64 画像を `assets/img/` に書き出すスクリプト |
| `tools/build_standalone.py` | CSS と画像を埋め込み直した単一HTMLを作るスクリプト（外部ファイルを読めないアプリ内ビューア用） |

公開時は `index.html` と `assets/` をセットで置くこと（`index.html` 単体では画像とスタイルが出ない）。

単一HTMLが必要な場合：

```
python3 tools/build_standalone.py index.html standalone.html            # 効果音も埋め込む（約3.4MB）
python3 tools/build_standalone.py index.html standalone.html --no-audio # 効果音なし（約2.6MB、合成音で代用）
```
