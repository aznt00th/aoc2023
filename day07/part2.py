from __future__ import annotations

import argparse
import os.path
from collections import Counter
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

rankings = {'A': 14, 'K': 13, 'Q':12, 'J':'00', 'T':10}

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
    counter = Counter(hand)
    unique_counter = Counter(counter.values())
    max_count = max(unique_counter)
    if max_count == 5:
        return '7' + rank(hand)
    if max_count == 4 and 'J' in hand:
        return '7' + rank(hand)
    if max_count == 4:
        return '6' + rank(hand)
    if max_count == 3:
        if counter['J'] == 3:
            if 2 in unique_counter:
                return '7' + rank(hand)
            return '6' + rank(hand)
        if counter['J'] == 2:
            return '7' + rank(hand)
        if 'J' in hand:
            return '6' + rank(hand)
        if 2 in unique_counter:
            return '5' + rank(hand)
        return '4' + rank(hand)
    if max_count == 2:
        if counter['J'] == 2:
            if unique_counter[2] == 2:
                return '6' + rank(hand)
            return '4' + rank(hand)
        if 'J' in hand: # at least 3 of a kind, maybe fh
            if unique_counter[2] == 2:
                return '5' + rank(hand)
            return '4' + rank(hand)
        if unique_counter[2] == 2:
            return '3' + rank(hand)
        return '2' + rank(hand)
    if 'J' in hand:
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
    res = 0
    for rnk, (val, bid, cards) in enumerate(hands):
        res += (1 + rnk) * bid
    return sum(e*bid for e, (_,bid,_) in enumerate(hands, 1))


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 5905


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
