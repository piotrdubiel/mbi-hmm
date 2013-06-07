from hmm.model import HMM, create_from_sequence
import sys


def init_test():
    # Given
    states = {'A': 0.6, 'B': 0.4}
    observations = ['1', '2', '3']
    transitions = {'A': {'A': 0.7, 'B': 0.3},
                   'B': {'A': 0.4, 'B': 0.6}}
    emissions = {'A': {'1': 0.5, '2': 0.4, '3': 0.1},
                 'B': {'1': 0.1, '2': 0.3, '3': 0.6}}

    # When
    hmm = HMM(states, observations, transitions, emissions)

    # Then
    assert hmm.states == states
    assert hmm.observations == observations
    assert hmm.transitions == transitions
    assert hmm.emissions == emissions


def states_for_sequence_test():
    # Given
    states = {'A': 0.6, 'B': 0.4}
    observations = ['1', '2', '3']
    transitions = {'A': {'A': 0.7, 'B': 0.3},
                   'B': {'A': 0.4, 'B': 0.6}}
    emissions = {'A': {'1': 0.5, '2': 0.4, '3': 0.1},
                 'B': {'1': 0.1, '2': 0.3, '3': 0.6}}

    # When
    hmm = HMM(states, observations, transitions, emissions)
    decoded = hmm.decode(['1', '2', '3'])

    # Then
    assert decoded[1] == ['A', 'A', 'B']


def safe_log_test():
    hmm = HMM({}, [])
    assert hmm._safe_log(0.0) == -sys.maxint


def create_from_sequence_test():
    # Given
    sequence = ['AAA', 'GGG', 'TTT', 'CCC']

    # When
    hmm = create_from_sequence(sequence)

    # Then
    assert len(hmm.states) == 4
    assert len(hmm.observations) == 4
    assert hmm.states.values() == [0.25, 0.25, 0.25, 0.25]
    assert 'K' in hmm.observations
    assert 'P' in hmm.observations
    assert 'F' in hmm.observations
    assert 'G' in hmm.observations
    assert hmm.transitions['AAA']['GGG'] == 1.0
    assert hmm.transitions['GGG']['TTT'] == 1.0
    assert hmm.transitions['TTT']['CCC'] == 1.0
    assert hmm.transitions['CCC']['AAA'] == 0.0
