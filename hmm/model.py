class HMM():
    def __init__(self, states, emissions, transitions):
        self.states = states
        self.emissions = emissions
        self.transitions = transitions

    def sequence_propability(self, sequence):
        pass

    def states_for_sequence(self, sequence):
        T = [{}]
        T[0] = {state: self.emissions[state][sequence[0]] * p for state, p in self.states.items()}
        path = {state: [state] for state in self.states}

        for s in sequence:
            T.append({})
            new_path = {}
            for new_state in self.states:
                T[-1][new_state], max_state = max([(T[-2][current_state]
                                                   * self.transitions[current_state][new_state]
                                                   * self.emissions[new_state][s], current_state) for current_state in self.states])
                new_path[new_state] = path[max_state] + [new_state]

            path = new_path

        print T
        print path

    def train(self, *sequences):
        pass
