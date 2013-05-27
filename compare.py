"""Compare

Usage:
    compare.py SEQ1 SEQ2

Options:
    -h --help               show this screen
"""
from __future__ import print_function
from docopt import docopt
from dna import utils


def process(filename_a, filename_b):
    a = open(filename_a)
    b = open(filename_b)

    _, sequence_a = utils.load(a)
    a.close()

    _, sequence_b = utils.load(b)
    b.close()

    equal = 0
    length = min((len(sequence_a), len(sequence_b)))
    for i in range(length):
        if sequence_a[i] == sequence_b[i]:
            equal += 1

    print(equal)
    print(float(equal) / length)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='translate')

    process(arguments['SEQ1'], arguments['SEQ2'])
