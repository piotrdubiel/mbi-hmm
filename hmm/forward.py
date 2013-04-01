P = [0.9, 0.1]

A = [[0.6, 0.4], [0.0, 1.0]]

B = [[0.8, 0.2], [0.0, 1.0]]

def sequence_probability(seq, P, A, B):
    a = alfa_pass(seq, P, A, B)
    return sum(a[-1])

def alfa_pass(seq, P, A, B):
    N = len(P)
    a = [[p * B[i][seq[0]] for i, p in enumerate(P)]]

    for i, s in enumerate(seq[1:]):
        a.append([])
        a[-1] = [sum([a[i][state] * A[state][new_state] for state in range(N)]) * B[new_state][s] for new_state in range(N)]

    return a

seq = [1,1,1]
a = sequence_probability([1, 1, 1], P, A, B)
