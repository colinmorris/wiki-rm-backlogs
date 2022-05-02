Visualizing the size of the backlog of [Requested Move discussions on Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Requested_moves) over time.

`scrape.py` walks through the revision history of [this bot-updated listing of RM discussions](https://en.wikipedia.org/wiki/Wikipedia:Requested_moves/Current_discussions_(table)) grabbing structured data about the backlog size at the beginning of each day (or other time period, e.g. week). This is saved to a csv file (`rms.csv`), with the following columns:

- `w0`, `w1`, `w2`...: Number of active discussions where 7n <= age in days < 7(n+1), with the exception of `w4`, which counts *all* discussions with age > 28 days.
- `total`: Total number of active discussions, i.e. sum of the previous 5 columns
- `mean_age`: Average age of active discussions
- `date`: Date of this observation. Numbers correspond specifically to the earliest revision of WP:RMTABLE that falls on this date.

`visualizations.ipynb` is an IPython notebook that generates some visualizations from this data using Seaborn/Matplotlib/Pandas.
- 
