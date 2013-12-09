from hmm import model


states = {'C+': 0.125, 'G+': 0.125, 'C-': 0.125, 'G-': 0.125}

transitions = {
    'C+': {'C+': 0.351, 'G+': 0.257, 'C-': 0.018, 'G-': 0.014},
    'G+': {'C+': 0.323, 'G+': 0.352, 'C-': 0.017, 'G-': 0.019},
    'C-': {'C+': 0.03, 'G+': 0.008, 'C-': 0.27, 'G-': 0.071},
    'G-': {'C+': 0.025, 'G+': 0.03, 'C-': 0.225, 'G-': 0.27},
   }

emissions = {
   'C+' : {'C': 1, 'G': 0},
   'G+' : {'C': 0, 'G': 1},
   'C-' : {'C': 1, 'G': 0},
   'G-' : {'C': 0, 'G': 1},
   }

hmm = model.HMM(states, ['C', 'G'], transitions, emissions)
print hmm.prefix(['C', 'G', 'C', 'G'])
print hmm.suffix(['C', 'G', 'C', 'G'])
