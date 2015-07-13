from hmm import model

states = {'1': 0.2, '2': 0.8}

transitions = {'1': {'1': 0.5, '2': 0.5},
               '2': {'1': 0.3, '2': 0.7}}

emissions = {'1': {'N': 0.3, 'E': 0.7},
             '2': {'N': 0.8, 'E': 0.2}}

observations = ['N', 'E']

hmm = model.HMM(states, observations, transitions, emissions)

g, G = hmm.train(['N', 'N'])

print g
print G
