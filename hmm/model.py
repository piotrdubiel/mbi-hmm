from math import log, exp
import random


class HMM():
    def __init__(self, states, observations, start=None, transitions=None, emissions=None):
        random.seed()

        if start:
            self.states = {state: start[i] for i, state in enumerate(states)}
        else:
            self.states = {state: 1.0 / len(states) for state in states}

        self.observations = observations

        if emissions:
            self.emissions = {state: {observation: emissions[i][j] for j, observation in enumerate(self.observations)}
                              for i, state in enumerate(self.states)}
        else:
            self.emissions = {state: {observation: random.random() / len(self.observations) for j, observation in enumerate(self.observations)}
                              for i, state in enumerate(self.states)}

        if transitions:
            self.transitions = {current_state: {new_state: transitions[i][j] for j, new_state in enumerate(self.states)}
                                for i, current_state in enumerate(self.states)}
        else:
            self.transitions = {current_state: {new_state: random.random() / len(self.states) for j, new_state in enumerate(self.states)}
                                for i, current_state in enumerate(self.states)}

    def states_for_sequence(self, sequence):
        T = [{}]
        T[0] = {state: log(p * self.emissions[state][sequence[0]]) for state, p in self.states.items()}
        path = {state: [state] for state in self.states}

        for s in sequence[1:]:
            T.append({})
            new_path = {}
            for new_state in self.states:
                T[-1][new_state], max_state = max([(T[-2][current_state]
                                                   + log(self.transitions[current_state][new_state])
                                                   + log(self.emissions[new_state][s]), current_state) for current_state in self.states])
                new_path[new_state] = path[max_state] + [new_state]

            path = new_path

        (prob, max_state) = max([(T[-1][state], state) for state in self.states])
        return (exp(prob), path[max_state])

    def train(self, iterations, *sequences):
        last_prob = 0
        i = 0
        print iterations
        while True:
            i += 1
            for sequence in sequences:
                (a, c) = self._alfa_pass(sequence)
                b = self._beta_pass(sequence, c)
                (g, G) = self._gamma_pass2(sequence, a, b)

                self.states = {state: g[0][state] for state in self.states}
                self.transitions = {current_state: {new_state:
                                                    sum([Y[current_state][new_state] for Y in G])
                                                    / sum([y[current_state] for y in g])
                                                    for new_state in self.states}
                                    for current_state in self.states}

                self.emissions = {state: {observation: sum([y[state] for i, y in enumerate(g) if sequence[i] == observation]) / sum([y[state] for y in g])
                                          for observation in self.observations}
                                  for state in self.states}

                prob = -sum([log(x) for x in c])
                print(i, prob)
            if prob < last_prob or i <= iterations:
                last_prob = prob
            else:
                break

    def viterbi(self, obs, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}

        # Initialize base cases (t == 0)
        for y in states:
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
            path[y] = [y]

        # Run Viterbi for t > 0
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}

            for y in states:
                (prob, state) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            # Don't need to remember the old paths
            path = newpath

        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
        return (prob, path[state])

    def sequence_probability(self, sequence):
        a = self._alfa_pass2(sequence)
        return sum(a[-1].values())

    def _alfa_pass2(self, sequence):
        a = [{state: p * self.emissions[state][sequence[0]] for state, p in self.states.items()}]
        for i, s in enumerate(sequence[1:]):
            a.append({})
            a[-1] = {new_state: sum([a[i][state] * self.transitions[state][new_state] for state in self.states]) * self.emissions[new_state][s] for new_state in self.states}

        return a

    def _alfa_pass(self, sequence):
        a = [{state: p * self.emissions[state][sequence[0]] for state, p in self.states.items()}]
        c = [sum(a[0].values())]
        a[0] = {state: a[0][state] / c[0] for state in self.states}

        for i, s in enumerate(sequence[1:]):
            a.append({})
            a[-1] = {new_state: sum([a[i][state] * self.transitions[state][new_state] for state in self.states]) * self.emissions[new_state][s] for new_state in self.states}
            c.append(sum(a[-1].values()))
            a[-1] = {state: a[-1][state] / c[-1] for state in self.states}

        return a, c

    def _beta_pass2(self, sequence):
        b = [{state: 1.0 for state in self.states}]

        for i, s in enumerate(sequence[-1:0:-1]):
            b.append({})
            b[-1] = {state: sum([self.transitions[state][new_state] * self.emissions[new_state][s] * b[-2][new_state] for new_state in self.states]) for state in self.states}
        b.reverse()
        return b

    def _beta_pass(self, sequence, c):
        b = [{state: c[-1] for state in self.states}]

        for i, s in enumerate(sequence[-1:0:-1]):
            b.append({})
            b[-1] = {state: sum([self.transitions[state][new_state] * self.emissions[new_state][s] * b[-2][new_state] for new_state in self.states]) / c[i] for state in self.states}
        b.reverse()
        return b

    def _gamma_pass2(self, sequence, a, b):
        g = []
        G = []
        for i, s in enumerate(sequence[:-1]):
            d = sum([sum([a[i][current_state] * self.transitions[current_state][new_state] * self.emissions[new_state][s] * b[i + 1][new_state]
                     for new_state in self.states])
                    for current_state in self.states])
            G.append({})
            G[-1] = {current_state: {new_state:
                                     a[i][current_state]
                                     * self.transitions[current_state][new_state]
                                     * self.emissions[new_state][s]
                                     * b[i + 1][new_state]
                                     / d
                                     for new_state in self.states}
                     for current_state in self.states}

            g.append({})
            g[-1] = {state: sum(G[-1][state].values()) for state in self.states}

        P = sum(a[-1].values())
        g.append({state: a[-1][state] / P for state in self.states})

        return g, G

    def _gamma_pass(self, sequence, a, b):
        g = []
        G = []
        for i, s in enumerate(sequence[:-1]):
            d = sum([sum([a[i][current_state] * self.transitions[current_state][new_state] * self.emissions[new_state][s] * b[i + 1][new_state]
                     for new_state in self.states])
                    for current_state in self.states])
            G.append({})
            G[-1] = {current_state: {new_state:
                                     a[i][current_state]
                                     * self.transitions[current_state][new_state]
                                     * self.emissions[new_state][s]
                                     * b[i + 1][new_state]
                                     / d
                                     for new_state in self.states}
                     for current_state in self.states}

            g.append({})
            g[-1] = {state: sum(G[-1][state].values()) for state in self.states}

        return g, G
