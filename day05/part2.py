from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def update_map(section, line, maps):
    if section not in maps:
        maps[section] = {}
    dest_start, source_start, length = line.split()
    maps[section][(int(source_start), int(source_start) + int(length)-1)] = int(dest_start) - int(source_start)
    return maps

def compute(s: str) -> int:
    lines = s.splitlines()
    tmp = lines[0].split(':')[1].split()
    seeds = []
    for i in range(0,len(tmp),2):
        seeds += [(int(tmp[i]), int(tmp[i]) + int(tmp[i+1]) -1)]
    section = None
    maps = {}
    for line in lines[1:]:
        if not line:
            continue
        if line[0].isdigit():
            maps = update_map(section, line, maps)
        elif line[0].isalpha():
            section = line.split(' map')[0]

    unmapped = seeds
    for section, map in maps.items():
        next = []
        while len(unmapped) > 0:
            c_l, c_u = unmapped.pop()
            seen = False
            for (lower, upper), offset in map.items():
                if c_u < lower or c_l > upper:
                    continue
                if c_l >= lower and c_u <= upper:
                    next.append((c_l + offset, c_u + offset))
                    seen=True
                    break
                elif c_u > upper and c_l >= lower:
                    next.append((c_l + offset, upper+offset))
                    unmapped.append((upper+1, c_u))
                    seen = True
                elif c_l < lower and c_u <= upper:
                    next.append((lower+offset, c_u+offset))
                    unmapped.append((c_l, lower-1))
                    seen = True
                    break
                else:
                    next.append((lower+offset, upper+offset))
                    unmapped.append((upper+1, c_u))
                    unmapped.append((c_l+1, lower))
                    seen = True
                    break
            if not seen:
                next.append((c_l, c_u))
        unmapped = next
    min_l = unmapped[0][0]
    for lower_location, _ in unmapped:
        min_l = min(lower_location, min_l)
    return min_l

INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 46


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
