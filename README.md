# log_analysis
Reads data on a linux vm. Uses `run_query(query)` to fetch query results for `get_top3_viewed_articles()`, `get_most_popular_authors()` and `get_days_with_bad_requests()` in *newsdatadb.py*.

# QuickStart

## Prerequisites
-Python 2.7
-VM of linux
-import newsdata.sql into news database

### Running the Program
1. Extract the folder *log_analysis.zip*
2. Open up the file with vagrant
3. Use Git Bash to run vagrant
4. Open *newsdatadb.py* in a word editor
5. Select a method in *newsdatadb.py*
6. Run command `python newsdatadb.py`

### Views 
CREATE VIEW all_requests AS SELECT date_trunc('day'::text, log."time") AS day,count(*) AS num FROM log GROUP BY (date_trunc('day'::text, log."time"));

CREATE VIEW bad_requests AS SELECT date_trunc('day'::text, log."time") AS day,  count(*) AS num FROM log WHERE (log.status <> '200 OK'::text) GROUP BY (date_trunc('day'::text, log."time"));

CREATE VIEW bad_percent_v2 AS SELECT all_requests.day, round(((((bad_requests.num)::double precision / (all_requests.num)::double precision) * (100)::double precision))::numeric, 1) AS percent FROM all_requests, bad_requests WHERE (all_requests.day = bad_requests.day);
