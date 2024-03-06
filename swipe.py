import subprocess
import time

def swipe():
    subprocess.check_output('adb shell input swipe 100 1500 500 1000 100',shell=True)
    # subprocess.check_output('adb shell input swipe  500 1000 100 1500 100',shell=True)

interval = 0.01
# interval = 0.5
# interval = 1
# interval = 3


while True:
    swipe()
    time.sleep(interval)

