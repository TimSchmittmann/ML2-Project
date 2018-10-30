#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv


csv_to_fix = "data/german_tweets_text_id_only_586335_samples_desc.csv"

with open(csv_to_fix, 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    with open(csv_to_fix+"_fixed.csv", 'w', encoding='utf-8', newline='', buffering=1) as fixedcsv:
        writer = csv.DictWriter(fixedcsv, delimiter=';', fieldnames=['id', 'text'],
                        quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in reader:
            if row == ['id', 'text']:
                print(row)
                continue
            writer.writerow({'id':row[0], 'text': row[1]})
            