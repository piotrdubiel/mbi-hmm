"""HMM Aminoacid Decoder

Usage:
    hmm_decoder.py [-o FILE] <model> <window_size> <sequence_file>

Arguments:
    model           Generated Hidden Markov Model
    window_size     Length of gene sequence window
    sequence_file   File in FASTA format with sequence of aminoacids

Options:
    -o FILE --output=FILE   save decoded sequence to file, default is stdout
    -h --help               show this screen
"""
from __future__ import print_function
from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError
from dna import utils
from hmm.model import HMM
import sys
import json


def validate(arguments):
    schema = Schema({
        '<model>': Use(open, error='<model> file should be readable'),
        '<window_size>': And(Use(int), lambda w: w > 0, error='<window_size> should be positive integer'),
        '<sequence_file>': Use(open, error='<sequence_file> file should be readable'),
        '--output': Or(None, str),
    })

    try:
        return schema.validate(arguments)
    except SchemaError as e:
        print('ERROR: {}'.format(e))
        print(__doc__)
        exit(1)


def process(model_file, sequence_file, window_size):
    model = json.loads(model_file.read())
    model_file.close()

    header, sequence = utils.load(sequence_file)
    sequence_file.close()

    print(header)
    hmm = HMM(**model['model'])

    subsequences = utils.prepare_subsequences(sequence, window_size)

    decoded = ''
    for seq in subsequences:
        decoded += ''.join(hmm.states_for_sequence(seq)[1])
        print('{} / {}'.format(len(decoded), 3 * len(sequence)), file=sys.stderr)

    lines = utils.prepare_subsequences(decoded, 80)
    for l in lines:
        print(l)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='HMM Aminoacid Decoder')

    arguments = validate(arguments)

    # if output file provided, redirect stdout
    if arguments['--output']:
        sys.stdout = open(arguments['--output'], 'w')

    process(arguments['<model>'], arguments['<sequence_file>'], arguments['<window_size>'])

    sys.stdout.flush()
