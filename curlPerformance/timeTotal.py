#!/usr/bin/env python
import sys

fl = sys.argv[-1]
time_total = 0.0
totals = 0

''' Read text file line by line'''
with open(fl) as text_file:
    for line in text_file:
        if 'time_total' in line:
            for x in line.split():
                try:
                    time_total += float(x)
                    totals += 1
                except Exception:
                    pass
print(f'Total time average: {round(time_total/totals, 3)} secs')
print(f'Number of requests: {totals}')
