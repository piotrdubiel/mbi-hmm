from hmm import model


states = {'Rainy': 0.6, 'Sunny': 0.4}

transitions = {
   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
   }

emissions = {
   'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
   'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
   }

hmm = model.HMM(states, ['clean', 'walk', 'walk'], transitions, emissions)
print hmm.prefix(['clean', 'walk', 'walk'])
print hmm.suffix(['clean', 'walk', 'walk'])
