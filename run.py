#!/home/samuel/code/mouse-events/env/bin/python
import struct
import sys
import time
from pathlib import Path

import fcntl
from pyautogui import keyDown, keyUp, press
from ioctl_opt import IOC, IOC_READ

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


def EVIOCGNAME(length):
    return IOC(IOC_READ, ord('E'), 0x06, length)


def get_devices():
    paths = sorted([f for f in Path('/dev/input').iterdir() if f.name.startswith('event')],
                   key=lambda f: int(f.name.replace('event', '')))
    devices = []
    for f in paths:
        buffer = b'\0' * 512
        with f.open() as fd:
            name = fcntl.ioctl(fd, EVIOCGNAME(512), buffer)
            name = name[:name.find(b'\0')].decode()
        devices.append((str(f), name))
    return devices


def main(verbose_):
    def verbose(*args, **kwargs):
        verbose_ and print(*args, **kwargs)

    devs = get_devices()
    mouse_names = 'Logitech Performance MX', 'Logitech Unifying Device'
    dev = None
    devs_str = '\n'.join(f'  {file:>20}: {name}' for file, name in devs)
    verbose('devices:\n' + devs_str)
    for match in mouse_names:
        dev, dev_name = next(([file, name] for file, name in devs if match in name), (None, None))
        if dev:
            print(f'using: {dev} "{dev_name}"')
            break
    if not dev:
        print(f'no devices found: "{mouse_names}", devices:\n{devs_str}')
        sys.exit(1)
    try:
        last_event = None
        last_event_time = 0
        with open(dev, 'rb') as f:
            while True:
                event = f.read(EVENT_SIZE)
                if event:
                    _, _, type_, code, value = struct.unpack(FORMAT, event)
                    if verbose_ and (type_, code, value) != (0, 0, 0):
                        print(f'type: {type_} code: {code} value: {value}')
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
    main('--verbose' in sys.argv or '-v' in sys.argv)
