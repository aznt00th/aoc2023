from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    res = 0
    for line in lines:
        diffs = []
        numbers = [int(i) for i in line.split()]
        diffs.append(numbers)
        if not all([i==0 for i in numbers]):
            curr = numbers
            while True:
                diff = [curr[i+1] - curr[i] for i in range(len(curr) -1 )]
                diffs.append(diff)
                if all([i==0 for i in diff]):
                    break
                curr = diff
        last_vals = [i[-1] for i in diffs]
        res += sum(last_vals)
    return res


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 114


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
