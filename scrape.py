import mwclient
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def first_rev_of_the_day(pg, date):
    revs = pg.revisions(start=date.strftime('%F %T'), dir='newer',
            prop='content',
            limit=1,
            )
    return revs.next()

def age_for_row(rowstr):
    """Example rowstr:
| 2022-04-19 12:27 || style="text-align: center" | 3 || 2022-04-19 12:27 || [[Talk:Whitelisting#Requested move 19 April 2022|Discuss]] || [[:Whitelisting]] → {{no redirect|Whitelist}}
    """
    parts = rowstr.split('||')
    assert len(parts) == 5
    age_part = parts[1]
    tokens = age_part.split('|')
    age_str = tokens[-1].strip()
    if age_str == '< 1':
        age = 0
    else:
        age = int(age_str)
    return age

def munge_ages(ages):
    buckets = [0, 0, 0, 0, 0]
    for age in ages:
        ix = min(age//7, len(buckets)-1)
        buckets[ix] += 1
    return buckets

def data_for_revision(rev):
    src = rev['*']
    ages = []
    for line in src.split('\n'):
        if not line.startswith('| '):
            continue
        age = age_for_row(line)
        if age > 1000:
            print("WARNING: Skipping crazy long age, ", age,
                    "for row:\n", line)
            continue
        ages.append(age)
    bucketed = munge_ages(ages)
    dat = {
            f'w{n}': bucketed[n]
            for n in range(len(bucketed))
    }
    dat['total'] = len(ages)
    dat['mean_age'] = np.mean(ages)
    return dat


wiki = mwclient.Site('en.wikipedia.org')
title = 'Wikipedia:Requested moves/Current discussions (table)'

pg = wiki.pages[title]

# First revisions of 4-21
pg.revisions(start='2022-04-21T00:00:00Z', dir='newer')

DAY = timedelta(days=1)
START = datetime(2022, 4, 22)
# Oldest full day of table data is May 5 2017. Though the age column doesn't
# appear until May 6.
END = datetime(2017, 5, 22)

curr_date = START
dat_per_day = []
while curr_date >= END:
    rev = first_rev_of_the_day(pg, curr_date)
    dat = data_for_revision(rev)
    dat['date'] = curr_date.date()
    dat_per_day.append(dat)
    curr_date -= DAY

df = pd.DataFrame(dat_per_day)

df.to_csv('rms.csv', index=False)
