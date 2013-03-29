from forward import *


a = alfa_pass(seq, P, A, B)
def beta_pass(a, seq, P, A, B):
    N = len(P)
    b = [[1.0 for _ in P]]
    
    for i, s in enumerate(seq[-1:0:-1]):
        b.append([])
        b[-1] = [sum([A[state][new_state] * B[new_state][s] * b[-2][new_state] for new_state in range(N)]) for state in range(N)]
    b.reverse()
    return b

def gamma_pass(a, b):
    d = sum(a[-1])
    return map(lambda p: map(lambda x: x[0] * x[1], zip(p[0], p[1])), zip(a,b))

b = beta_pass(a, seq, P, A, B)
g = gamma_pass(a, b)
print g
for i, s in enumerate(g):
    m = max(s)
    print s.index(m)