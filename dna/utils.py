TRANSLATION_TABLE = {
    'TTT': 'F',	'TCT': 'S',	'TAT': 'Y',	'TGT': 'C',
    'TTC': 'F',	'TCC': 'S',	'TAC': 'Y',	'TGC': 'C',
    'TTA': 'L',	'TCA': 'S',	'TAA': '*', 'TGA': '*',
    'TTG': 'L',	'TCG': 'S',	'TAG': '*',	'TGG': 'W',
    'CTT': 'L',	'CCT': 'P',	'CAT': 'H',	'CGT': 'R',
    'CTC': 'L',	'CCC': 'P',	'CAC': 'H',	'CGC': 'R',
    'CTA': 'L',	'CCA': 'P',	'CAA': 'Q',	'CGA': 'R',
    'CTG': 'L',	'CCG': 'P',	'CAG': 'Q',	'CGG': 'R',
    'ATT': 'I',	'ACT': 'T',	'AAT': 'N',	'AGT': 'S',
    'ATC': 'I',	'ACC': 'T',	'AAC': 'N',	'AGC': 'S',
    'ATA': 'I',	'ACA': 'T',	'AAA': 'K',	'AGA': 'R',
    'ATG': 'M', 'ACG': 'T',	'AAG': 'K',	'AGG': 'R',
    'GTT': 'V',	'GCT': 'A',	'GAT': 'D',	'GGT': 'G',
    'GTC': 'V',	'GCC': 'A',	'GAC': 'D',	'GGC': 'G',
    'GTA': 'V',	'GCA': 'A',	'GAA': 'E',	'GGA': 'G',
    'GTG': 'V',	'GCG': 'A',	'GAG': 'E',	'GGG': 'G'
}


def translate(sequence):
    genes = to_gene_sequence(sequence)
    return ''.join([TRANSLATION_TABLE[g] for g in genes])


def to_gene_sequence(sequence):
    marker = 3
    genes = []
    while marker <= len(sequence):
        genes.append(sequence[marker - 3:marker].upper().replace('U', 'T'))  # unify to DNA if RNA
        marker += 3

    return genes


def prepare_subsequences(sequence, window_size):
    return [sequence[i:i + window_size] for i in range(0, len(sequence), window_size)]


def load(sequence_file):
    sequence = ''
    for line in sequence_file:
        if line[0] == '>':
            header = line.strip()
        else:
            sequence += line.strip()

    return (header, sequence)
