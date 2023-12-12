from __future__ import annotations

import argparse
import os.path
import pdb
import pytest
from itertools import product
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def g(memo, str, pos, seq_c, curr_seq_len, springs):
    key = (pos, seq_c, curr_seq_len)
    if key in memo:
        return memo[key]
    if pos == len(str):
        if seq_c == len(springs):
            res = 1
        else:
            res = 0
    elif str[pos]  == '#': 
        res = g(memo, str, pos + 1, seq_c, curr_seq_len +1, springs)
    elif seq_c == len(springs): # currently . or ?, forced to treat as .
        if curr_seq_len == 0:
            res = g(memo, str, pos + 1, seq_c, 0, springs)
        else:
            res = 0
    elif str[pos] == '.':
        if curr_seq_len == springs[seq_c]: # implicitly seq_c < len(springs)
            res = g(memo, str, pos+1, seq_c + 1, 0, springs)
        elif curr_seq_len == 0:
            res = g(memo, str, pos + 1, seq_c, 0, springs)
        else:
            res = 0
    else:
        hash_count = g(memo, str, pos + 1, seq_c, curr_seq_len + 1, springs)
        dot_count = 0
        if curr_seq_len == springs[seq_c]:
            dot_count = g(memo, str, pos+1, seq_c + 1, 0, springs)
        elif curr_seq_len == 0:
            dot_count = g(memo, str, pos + 1, seq_c, 0, springs)
        res = dot_count + hash_count
    memo[key] = res
    return res

def compute(s: str) -> int:
    lines = s.splitlines()
    res = 0
    for row_num, line in enumerate(lines):
        grid, real = line.split()
        real = [int(i) for i in real.split(',')]
        res += g({}, "?".join([grid for i in range(5)]) + ".", 0, 0, 0, real*5)
    # TODO: implement solution here!
    return res

INPUT_S = '''\
?..#?.??#?...??##??? 1,2,2,1,5
'''
EXPECTED = 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
