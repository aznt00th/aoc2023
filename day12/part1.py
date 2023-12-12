from __future__ import annotations

import argparse
import os.path

import pytest
from itertools import product
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def comp(str, res, replace):
    tmp_s = ''
    cnt = 0
    for  char in str:
        if char != '?':
            tmp_s += char
        if char == '?':
            if replace[cnt]:
                tmp_s += '#'
            else:
                tmp_s += '.'
            cnt += 1
    tmp = [i for i in tmp_s.split('.') if i]
    if len(tmp) != len(res):
        return False
    for i, cnt in enumerate(res):
        if len(tmp[i]) != cnt:
            return False
    return True

def compute(s: str) -> int:
    lines = s.splitlines()
    res = 0
    for row_num, line in enumerate(lines):
        grid, real = line.split()
        real = [int(i) for i in real.split(',')]
        num_q = 0
        num_hash = 0
        for col_num, char in enumerate(grid):
            if char == '?':
                num_q +=1
            if char == '#':
                num_hash += 1
        attempts = product([0,1], repeat = num_q)
        for attempt in attempts:
            if sum(attempt) + num_hash != sum(real):
                continue
            res += comp(grid, real, attempt)
    # TODO: implement solution here!
    return res

INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 21


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
