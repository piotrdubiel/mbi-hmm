"""HMM Aminoacid Model

Usage:
    hmm_generator.py <fasta_sequence> [FILE]

Arguments:
    FILE            output file, without output is printed to stdout

Options:
    -h --help       show this screen
"""
from docopt import docopt
from schema import Schema, Or, Use, SchemaError
from hmm.model import HMM, create_from_sequence
from dna import utils
import json
import sys


def validate(arguments):
    schema = Schema({
        '<fasta_sequence>': Use(open, error='<fasta_sequence> file should be readable'),
        'FILE': Or(None, str),
    })

    try:
        return schema.validate(arguments)
    except SchemaError as e:
        print('ERROR: {}'.format(e))
        print(__doc__)
        exit(1)


def process(sequence_file):
    header, sequence = utils.load(arguments['<fasta_sequence>'])
    gene_sequence = utils.to_gene_sequence(sequence)
    hmm = create_from_sequence(gene_sequence)
    print(json.dumps({'header': header, 'model': hmm.__dict__}, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='HMM Aminoacid Model')

    arguments = validate(arguments)

    # if output file provided, redirect stdout
    if arguments['FILE']:
        sys.stdout = open(arguments['FILE'], 'w')

    process(arguments['<fasta_sequence>'])

    sys.stdout.flush()
