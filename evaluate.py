from subprocess import call
from dna import utils
import matplotlib.pyplot as plt
import os

RESULTS = {}


def compare(filename_a, filename_b):
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

    return float(equal) / length


def execute(window):
    print('Window: {}'.format(window))
    output_file = 'decoded/{}.fasta'.format(window)
    if not os.path.exists(output_file):
        cmd = 'python hmm_decoder.py -o {} coli.model {} test_aa.fasta'.format(output_file, window)
        print cmd
        call(cmd, shell=True)
    RESULTS[window] = compare(output_file, 'test.fasta')
    print(RESULTS[window])


def graph():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(RESULTS.keys(), RESULTS.values())

    plt.savefig('foo.png')


for window in range(1, 10):
    execute(window)

for window in range(10, 150, 10):
    execute(window)

for window in range(150, 500, 50):
    execute(window)

for window in range(500, 1000, 100):
    execute(window)

graph()
