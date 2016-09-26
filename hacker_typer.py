import sys
import time
import curses
from pygments import lexers
from pygments.formatters import terminal256


class ListTermFormatter(terminal256.Terminal256Formatter):

    def format_unencoded(self, tokensource, tokenlist):
        for ttype, value in tokensource:
            highlighted = []
            not_found = True
            while ttype and not_found:
                try:
                    on, off = self.style_string[str(ttype)]

                    # Like TerminalFormatter, add "reset colors" escape sequence
                    # on newline.
                    spl = value.split('\n')
                    for line in spl[:-1]:
                        if line:
                            highlighted.append(on + line + off)
                        highlighted.append('\n')
                    if spl[-1]:
                        highlighted.append(on + spl[-1] + off)

                    not_found = False

                except KeyError:
                    ttype = ttype[:-1]

            if not_found:
                highlighted.append(value)
            tokenlist.append((value.replace('\n', '\r\n'), ''.join(highlighted).replace('\n', '\r\n')))


class HackerTyper(object):
    file_names = __file__,

    def process_file(self):
        text = self.template
        lexer = lexers.guess_lexer(text)
        formatter = ListTermFormatter(style='vim')
        tokens = lexer.get_tokens(text)
        formatted = []
        formatter.format(tokens, formatted)
        return formatted

    @classmethod
    def _use_file(cls, file_name):
        heading = 'vim ' + file_name
        template = open(file_name).read() + '\n'
        return heading, template

    def print_token(self, 
                    plain, 
                    highlighted='', 
                    delay=0.001
                    ):
        if not highlighted:
            highlighted = plain
        if plain in highlighted:
            j = highlighted.index(plain)
            k = j + len(plain)
        else:
            k = j = 0
        print(highlighted[:j], end='')
        for char in highlighted[j:k]:
            self.print_char(char)
            if delay:
                time.sleep(delay)
        print(highlighted[k:], end='')

    @classmethod
    def run(cls, screen):

        def refresh():
            screen.clear()
            screen.refresh()
            screen.clear()
            screen.refresh()

        while True:
            for file_name in cls.file_names:
                obj = cls(screen, file_name)
                for plain, highlighted in obj.process_file():
                    next(obj.chars)
                    obj.print_token(plain, highlighted)
                print('\n')

    @staticmethod
    def print_char(char):
        print(char, end='')
        sys.stdout.flush()

    def get_char(self):
        while True:
            ch = self.screen.getch()
            if ch == 27:
                self.screen.clear()
            else:
                yield ch

    def __init__(self, screen, file_name):
        curses.curs_set(2)
        self.screen = screen
        self.chars = self.get_char()
        self.heading, self.template = self._use_file(file_name)

if __name__ == '__main__':
    HackerTyper.file_names = sys.argv[1:] or HackerTyper.file_names
    try:
        curses.wrapper(HackerTyper.run)
    except KeyboardInterrupt:
        pass
