#!/usr/bin/env python3
try:
    from pyautogui import click
except ImportError as e:
    raise ImportError("""
        You need to install PyAutoGUI, python-3xlib which it requires, and ioctl-opt:

            pip install python3-xlib --user
            pip install PyAutoGUI ioctl-opt --user

    """) from e

click(button='middle')
