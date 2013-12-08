from math import log, exp
from dna import utils
import sys


class HMM():
    def __init__(self, states, observations, transitions=None, emissions=None):
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

    def decode(self, sequence):
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

    def _safe_log(self, value):
        if value != 0.0:
            return log(value)
        else:
            return -sys.maxint

    def prefix(self, sequence):
        T = [{state: self._safe_log(p * self.emissions[state][sequence[0]]) for state, p in self.states.items()}]
        for s in sequence[1:]:
            T.append({})
            for current_state in self.states:
                T[-1][current_state] = self._safe_log(self.emissions[current_state][s]) * sum([T[-2][prev_state] * self._safe_log(self.transitions[prev_state][current_state]) for prev_state in self.states])

        return T

    def suffix(self, sequence):
        T = [{state: 1.0 for state in self.states}]

        return T


def create_from_sequence(sequence):
    states = list(set(sequence))
    observations = list(set([utils.translate(g) for g in states]))

    hmm = HMM(states, observations)

    gene_count = {g: {h: 0.0 for h in states} for g in states}

    for i, g in enumerate(sequence[:-1]):
        gene_count[g][sequence[i + 1]] += 1.0

    def normalize(value_dict):
        n = float(sum(value_dict.values()))
        if n == 0:
            n = 1
        return {k: v / n for k, v in value_dict.items()}

    gene_count = {k: normalize(v) for k, v in gene_count.items()}
    emissions = {g: {o: 1.0 if utils.translate(g) == o else 0.0 for o in observations} for g in states}
    hmm.emissions = emissions
    hmm.transitions = gene_count

    return hmm
