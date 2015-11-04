#!/usr/bin/env python
# encoding: utf-8

import requests


def parse_ruleset(url):
    ruleset = set()
    start = False
    response = requests.get(url)
    if response.status_code != 200:
        return ruleset

    for line in response.text.split("\n"):
        line = line.strip()

        if "[Rule]" in line:
            start = True
            continue
        elif "[" in line and "]" in line:
            start = False

        if not start:
            continue

        if not line:
            continue

        if line.startswith("//"):
            continue

        if "REJECT" in line or "DIRECT" in line or "FINAL" in line:
            continue

        ruleset.add(line.replace(" ", ""))

    return ruleset


ruleset = set().union(
    parse_ruleset("http://surge.pm/main.conf")
).union(
    parse_ruleset("https://gist.githubusercontent.com/jason5ng32/648597df6ca7da5aeb41/raw/e9a0024b4cb7425fef55d941b389a08745a17a52/surge_main.conf")
).union(
    parse_ruleset("https://gist.githubusercontent.com/Huangsir/ebe23f97448709351c26/raw/6346434903b4e70e16e7bfef62a614a424bdad39/surge.conf")
)
rules = sorted(list(ruleset))

content = ""
with open("config.txt") as fp:
    content = fp.read()

content += "[Rule]\n" + "\n".join(rules) + "\nFINAL,DIRECT\n"
print content
