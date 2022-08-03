from fractions import Fraction
import os
import re
import json

from utils import Soup

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

class Monzo:
    def __init__(self, value):
        try:
            value = Fraction(value)
            n = value.numerator
            d = value.denominator
            self.value = []
            for prime in PRIMES:
                component = 0
                while n % prime == 0:
                    n //= prime
                    component += 1
                while d % prime == 0:
                    d //= prime
                    component -= 1
                self.value.append(component)
            if n != 1 or d != 1:
                print("Out of primes", value, n, d)
                raise ValueError("Out of primes")
            while self.value[-1] == 0:
                self.value.pop()

        except ValueError:
            self.value = list(map(int, value.strip("|[⟩>").replace(" ", ",").replace(",,", ",").split(",")))

non_names = [
    "5-limit", "7-limit", "11-limit", "13-limit", "17-limit", "19-limit", "23-limit", "29-limit", "31-limit", "37-limit", "41-limit", "43-limit", "47-limit", "53-limit",
    "Rank-4 temperaments", "Rank five", "No-31's 37-limit", "5-limit (university)", "5-limit (laconic)", "7-limit (squalentine)",
    "5-limit (supersharp)", "5-limit (avila)", "7-limit (Crusher)", "Subgroup temperament",
]

def string_contents(node):
    result = ""
    if hasattr(node, "children"):
        for child in node.children:
            result += string_contents(child)
    elif node.string:
        result += node.string
    return result


def try_parse_subgroup(line):
    try:
        if ":" in line:
            line = line.split(":")[1].strip()
        if line.lower() == "full 13-limit":
            return [Fraction(2), Fraction(3), Fraction(5), Fraction(7), Fraction(11), Fraction(13)]
        line = line.split(" ")[0].strip(".")
        if "." in line:
            return list(map(Fraction, line.split(".")))
    except Exception:
        return None

def try_parse_commas(line):
    try:
        line = line.split(":")[1].strip().strip(" (mirkwai)(hemimean)")
        if "=" in line:
            line = line.split("=")[1].strip().replace(" ", "")
        elif "⟩" in line or ">" in line:
            line = line.replace("|", "[")
            return list(map(Monzo, line.split(", [")))
        return list(map(Monzo, line.replace(" ", ",").replace(",,,", ",").replace(",,", ",").split(",")))
    except Exception:
        return None

# TODO: Fix
def parse_mapping(line):
    print(line)
    result = []
    line = line.replace("[", "").replace("⟨", "").replace("<", "").replace(",", "").strip("]")
    for vec in line.split("]"):
        result.append(list(map(Fraction, vec.split())))
    return result

# TODO: Fix Marveltwin
# TODO: Fix Mercator

directories = [
    "downloads/chromatic_realms",
    "downloads/clans",
    "downloads/collections",
    "downloads/families"
]
filenames = ["downloads/Chromatic_pairs.html"]
for directory in directories:
    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext != ".html":
            continue
        filenames.append(os.path.join(directory, filename))

results = []

for filename in filenames:
    print("...Opening", filename)
    with open(filename, "r") as fp:
        soup = Soup(fp)

    last_name = None
    for headline in soup.find_all(class_="mw-headline"):
        name = headline.string
        subtitle = None
        if last_name and (name in non_names or "." in name or re.match(r"\d+/\d+", name)):
            title = last_name
            subtitle = name
        else:
            title = name
            current_name = name
        sg = None
        cl = None
        subgroup = None
        commas = None
        mapping = None
        generator = None
        optimal = None
        badness = None
        node = headline.parent.next_sibling
        while node and getattr(node, "name", None) not in ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"]:
            contents = string_contents(node).strip()
            if "NewPP limit report" in contents:
                node = node.next_sibling
                continue
            if "Transclusion expansion time report" in contents:
                node = node.next_sibling
                continue
            lower = contents.lower()
            if "subgroup" in lower and not isinstance(subgroup, list):
                sg = contents
                subgroup = try_parse_subgroup(contents)
            elif "comma" in lower and "comma pump" not in lower:
                cl = contents
                commas = try_parse_commas(contents)
            elif "mapping" in lower:
                mapping = contents
            elif "generator" in lower:
                generator = contents
            elif "optimal" in lower:
                optimal = contents
            elif "badness" in lower:
                badness = contents
            node = node.next_sibling
        if subgroup and commas:
            results.append({
                "title": title,
                "subtitle": subtitle,
                "subgroup": ".".join(map(str, subgroup)),
                "commas": list(map(lambda m: m.value, commas)),
                "mapping": mapping,
                "generator": generator,
                "optimal": optimal,
                "badness": badness
            })

            last_name = current_name
        elif commas:
            print("failed subgroup", title, subtitle, sg)
        elif subgroup:
            print("failed commas", title, subtitle, cl)

with open("json/out.json", "w") as fp:
    json.dump({"temperaments": results}, fp)
