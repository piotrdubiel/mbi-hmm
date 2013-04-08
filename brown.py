import json
import os
import glob
import re
from hmm import model


o = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
s = ['consonant', 'vowel']
hmm = model.HMM(s, o)

not_allowed = '[^{0}]'.format(''.join(o))
os.chdir('corpus')
lines = []
i = 0
for name in glob.glob('*'):
    print name
    if not os.path.isdir(name):
        f = open(name)
        lines.append([])
        if i > 100:
            break
        i += 1
        for line in f:
            lines[-1] += list(re.sub(not_allowed, '', line[15:].strip()))

print lines
import pdb; pdb.set_trace() ### XXX BREAKPOINT

for i in range(10):
    print('ITERTION {}'.format(i))
    for line in lines:
        hmm.train(None, line)
