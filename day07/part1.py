from __future__ import annotations

import argparse
import os.path

import pytest
from collections import Counter
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

rankings = {'A': 14, 'K': 13, 'Q':12, 'J':11, 'T':10}

def rank(hand):
    res = '.'
    for char in hand:
        val = rankings.get(char)
        if val is None:
            res = res + '0' + char
        else:
            res = res  + str(val)
    return res

def score(hand):
    cnt = Counter(hand)
    u_cnt = Counter(cnt.values())
    max_cnt = max(u_cnt)
    if max_cnt == 5:
        return '7' + rank(hand)
    if max_cnt == 4:
        return  '6' + rank(hand)
    if max_cnt == 3:
        if 2 in u_cnt:
            return '5' + rank(hand)
        return '4' + rank(hand)
    if u_cnt[2] == 2:
        return '3' + rank(hand)
    if 2 in u_cnt:
        return '2' + rank(hand)
    return '1' + rank(hand)

def compute(s: str) -> int:
    lines = s.splitlines()

    hands = []
    for row_num, line in enumerate(lines):
        hands.append((score(line.split()[0]),
                          int(line.split()[1])
, line.split()[0]))
    hands.sort(key = lambda x: x[0])
    return sum(e*bid for e, (_,bid,_) in enumerate(hands, 1))


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


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
