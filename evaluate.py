from subprocess import call


for window in range(10, 500, 10):
    cmd = 'python hmm_decoder.py -o decoded/{}.fasta coli.model {} test.fasta'.format(window, window)
    print cmd
    call(cmd, shell=True)
