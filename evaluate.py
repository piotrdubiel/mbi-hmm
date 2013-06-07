from subprocess import call
from dna import utils
import matplotlib.pyplot as plt
import os

RESULTS = ([], [])

if not os.path.isdir('decoded'):
    os.mkdir('decoded')


def compare(filename_a, filename_b):
    a = open(filename_a)
    b = open(filename_b)

    _, sequence_a = utils.load(a)
    a.close()

    _, sequence_b = utils.load(b)
    b.close()

    return utils.compare(sequence_a, sequence_b)


def execute(window):
    print('Window: {}'.format(window))
    output_file = 'decoded/{}.fasta'.format(window)
    if not os.path.exists(output_file):
        cmd = 'python hmm_decoder.py -o {} coli.model {} test_aa.fasta'.format(output_file, window)
        print cmd
        call(cmd, shell=True)
    RESULTS[0].append(window)
    RESULTS[1].append(compare(output_file, 'test.fasta'))
    print(RESULTS[1][-1])


def graph():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(RESULTS[0], RESULTS[1])

    plt.savefig('graph.png')


for window in range(1, 10):
    execute(window)

for window in range(10, 150, 10):
    execute(window)

for window in range(150, 500, 50):
    execute(window)

for window in range(500, 1000, 100):
    execute(window)

graph()
