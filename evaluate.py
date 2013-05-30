from subprocess import call

for window in range(1, 10):
    cmd = 'python hmm_decoder.py -o decoded/{}.fasta coli.model {} test_aa.fasta'.format(window, window)
    print cmd
    call(cmd, shell=True)

for window in range(10, 150, 10):
    cmd = 'python hmm_decoder.py -o decoded/{}.fasta coli.model {} test_aa.fasta'.format(window, window)
    print cmd
    call(cmd, shell=True)

for window in range(150, 500, 50):
    cmd = 'python hmm_decoder.py -o decoded/{}.fasta coli.model {} test_aa.fasta'.format(window, window)
    print cmd
    call(cmd, shell=True)
