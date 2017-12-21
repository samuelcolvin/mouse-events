#!/home/samuel/code/mouse-events/env/bin/python
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
REPEAT_TTL = 0.6


def get_devices():
    with open('/proc/bus/input/devices') as f:
        text = f.read()

    matches = re.findall(r'N: Name="(.+?)"\nP: .*\nS: .*input(\d+)', text)
    return dict(matches)


def main():
    devs = get_devices()
    mouse_names = 'Logitech Performance MX', 'Logitech Unifying Device'
    dev = None
    for name in mouse_names:
        dev = next((v for k, v in devs.items() if name in k), None)
        if dev:
            break
    if not dev:
        devs = '\n  '.join(devs)
        print(f'no devices found: "{mouse_names}", devices:\n{devs}')
        sys.exit(1)
    try:
        last_event = None
        last_event_time = 0
        with open(f'/dev/input/event{dev}', 'rb') as f:
            while True:
                event = f.read(EVENT_SIZE)
                if event:
                    _, _, type_, code, value = struct.unpack(FORMAT, event)
                    # if (type_, code, value) != (0, 0, 0):
                    #     print(f'type: {type_} code: {code} value: {value}')
                    event = CODES.get((type_, code, value))
                    if event:
                        now = time.time()
                        e_name = event.__name__
                        run = last_event != e_name or now > (last_event_time + REPEAT_TTL)
                        print(e_name, f'{now - last_event_time:0.2f}s', 'run' if run else '-')
                        if run:
                            event()
                            last_event = e_name
                            last_event_time = now
                else:
                    time.sleep(0.01)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
