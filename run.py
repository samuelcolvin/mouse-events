import time
import struct
import pyautogui

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)


def move(direction):
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('alt')
    pyautogui.press(direction)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('alt')


def left():
    move('left')


def right():
    move('right')


def zoom():
    pyautogui.press('winleft')


CODES = {
    (2, 6, 2**32 - 1): left,
    (2, 6, 1): right,
    (1, 280, 0): zoom,
}


try:
    with open('/dev/input/event6', 'rb') as f:
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
                time.sleep(0.1)
except KeyboardInterrupt:
    pass
