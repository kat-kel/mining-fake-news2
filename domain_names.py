from collections import Counter
import csv


with open("data/private.ural_results.csv", "r") as f:
    reader = csv.DictReader(f)
    static_domains = [row["domain"] for row in reader]

count = dict(Counter(static_domains).most_common())

with open("data/test_domain_count.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "count"])
    for key,value in count.items():
        writer.writerow([key,value])
    