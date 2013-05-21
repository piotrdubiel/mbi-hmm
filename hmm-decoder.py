"""HMM Aminoacid Decoder

Usage:
    hmm-decoder.py <model> [-o FILE] SEQUENCE

Options:
    -o FILE --output=FILE   save decoded sequence to file, default is stdout
    -h --help               show this screen
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='HMM Aminoacid Decoder')
    print(arguments)
