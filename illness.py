from hmm import model


states = {'Healthy': 0.6, 'Fever': 0.4}

transitions = {
   'Fever' : {'Fever': 0.7, 'Healthy': 0.3},
   'Healthy' : {'Fever': 0.4, 'Healthy': 0.6},
   }

emissions = {
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   }

#hmm = model.HMM(states.keys(), ['normal', 'cold', 'dizzy'], [0.6, 0.4], emissions=[[0.5, 0.4, 0.1], [0.1, 0.3, 0.6]], transitions=[[0.6, 0.4], [0.3, 0.7]])
hmm = model.HMM(states.keys(), ['normal', 'cold', 'dizzy'])

seq = ['normal', 'cold', 'dizzy']
#print hmm.states_for_sequence(['normal', 'cold', 'dizzy'])
#print hmm.sequence_probability(['normal', 'cold', 'dizzy', 'dizzy'])
#print hmm.viterbi(['normal', 'cold', 'dizzy'], states.keys(), states, transitions, emissions)

hmm.train(10,seq)
