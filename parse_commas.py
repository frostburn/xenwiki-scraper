from fractions import Fraction
import re
import os
import json
from utils import Soup, LOG_PRIMES, PRIMES
from numpy import dot
from pathlib import Path

EPSILON = 0.1

def to_monzo(value):
    value = Fraction(value.strip())
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
    while not result[-1]:
        result.pop()
    return result

def clean_name(name):
    return re.sub(r"\[\d\]", "", name.strip())

def parse_row(data, headers, offset_names=False):
    offset = 0
    ratio_index = None
    name_index = None
    monzo_index = None
    cents_index = None
    for i, header in enumerate(headers):
        header = header.lower()
        if 'color' in header:
            offset += 1
        elif 'name' in header and name_index is None:
            name_index = i + offset
            if offset_names:
                offset += 1
        elif 'monzo' in header and monzo_index is None:
            monzo_index = i + offset
        elif 'cents' in header and cents_index is None:
            cents_index = i + offset
        elif 'ratio' in header and ratio_index is None:
            ratio_index = i + offset
    names = list(filter(None, [clean_name(name) for name in data[name_index].split(",")]))
    if not names:
        raise ValueError("No names found")
    monzo = [int(c) for c in filter(None, data[monzo_index].strip("[⟩>").replace(",", " ").split(" "))]
    if not monzo:
        monzo = to_monzo(data[ratio_index])
    size = dot(LOG_PRIMES[:len(monzo)], monzo) / LOG_PRIMES[0] * 1200
    cents = float(data[cents_index].replace(" ", "").replace("×10", "e"))
    if abs(size - cents) > EPSILON:
        raise ValueError(f"Size mismatch {size} vs {cents}: {names[0]}")
    return [names, monzo]


def to_key(monzo):
    size = dot(LOG_PRIMES[:len(monzo)], monzo) / LOG_PRIMES[0] * 1200
    if size < -1e-7:
        raise ValueError("Negative monzo")
    if size >= 1200:
        raise ValueError("Monzo too large")
    return ",".join(str(c) for c in monzo[1:])

filenames = []
comma_directory = "downloads/commas"
for filename in os.listdir(comma_directory):
    filenames.append(os.path.join(comma_directory, filename))

result = {"": ["perfect prime","tonic","unity"]}

for filename in filenames:
    offset_names = False
    if '3-limit' in filename:
        offset_names = True
    print("Opening", filename)
    with open(filename, "r") as fp:
        soup = Soup(fp)
        for table in soup.find_all(name="table"):
            headers = []
            for th in table.find_all("th"):
                headers.append(th.text.strip())
            for row in table.find_all("tr"):
                data = []
                for cell in row.find_all("td"):
                    for br in cell.find_all("br"):
                        br.replace_with(",")
                    data.append(cell.text.strip())
                if data:
                    try:
                        names, monzo = parse_row(data, headers, offset_names)
                        key = to_key(monzo)
                        if key in result:
                            existing = [name.lower() for name in result[key]]
                            for name in names:
                                if name.lower() not in existing:
                                    result[key].append(name)
                        else:
                            result[key] = names
                    except ValueError as e:
                        print("Failed to parse", data)

json_path = Path("json")
json_path.mkdir(parents=True, exist_ok=True)

with open(json_path / "commas.json", "w") as fp:
    json.dump(result, fp, indent=None, separators=[",", ":"])
