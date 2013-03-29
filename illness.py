import model


states = {'Healthy': 0.6, 'Fever': 0.4}

transitions = {
   'Fever' : {'Fever': 0.7, 'Healthy': 0.3},
   'Healthy' : {'Fever': 0.4, 'Healthy': 0.6},
   }

emissions = {
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   }

hmm = model.HMM(states, emissions, transitions)
hmm.states_for_sequence(['normal', 'cold', 'dizzy'])
