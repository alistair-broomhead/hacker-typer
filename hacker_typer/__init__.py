import sys, termios, tty, random, time

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
    ch = sys.stdin.read(1)
    #print(repr(ch))
    if ch == '\04':
        raise EOFError()
    if ch == '\x1b':
        clear_screen()
    return ch

def clear_screen():
    print('\n'*1000)
    
def main():
    clear_screen()
    i = 0
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    colors = ['\033[9%dm' % i for i in range(10)]
    while True:
        sz = random.randint(3, 7)
        get_char()
        outstr = template[i:i+sz]
        for c in outstr:
            if c == " ":
                print(random.choice(colors),end='',file=sys.stderr)
            print(c, end='')
            sys.stdout.flush()
            time.sleep(0.1)
        i = i + sz
        if i > len(template)-(sz-1):
            i = 0
        if not random.randint(0, 400):
            clear_screen()



if __name__ == '__main__':
    file_descriptor = sys.stdin.fileno()

    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(sys.stdin.fileno())
        main()
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)