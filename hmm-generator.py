"""HMM Aminoacid Model

Usage:
    hmm-generator.py <fasta_sequence> [FILE]

Arguments:
    FILE            output file, without output is printed to stdout

Options:
    -h --help       show this screen
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='HMM Aminoacid Model')
    print(arguments)
