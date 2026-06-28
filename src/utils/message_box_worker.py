"""
Prevent Python GIL error.

This is run as a subprocess from utils.safe_message_box
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from core.native_methods import NativeMethods

text = sys.argv[1]
title = sys.argv[2]
flags = int(sys.argv[3])

result = NativeMethods.message_box(text, title, flags)

print(result) # simple IPC; print verbatim to stdout
