from hmm.model import HMM
from collections import defaultdict

def translate(gene):
    if gene[0].upper() == 'A':
        return 'T'
    elif gene[0].upper() == 'G':
        return 'A'
    elif gene[0].upper() == 'T':
        return 'F'
    else:
        return 'Y'

f = open('coli.txt')
sequence = []
dna = ''
for line in f:
    tokens = line.split()
    dna += ''.join(tokens[1:])

def genify(seq):
    marker = 3
    genes = []
    while marker <= len(seq):
        genes.append(seq[marker-3:marker].upper())
        marker += 3

    return genes

genes = genify(dna)
states = set(genes)
obs = set([translate(g) for g in states])

hmm = HMM(states, obs)
gene_count = {g: {h: 0 for h in states} for g in states}

for i, g in enumerate(genes[:-1]):
    if genes[i+1] not in gene_count[g]:
        gene_count[g][genes[i+1]] = 0
    gene_count[g][genes[i+1]] += 1

def normalize(d):
    n = sum(d.values())
    for g in d:
        d[g] /= n

gene_count = map(normalize, gene_count.values())
emissions = {g: {o: 1.0 if translate(g) == o else 0.0 for o in obs} for g in states}
hmm.emissions = emissions

print hmm.__dict__
