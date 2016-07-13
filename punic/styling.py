from __future__ import division, absolute_import, print_function

__all__ = ['styled', 'enabled']

from six.moves.html_parser import HTMLParser

from blessings import Terminal

# from .config import config

term = Terminal()


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.s = ''

        self.styles = {
            'err': term.red,
            'ref': term.yellow,
            'rev': term.bold,
            'cmd': term.cyan + term.underline,
            # 'sub': term.cyan,
            'echo': term.yellow,
        }

        self.style_stack = []

    def handle_starttag(self, tag, attrs):
        if tag in self.styles:
            self.style_stack.append(self.styles[tag])

    def handle_endtag(self, tag):
        if tag in self.styles:
            self.style_stack.pop()

    def handle_data(self, data):
        if enabled:
            self.apply()
        self.s += data

    def apply(self):
        self.s += term.normal
        for style in set(self.style_stack):
            self.s += style

# TODO: This is crap. Stop exposing it. Maybe put into logger instead?
enabled = True


def styled(s):
    parser = MyHTMLParser()
    parser.feed(s)
    return parser.s + term.normal

# '<head>***</head> Checkout out <title>SwiftLogging</title> at "<version>v1.0.1</version>"')
#
# # instantiate the parser and fed it some HTML
