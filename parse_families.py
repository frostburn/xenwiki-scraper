from fractions import Fraction
import os
import re
import json

from utils import Soup

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
MAX_COMPLEXITY = 9007199254740991

def toMonzo(value, preserve_fractions=True):
    value = value.strip()
    try:
        value = Fraction(value)
        n = value.numerator
        d = value.denominator
        result = []
        for prime in PRIMES:
            component = 0
            while n % prime == 0:
                n //= prime
                component += 1
            while d % prime == 0:
                d //= prime
                component -= 1
            result.append(component)
        if n != 1 or d != 1:
            print("Out of primes", value, n, d)
            raise ValueError("Out of primes")
        while result[-1] == 0:
            result.pop()
        if preserve_fractions and value.numerator <= MAX_COMPLEXITY and value.denominator <= MAX_COMPLEXITY:
            return value
        else:
            return result

    except ValueError:
        return list(map(int, value.strip("|[⟩>").replace(" ", ",").replace(",,", ",").split(",")))

non_names = [
    "5-limit", "7-limit", "11-limit", "13-limit","17-limit", "19-limit",
    "23-limit", "29-limit", "31-limit", "37-limit", "41-limit", "43-limit", "47-limit", "53-limit",

    "Rank-2 temperaments",
    "Rank-3 temperaments",
    "Rank-4 temperaments",
    "Rank-5 temperaments",

    "Subgroup temperaments",
    "Fractional subgroup temperaments",

    "Rank two",
    "Rank three",
    "Rank four",
    "Rank five",

    "Rank two temperaments",
    "Rank three temperaments",
    "Rank four temperaments",
    "Rank five temperaments",

    "No-31's 37-limit", "5-limit (university)", "5-limit (laconic)", "7-limit (squalentine)",
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
            line = line.replace("|", "[").replace("⟩", ">")
            cleaned = ""
            in_monzo = False
            for c in line:
                if c == "[":
                    in_monzo = True
                    cleaned += c
                elif c == ">":
                    in_monzo = False
                    cleaned += c
                elif in_monzo and c == ",":
                    pass
                else:
                    cleaned += c
            return list(map(toMonzo, cleaned.split(",")))
        return list(map(toMonzo, line.replace(" ", ",").replace(",,,", ",").replace(",,", ",").split(",")))
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

def stringify_commas(commas):
    result = []
    for comma in commas:
        if isinstance(comma, Fraction):
            result.append(str(comma))
        else:
            result.append(comma)
    return result

# Fixes Mercator
subgroups = {
    "Mercator": {None: "2.3.5"},
    "Schismerc": {None: "2.3.5.7"},
    "Cartography": {None: "2.3.5.7.11", "13-limit": "2.3.5.7.11.13"},
    "Pentacontatritonic": {None: "2.3.5.7.11", "13-limit": "2.3.5.7.11.13"},
    "Boiler": {None: "2.3.5.7.11"},
    "Joliet": {None: "2.3.5.7.11", "13-limit": "2.3.5.7.11.13"},
}

directories = [
    "downloads/chromatic_realms",
    "downloads/clans",
    "downloads/collections",
    "downloads/families"
]
filenames = ["downloads/Chromatic_pairs.html"]
for directory in directories:
    for filename in os.listdir(directory):
        if "Marveltwin" in filename:
            continue
        base, ext = os.path.splitext(filename)
        if ext != ".html":
            continue
        filenames.append(os.path.join(directory, filename))

# Marveltwin parsed manually
results = [
    {
        "title": "Marveltwin",
        "subtitle": "Rank five",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": None
    },
    {
        "title": "Marveltwin",
        "subtitle": "225/224",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "225/224"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.668",
    },
    {
        "title": "Marveltwin",
        "subtitle": "364/363",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "364/363"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.011",
    },
    {
        "title": "Marveltwin",
        "subtitle": "441/440",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "441/440"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.037",
    },
    {
        "title": "Marveltwin",
        "subtitle": "169/168",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "169/168"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 2.975",
    },
    {
        "title": "Marveltwin",
        "subtitle": "540/539",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "540/539"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.281",
    },
    {
        "title": "Marveltwin",
        "subtitle": "352/351",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "352/351"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.434",
    },
    {
        "title": "Marveltwin",
        "subtitle": "625/624",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "625/624"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^6 * Badness: 3.563",
    },
    {
        "title": "Portending",
        "subtitle": None,
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "364/363", "441/440"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^5 * Badness: 62.715",
    },
    {
        "title": "Marvel",
        "subtitle": "Hecate",
        "subgroup": "2.3.5.7.11.13",
        "commas": ["225/224", "325/324", "385/384"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^5 * Badness: 72.113",
    },
    {
        "title": "Sumatra",
        "subtitle": None,
        "subgroup": "2.3.5.7.11.13",
        "commas": ["325/324", "385/384", "625/624"],
        "mapping": None,
        "generator": None,
        "optimal": None,
        "badness": "10^5 * Badness: 68.005",
    },
]

def is_non_name(name):
    return name in non_names or "." in name or re.match(r"\d+/\d+", name)

for filename in filenames:
    print("...Opening", filename)
    with open(filename, "r") as fp:
        soup = Soup(fp)

    last_name = None
    header_name = None
    header_level = "h9"
    for headline in soup.find_all(class_="mw-headline"):
        if headline.string is None:
            continue
        headline_level = getattr(headline.parent, "name")
        name = headline.string.strip()
        subtitle = None
        if last_name and is_non_name(name):
            title = last_name
            subtitle = name
        elif headline_level > header_level:
            title = header_name
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
        if not subgroup:
            subgroup = try_parse_subgroup(subgroups.get(title, {}).get(subtitle))
        if subgroup and commas:
            results.append({
                "title": title,
                "subtitle": subtitle,
                "subgroup": ".".join(map(str, subgroup)),
                "commas": stringify_commas(commas),
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

        if is_non_name(name):
            header_level = "h9"
            header_name = None
        elif headline_level <= header_level:
            header_level = headline_level
            header_name = name

with open("json/out.json", "w") as fp:
    json.dump({"temperaments": results}, fp)
