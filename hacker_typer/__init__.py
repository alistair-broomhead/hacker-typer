import sys, termios, tty

template = """
# python
>>> def get_char():
...     file_descriptor = sys.stdin.fileno()
...
...     old_settings = termios.tcgetattr(file_descriptor)
...     try:
...         tty.setraw(sys.stdin.fileno())
...         ch = sys.stdin.read(1)
...     finally:
...         termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
...     return ch
...

>>> ^D
#
"""

def get_char():
    file_descriptor = sys.stdin.fileno()

    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == '__main__':
    i = 0
    while True:
        get_char()
        print(template[i:i+3], end='', file=sys.stderr)
        sys.stderr.flush()
        i = i + 3
        if i > len(template)-2:
            i = 0
