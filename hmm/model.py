from math import log, exp
from dna import utils
import random
import sys


class HMM():
    def __init__(self, states, observations, transitions=None, emissions=None):
        random.seed()

        if type(states) is dict:
            self.states = states
        elif type(states) is list:
            self.states = {state: 1.0 / len(states) for state in states}
        else:
            raise TypeError

        self.observations = list(observations)

        if emissions:
            self.emissions = {state: {observation: emissions[state][observation] for observation in self.observations}
                              for state in self.states}
        else:
            self.emissions = {state: {observation: 1.0 / len(self.observations) for observation in self.observations}
                              for state in self.states}

        if transitions:
            self.transitions = {current_state: {new_state: transitions[current_state][new_state] for new_state in self.states}
                                for current_state in self.states}
        else:
            self.transitions = {current_state: {new_state: 1.0 / len(self.states) for new_state in self.states}
                                for current_state in self.states}

    def states_for_sequence(self, sequence):
        T = [{}]
        T[0] = {state: self._safe_log(p * self.emissions[state][sequence[0]]) for state, p in self.states.items()}
        path = {state: [state] for state in self.states}
        for s in sequence[1:]:
            T.append({})
            new_path = {}
            for new_state in self.states:
                T[-1][new_state], max_state = max([(T[-2][current_state]
                                                   + self._safe_log(self.transitions[current_state][new_state])
                                                   + self._safe_log(self.emissions[new_state][s]),
                                                    current_state) for current_state in self.states])
                new_path[new_state] = path[max_state] + [new_state]

            path = new_path

        (prob, max_state) = max([(T[-1][state], state) for state in self.states])
        return (exp(prob), path[max_state])

    def train(self, iterations, sequence):
        last_prob = sys.maxint
        i = 0
        while True:
            i += 1
            (a, c) = self._alfa_pass(sequence)
            b = self._beta_pass(sequence, c)
            (g, G) = self._gamma_pass(sequence, a, b)

            self.states = {state: g[0][state] for state in self.states}
            self.transitions = {current_state: {new_state:
                                                sum([Y[current_state][new_state] for Y in G])
                                                / sum([y[current_state] for y in g])
                                                for new_state in self.states}
                                for current_state in self.states}

            self.emissions = {state: {observation: sum([y[state] for i, y in enumerate(g) if sequence[i] == observation]) / sum([y[state] for y in g])
                                        for observation in self.observations}
                                for state in self.states}

            prob = -sum([self._safe_log(x) for x in c])
            print(i, prob)
            if prob < last_prob:
                last_prob = prob
            else:
                break

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
            if c[-1] == 0:
                a[-1] = {state: 1.0 / len(self.states) for state in self.states}
                c[-1] = 1.0
            else:
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
            if d == 0:
                G[-1] = {current_state: {new_state: 1.0 / len(self.states)
                                         for new_state in self.states}
                        for current_state in self.states}
            else:
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

    def _safe_log(self, value):
        if value != 0.0:
            return log(value)
        else:
            return -sys.maxint

def create_from_sequence(sequence):
    states = list(set(sequence))
    observations = list(set([utils.translate(g) for g in states]))

    hmm = HMM(states, observations)

    gene_count = {g: {h: 0.0 for h in states} for g in states}

    for i, g in enumerate(sequence[:-1]):
        gene_count[g][sequence[i+1]] += 1.0

    def normalize(value_dict):
        n = float(sum(value_dict.values()))
        return {k: v / n for k, v in value_dict.items()}

    gene_count = {k: normalize(v) for k, v in gene_count.items()}
    emissions = {g: {o: 1.0 if utils.translate(g) == o else 0.0 for o in observations} for g in states}
    hmm.emissions = emissions
    hmm.transitions = gene_count

    return hmm
