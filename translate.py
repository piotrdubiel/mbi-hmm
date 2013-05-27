"""DNA to Aminoacid translation

Usage:
    translate.py <dna_sequence> <output_file>

Options:
    -h --help               show this screen
"""
from __future__ import print_function
from docopt import docopt
from dna import utils


def process(in_filename, out_filename):
    in_file = open(in_filename)
    out_file = open(out_filename, 'w')

    header, sequence = utils.load(in_file)
    in_file.close()

    out_file.write(header + '\n')
    out_file.write('\n'.join(utils.prepare_subsequences(utils.translate(sequence), 80)))

    out_file.close()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='translate')

    process(arguments['<dna_sequence>'], arguments['<output_file>'])
