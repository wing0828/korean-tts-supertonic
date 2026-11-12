# korean-tts-supertonic

API 키 없이 CPU만으로 돌아가는 한국어 TTS 스크립트입니다. [Supertonic](https://github.com/supertone-inc/supertonic) 온디바이스 모델로 텍스트 파일을 그대로 읽어 `.wav` 또는 `.mp3`로 저장합니다. 인스타그램 릴스 한국어 내레이션용으로 쓰고 있습니다.

## 설치

```bash
python3 -m venv .venv-supertonic
.venv-supertonic/bin/pip install -r requirements.txt
```

mp3로 저장하려면 `ffmpeg`가 필요합니다. 모델은 첫 실행 때 자동으로 내려받습니다.

## 사용법

```bash
echo "안녕하세요, 오늘의 AI 소식입니다." > script.txt
./supertonic_tts.sh F1 script.txt out.mp3 1.05
# 또는
./supertonic_tts.sh --voice M2 --text-file script.txt --output out.wav --speed 1.1
```

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--voice` | 목소리 F1–F5(여성), M1–M5(남성) | 필수 |
| `--text-file` | 읽을 텍스트 파일(UTF-8) | 필수 |
| `--output` | 출력 경로 `.wav` / `.mp3` | 필수 |
| `--speed` | 속도 0.7–2.0 | 1.05 |
| `--lang` | 언어 코드 | `ko` |
| `--steps` | 품질 단계 5–12 | 8 |

## 라이선스

MIT. Supertonic 모델과 라이브러리는 각자의 라이선스를 따릅니다.
