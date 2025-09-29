#!/usr/bin/env python3
import RPi.GPIO as GPIO, time

DT, SCK = 5, 6  # BCM 번호 (DT=GPIO5, SCK=GPIO6)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DT, GPIO.IN)
GPIO.setup(SCK, GPIO.OUT, initial=GPIO.LOW)

def wait_ready(timeout=1.0):
    t0 = time.time()
    while GPIO.input(DT):
        if time.time() - t0 > timeout:
            return False
        time.sleep(0.0002)
    return True

def read_channel(pulses_after):
    """pulses_after:
       1 → 채널 A, 게인 128
       2 → 채널 B, 게인 32
       3 → 채널 A, 게인 64
    """
    if not wait_ready():
        return None
    v = 0
    for _ in range(24):
        GPIO.output(SCK, 1)
        v = (v << 1) | GPIO.input(DT)
        GPIO.output(SCK, 0)
    if v & 0x800000:  # 24비트 2의 보수 처리
        v -= 1 << 24
    for _ in range(pulses_after):
        GPIO.output(SCK, 1)
        GPIO.output(SCK, 0)
    return v

try:
    print("로드셀 미연결 상태: A채널(128배), B채널(32배) 원시값 테스트")
    while True:
        a128 = read_channel(1)  # A 채널 128배
        b32  = read_channel(2)  # B 채널 32배
        print(f"A128={a128:>8}   B32={b32:>8}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(SCK, 0)
    GPIO.cleanup()
