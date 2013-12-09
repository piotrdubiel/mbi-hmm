from hmm import model

states = {'U': 0.5, 'N': 0.5}
observations = {'1', '2', '3', '4', '5', '6'}
transitions = {'U': {'U': 0.95, 'N': 0.05},
               'N': {'U': 0.1, 'N': 0.9}}
emissions = {'U': {'1': 0.167, '2': 0.167, '3': 0.167, '4': 0.167, '5': 0.167, '6': 0.167},
             'N': {'1': 0.1, '2': 0.1, '3': 0.1, '4': 0.1, '5': 0.1, '6': 0.5}}

hmm = model.HMM(states, observations, transitions, emissions)

seq = ['6', '1', '6', '6', '5', '6', '2', '1', '5', '1', '3', '4']
print hmm.prefix(seq)
for i, a in enumerate(hmm.suffix(seq)):
    print a, seq[i]

# >>> 0.0001096449669352258 * 0.95 * 0.167 + 3.0418475024501612e-05 * 0.05 * 0.1
