import re
import struct
import sys
import time

from pyautogui import keyDown, keyUp, press

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)


def move(direction):
    keyDown('ctrl')
    keyDown('alt')
    press(direction)
    keyUp('ctrl')
    keyUp('alt')


def left():
    move('left')


def right():
    move('right')


def zoom():
    time.sleep(0.05)  # god knows why this is necessary, but it is
    keyDown('winleft')
    press('s')
    keyUp('winleft')



CODES = {
    (2, 6, 2**32 - 1): left,
    (2, 6, 1): right,
    # (1, 280, 0): zoom,
    (1, 280, 1): zoom,
}


def get_devices():
    with open('/proc/bus/input/devices') as f:
        text = f.read()

    matches = re.findall(r'N: Name="(.+?)"\nP: .*\nS: .*input(\d+)', text)
    return dict(matches)


def main():
    devs = get_devices()
    mouse_name = 'Logitech Performance MX'
    dev = devs.get(mouse_name)
    if not dev:
        print(f'device "{mouse_name}" not found')
        sys.exit(1)
    try:
        with open(f'/dev/input/event{dev}', 'rb') as f:
            while True:
                event = f.read(EVENT_SIZE)
                if event:
                    _, _, type_, code, value = struct.unpack(FORMAT, event)
                    event = CODES.get((type_, code, value))
                    event and event()
                    # event and print(event)
                    # if (type_, code, value) != (0, 0, 0):
                    #     print(f'type: {type_} code: {code} value: {value}')
                else:
                    time.sleep(0.01)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
