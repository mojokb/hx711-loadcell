#!/usr/bin/env python3
import RPi.GPIO as GPIO, time


#kb@raspberrypi:~/loadcell $ python main.py
#영점 설정 중...
#영점: 5746
#298g 추를 올리고 Enter
#298g 값: 36839, 스케일: 104.34/g

DT, SCK = 5, 6
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
    if not wait_ready():
        return None
    v = 0
    for _ in range(24):
        GPIO.output(SCK, 1)
        v = (v << 1) | GPIO.input(DT)
        GPIO.output(SCK, 0)
    if v & 0x800000:
        v -= 1 << 24
    for _ in range(pulses_after):
        GPIO.output(SCK, 1)
        GPIO.output(SCK, 0)
    return v

try:
    print("영점 설정 중...")
    values = []
    count = 0
    zero = 0
    scale = 1
    calibrated = False

    while True:
        a128 = read_channel(1)
        _ = read_channel(2)

        if count < 12:
            count += 1
            if 1 < count <= 12:
                values.append(a128)
                if count == 12:
                    zero = sum(values) // len(values)
                    print(f"영점: {zero}")
                    print("298g 추를 올리고 Enter")

        elif not calibrated:
            input()
            cal_values = []
            for i in range(10):
                a = read_channel(1)
                _ = read_channel(2)
                cal_values.append(a)
                time.sleep(0.1)
            cal_avg = sum(cal_values) // len(cal_values)
            scale = (cal_avg - zero) / 298
            print(f"298g 값: {cal_avg}, 스케일: {scale:.2f}/g")
            calibrated = True

        else:
            grams = (a128 - zero) / scale
            print(f"A128={a128:>8}   무게={grams:>6.1f}g")

        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    GPIO.output(SCK, 0)
    GPIO.cleanup()
