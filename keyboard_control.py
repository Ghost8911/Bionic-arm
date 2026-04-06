import serial
import keyboard
import time

# ── Change this to your ESP32 COM port ──
# Windows: "COM3" or "COM4" etc  (check Device Manager)
# Linux/Mac: "/dev/ttyUSB0" or "/dev/ttyACM0"
PORT = "COM3"
BAUD = 9600

print("Connecting to ESP32...")
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # wait for ESP32 to boot
print("Connected! Use keys to control the arm.")
print()
print("  W / S    →  Elbow up / down")
print("  A / D    →  Shoulder left / right")
print("  Q / E    →  Wrist left / right")
print("  O / C    →  Gripper open / close")
print("  SPACE    →  Center all servos")
print("  ESC      →  Quit")
print()

def send(cmd):
    ser.write(cmd.encode())
    time.sleep(0.05)
    if ser.in_waiting:
        print(ser.readline().decode().strip())

# Key repeat delay
REPEAT_DELAY = 0.12

keys = ['w','s','a','d','q','e','o','c','space']
last_time = {k: 0 for k in keys}

print("Press keys to move the arm. Press ESC to quit.")

while True:
    now = time.time()

    for k in keys:
        if keyboard.is_pressed(k):
            if now - last_time[k] > REPEAT_DELAY:
                last_time[k] = now
                if k == 'space':
                    send(' ')
                else:
                    send(k)

    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break

    time.sleep(0.01)

ser.close()
