from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def update_map(section, line, maps, reversed ):
    if section not in maps:
        maps[section] = {}
        reversed[section] = {}
    dest_start, source_start, length = line.split()
    maps[section][(int(source_start), int(source_start) + int(length))] = int(dest_start) - int(source_start)
    reversed[section][(int(dest_start), int(dest_start) + int(length))] = int(source_start) - int(dest_start)
    return maps, reversed


def condense_map(maps):
    res = {}
    for section, map in maps.items():
        for (lower, upper), offset in map.items():
            for (existing_lower, existing_upper), existing_offset in res.items():
                if existing_upper + existing_offset > lower or existing_lower + existing_offset <= upper:
                    del res[(existing_lower, existing_upper)]
                    if existing_lower + existing_offset < lower:
                        res[(existing_lower, lower - existing_offset)] = existing_offset
                        if existing_upper + existing_offset < upper:
                            res[(lower - existing_offset + 1, existing_upper)] = existing_offset + offset
                            res[(existing_upper + 1, upper + existing_offset)] = offset
                        else:
                            res[(upper - existing_offset + 1, existing_upper)] = offset
                            res[(lower - existing_offset, upper - existing_offset)] = existing_offset + offset
                    elif existing_upper + existing_offset > upper: # overlapping on upper end
                        res[(upper - existing_offset, existing_upper)] = existing_offset
                        if existing_lower + existing_offset:
                           pass
                else:
                   res[(lower, upper)] = offset



def compute(s: str) -> int:
    lines = s.splitlines()
    tmp = lines[0].split(':')[1].split()
    seeds = []
    for i in range(0,len(tmp),2):
        seeds += [(int(tmp[i]), int(tmp[i]) + int(tmp[i+1]) -1)]
    section = None
    maps = {}
    reversed = {}
    for line in lines[1:]:
        if not line:
            continue
        if line[0].isdigit():
            maps, reversed = update_map(section, line, maps, reversed)
        elif line[0].isalpha():
            section = line.split(' map')[0]
    # TODO: implement solution here!
    res = []
    reversed_steps = ['humidity-to-location', 'temperature-to-humidity', 'light-to-temperature', 'water-to-light', 'fertilizer-to-water', 'soil-to-fertilizer', 'seed-to-soil']
#    condensed_map = condense_map(maps)
    cnt = 46
    while True:
        curr = cnt
        for key in reversed_steps:
            map = reversed[key]
            for (lower, upper), offset in map.items():
                if curr>=lower and curr <= upper:
                    curr = curr + offset
                    break
        for lower_seed, upper_seed in seeds:
            if curr >=lower_seed and curr <= upper_seed:
                return cnt
        cnt += 1
    for seed in seeds:
        curr = int(seed)
        for map in maps.values():
            for (lower, upper), offset in map.items():
                if curr>=lower and curr <= upper:
                    curr = curr + offset
                    break
        res.append(curr)
    return min(res)


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
