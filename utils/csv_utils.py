import csv
from typing import List


def read_csv(filepath):
    """
    :return: a Python list of the csv rows
    """
    rows = []
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def write_csv(filepath: str, rows: List[any], fieldnames: List[str] = None):
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
