import csv


def read_csv(filepath):
    rows = []
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
