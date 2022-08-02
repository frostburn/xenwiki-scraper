from fractions import Fraction
import os
import re
import json

from utils import Soup

non_names = [
    "5-limit", "7-limit", "11-limit", "13-limit", "17-limit", "19-limit", "23-limit",
    "Rank-4 temperaments", "Rank five",
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
        line = line.split(":")[1].strip()
        return list(map(Fraction, line.replace(" ", ",").replace(",,", ",").split(",")))
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
                subgroup = try_parse_subgroup(contents)
            elif "comma" in lower:
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
                "commas": ",".join(map(str, commas)),
                "mapping": mapping,
                "generator": generator,
                "optimal": optimal,
                "badness": badness
            })

            last_name = current_name
        elif commas:
            print("failed subgroup", title, subtitle)
        elif subgroup:
            print("failed commas", title, subtitle)

with open("json/out.json", "w") as fp:
    json.dump({"temperaments": results}, fp)
