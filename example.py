from hmm import model
states = ['s', 't']
obs = ['A', 'B']
P = [0.85, 0.15]
A = [[0.3, 0.7], [0.1, 0.9]]
B = [[0.4, 0.6], [0.5, 0.5]]

hmm = model.HMM(states, obs, P, A, B)
s1 = ['A', 'B', 'B', 'A']
s2 = ['B', 'A', 'B']
a = hmm._alfa_pass2(s1)
b = hmm._beta_pass2(s1)

(g, G) = hmm._gamma_pass2(s1, a, b)

hmm.train(10, s1)
