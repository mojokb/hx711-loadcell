# HX711 Load Cell Weight Scale

Raspberry Pi를 사용한 HX711 로드셀 무게 측정 프로젝트입니다.

## 하드웨어 연결

- DT (Data): GPIO 5
- SCK (Clock): GPIO 6
- VCC: 3.3V 또는 5V
- GND: Ground

## 사용법

1. 스크립트 실행:
```bash
python3 main.py
```

2. 영점 설정:
   - 로드셀에 아무것도 올리지 않은 상태로 대기
   - 자동으로 영점이 설정됩니다

3. 보정:
   - "298g 추를 올리고 Enter" 메시지가 나오면
   - 298g 무게추를 올리고 Enter 키를 누르세요
   - 자동으로 스케일이 계산됩니다

4. 측정:
   - 보정 완료 후 실시간으로 무게가 표시됩니다
   - Ctrl+C로 종료할 수 있습니다

## 특징

- 자동 영점 설정
- 298g 표준 무게추를 사용한 보정
- 실시간 무게 측정 및 표시
- GPIO 안전 종료 처리

## 요구사항

- Raspberry Pi
- Python 3
- RPi.GPIO 라이브러리
- HX711 로드셀 앰프
- 298g 표준 무게추 (보정용)

## 설치

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```