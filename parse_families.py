from fractions import Fraction
import os
import re

from utils import Soup

non_names = [
    "5-limit", "7-limit", "11-limit", "13-limit", "17-limit", "19-limit", "23-limit",
    # "2.5.7.11", "2.5.7.11.13", "2.5.7.11.13.17", "2.3.7.11.13 subgroup", "2.3.5.17.19"
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
            line = line.split(":")[1].strip().split(" ")[0].strip(".")
        if "." in line:
            return list(map(Fraction, line.split(".")))
    except Exception:
        return None

# TODO: Fix Marveltwin

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

for filename in filenames:
    print("...Opening", filename)
    with open(filename, "r") as fp:
        soup = Soup(fp)

    last_name = None
    for headline in soup.find_all(class_="mw-headline"):
        name = headline.string
        if last_name and (name in non_names or "." in name or re.match(r"\d+/\d+", name)):
            name = last_name + " " + name
        else:
            current_name = name
        subgroup = None
        comma_list = None
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
                subgroup = try_parse_subgroup(contents) or contents
            elif "comma" in lower:
                comma_list = contents
            elif "mapping" in lower:
                mapping = contents
            elif "generator" in lower:
                generator = contents
            elif "optimal" in lower:
                optimal = contents
            elif "badness" in lower:
                badness = contents
            node = node.next_sibling
        if subgroup and comma_list:
            print("==", name, "==")
            print(subgroup)
            print(comma_list)
            print(mapping)
            print(generator)
            print(optimal)
            print(badness)
            last_name = current_name
