from hmm.model import HMM
from dna import utils
import difflib

f = open('coli.fasta')
sequence = []
dna = ''
for line in f:
    if line[0] == '>':
        continue
    dna += line.strip()

dna = dna[:9996]
genes = utils.to_gene_sequence(dna)
states = list(set(genes))
obs = set([utils.translate(g) for g in states])
hmm = HMM(states, obs)
gene_count = {g: {h: 0.0 for h in states} for g in states}

for i, g in enumerate(genes[:-1]):
    gene_count[g][genes[i+1]] += 1.0


def normalize(value_dict):
    n = float(sum(value_dict.values()))
    return {k: v / n for k, v in value_dict.items()}

gene_count = {k: normalize(v) for k, v in gene_count.items()}
emissions = {g: {o: 1.0 if utils.translate(g) == o else 0.0 for o in obs} for g in states}
hmm.emissions = emissions
hmm.transitions = gene_count

end = 21
decoded = ''
while end <= len(dna):
    amino_acids = utils.translate(dna[end-21:end])
    decoded += ''.join(hmm.states_for_sequence(amino_acids)[1])
    diff = difflib.SequenceMatcher(a=decoded[end-21:end], b=dna[end-21:end])

    print '{0}% Done --- Quality: {1}'.format(end * 100.0 / len(dna), diff.ratio())
    end += 21

print len(decoded)
print len(dna)

for i, x in enumerate(decoded):
    print decoded[i], dna[i], decoded[i]==dna[i]
diff = difflib.SequenceMatcher(a=decoded, b=dna)
