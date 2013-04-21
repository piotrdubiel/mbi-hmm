from dna import utils

def translate_test():
    # Given
    bases = ['U', 'C', 'A', 'G']
    codons = [a+b+c for a in bases for b in bases for c in bases]
    amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
    codon_table = dict(zip(codons, amino_acids))

    # When
    def check_translation(gene, aminoacid):
        assert utils.translate(gene) == aminoacid

    # Then
    for gene, aminoacid in codon_table.items():
       yield check_translation, gene, aminoacid
        
