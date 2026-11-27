#!/usr/bin/env python3
"""秘書ボイス・実況ボイスを Kokoro（hexgrad/Kokoro-82M, Apache-2.0）で生成し assets/audio/voice/ に mp3 で書き出す。
必要: pip install "kokoro>=0.9" "misaki[ja]" soundfile torch / python -m unidic download / ffmpeg
使い方: python3 tools/gen_voice.py [出力先ルート(既定: .)] [--only=secretary|commentary]
声を変えたいときは SECRETARY_VOICES を書き換えて再実行する。"""
import json, pathlib, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from kokoro import KPipeline

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
ONLY = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--only=')), None)
ROOT = pathlib.Path(ARGS[0] if ARGS else '.')
OUT = ROOT / 'assets' / 'audio' / 'voice'

# 秘書 index: 0 葵 / 1 楓 / 2 澪 / 3 凛 / 4 遥   (voice, speed, pitch倍率)
SECRETARY_VOICES = [
    ('jf_alpha', 1.0, 1.00),
    ('jf_tebukuro', 1.05, 1.00),
    ('jf_gongitsune', 0.95, 1.00),
    ('jf_alpha', 0.95, 0.95),
    ('jf_nezumi', 1.05, 1.05),
]
COMMENTATOR = ('jm_kumo', 1.15, 1.00)

# index.html の secGreet 等と同じ文言（ゲーム側は秘書番号＋カテゴリでファイルを引く）
LINES = json.loads((pathlib.Path(__file__).parent / 'voice_lines.json').read_text(encoding='utf-8'))

pipe = KPipeline(lang_code='j', repo_id='hexgrad/Kokoro-82M')

def synth(text, voice, speed, pitch, dst):
    chunks = [a.numpy() for _, _, a in pipe(text, voice=voice, speed=speed)]
    audio = np.concatenate(chunks) if chunks else np.zeros(2400, dtype=np.float32)
    with tempfile.NamedTemporaryFile(suffix='.wav') as tmp:
        sf.write(tmp.name, audio, 24000)
        af = 'silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,loudnorm=I=-16:TP=-1.5'
        if pitch != 1.0:
            af = f'asetrate={int(24000*pitch)},aresample=24000,atempo={1/pitch:.4f},' + af
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp.name, '-af', af, '-ac', '1', '-ar', '24000', '-b:a', '48k', str(dst)], check=True)

for cat, per_sec in (LINES['secretary'].items() if ONLY in (None, 'secretary') else []):
    for i, text in enumerate(per_sec):
        v, sp, pi = SECRETARY_VOICES[i]
        synth(text, v, sp, pi, OUT / f's{i}' / f'{cat}.mp3')
        print('secretary', i, cat)
v, sp, pi = COMMENTATOR
for key, text in (LINES['commentary'].items() if ONLY in (None, 'commentary') else []):
    synth(text, v, sp, pi, OUT / 'commentary' / f'{key}.mp3')
    print('commentary', key)
