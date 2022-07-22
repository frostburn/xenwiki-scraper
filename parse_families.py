import os

from utils import Soup

non_names = ["5-limit", "7-limit", "11-limit", "13-limit", "17-limit", "19-limit", "23-limit"]

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
        if "." in line:
            return list(map(int, line.split(".")))
    except Exception:
        return None


directory = "downloads/families"
for filename in os.listdir(directory):
    base, ext = os.path.splitext(filename)
    if ext != ".html":
        continue
    print("...Opening", filename)
    with open(os.path.join(directory, filename), "r") as fp:
        soup = Soup(fp)

    last_name = None
    for headline in soup.find_all(class_="mw-headline"):
        name = headline.string
        if name in non_names:
            name = last_name + " " + name
        else:
            last_name = name
        subgroup = None
        comma_list = None
        mapping = None
        generator = None
        optimal = None
        badness = None
        node = headline.parent.next_sibling
        while node and getattr(node, "name", None) not in ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"]:
            contents = string_contents(node).strip()
            lower = contents.lower()
            if "subgroup" in lower and not isinstance(subgroup, list):
                subgroup = try_parse_subgroup(contents) or contents
            elif "comma list" in lower:
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
