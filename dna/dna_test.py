from dna import utils
from nose.tools import with_setup
import os


def translate_test():
    # Given
    bases = ['U', 'C', 'A', 'G']
    codons = [a + b + c for a in bases for b in bases for c in bases]
    amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
    codon_table = dict(zip(codons, amino_acids))

    # When
    def check_translation(gene, aminoacid):
        assert utils.translate(gene) == aminoacid

    # Then
    for gene, aminoacid in codon_table.items():
        yield check_translation, gene, aminoacid


def prepare_subsequences_test():
    # Given
    sequence = 'AAAGGGCCCU'

    # When
    subseq = utils.prepare_subsequences(sequence, 3)

    # Then
    assert len(subseq) == 4
    assert subseq[0] == 'AAA'
    assert subseq[1] == 'GGG'
    assert subseq[2] == 'CCC'
    assert subseq[3] == 'U'


def setup_file():
    f = open('test.tmp', 'w')
    f.write('>header\n')
    f.write('AGCT')
    f.write('GC')
    f.close()


def cleanup_file():
    os.remove('test.tmp')


@with_setup(setup_file, cleanup_file)
def load_test():
    # Given
    f = open('test.tmp')

    # When
    header, sequence = utils.load(f)
    f.close()

    # Then
    assert header == '>header'
    assert sequence == 'AGCTGC'
