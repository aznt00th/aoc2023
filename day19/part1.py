from __future__ import annotations

import argparse
import os.path

import pytest
import json
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Part():
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def __repr__(self):
        return(f'[x={self.x:=}, m={self.m:=}, a={self.a:=}, s={self.s:=}]')

    def sum(self):
        return self.x + self.m + self.a + self.s

    def get_by_str(self, s):
        if s == 'x':
            return self.x
        if s == 'm':
            return self.m
        if s == 'a':
            return self.a
        if s == 's':
            return self.s



def check_rule(test, part):
    if test == '_':
        return True
    if test[1] == '>':
        return part.get_by_str(test[0]) > int(test[2:])
    elif test[1] == '<':
        return part.get_by_str(test[0]) < int(test[2:])
    else:
        raise Exception(f'unknown comp value {test}')


def format_str_to_dict(s: str):
    for char in 'xmas':
        s = s.replace(char, '"' + char + '"')
    return json.loads(s.replace('=', ':'))

def compute(s: str) -> int:
    lines = s.splitlines()
    start = True
    mappings = {}
    parts = []
    for row_num, line in enumerate(lines):
        curr_parts = []
        if len(line) == 0:
            start = False   
            continue
        if start:
            rule_name, rules = line.split('{')[0], line.split('{')[1]
            mappings[rule_name] = []
            for rule in rules.split(','):
                test = rule.split(':')[0]
                dest = rule.split(':')[-1]
                if test == dest:
                    test = '_'
                    dest = dest[:-1]
                mappings[rule_name].append((test, dest))
        else:
            parts.append(Part(**format_str_to_dict(line)))
    tot = 0
    for part in parts:
        #print(part)
        completed = False
        curr = 'in'
        while True:
            rules = mappings[curr]
            for rule in rules:
                if check_rule(rule[0], part):
                    dest = rule[1]
                    if dest == 'A':
                        tot += part.sum()
                        completed = True
                    elif dest == 'R':
                        completed = True
                    curr = dest
                    break
            if completed:
                break
        if completed:
            continue
    return tot


INPUT_S = '''\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
EXPECTED = 19114


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
