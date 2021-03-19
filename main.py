"""
Usage: python main.py grammar.txt string
"""
import sys
from itertools import product
from collections import defaultdict
import pdb

def print_and_exit():
    sys.stderr.write(__doc__ + "\n")
    sys.exit(1)

if len(sys.argv) != 3:
    print_and_exit()

w = sys.argv[2].strip()
if len(w) < 1:
    print_and_exit()
N = len(w)

atomic_rules = []
composite_rules = []
composite_righthands = set()

with open(sys.argv[1], "r") as r:
    for l in r.readlines():
        [left, right] = l.split()
        assert len(left) == 1
        assert 0 < len(right) < 3
        if len(right) == 1:
            atomic_rules.append( (left, right) )
        else:
            composite_rules.append( (left, (right[0], right[1])) )

table = []
for i in range(N):
    table.append( [None for _ in range(i)] + [defaultdict(list) for _ in range(i,N)] )
    #table.append( [None for _ in range(i)] + [set() for _ in range(i,N)] )

for (i, c) in enumerate(w):
    for (left, right) in atomic_rules:
        if c == right: table[i][i][left].append(i)

diag = 1
while diag < N:
    i = 0
    j = diag 
    while i < N and j < N:
        for k in range(i, j):
            for (cand_l, cand_r) in product(table[i][k], table[k+1][j]):
                for (left, right) in composite_rules:
                    #if (cand_l, cand_r) == right: table[i][j].add(left)
                    if (cand_l, cand_r) == right: table[i][j][left].append(k)
        i += 1
        j += 1
    diag += 1


def print_table(t):
    for i in range(len(t)):
        for j in range(len(t)):
            print(f"{i},{j}: {t[i][j]}")
print_table(table)
