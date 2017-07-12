# log_analysis
Reads data on a linux vm. Uses `get_most_viewed(query)` and `get_days_with_bad_requests(query)` in *newsdatadb.py*.

# QuickStart

## Prerequisites
-Python 2.7
-VM of linux

### Running the Program
1. Extract the folder *log_analysis.zip*
2. Open up the file with vagrant
3. Use Git Bash to run vagrant
4. Open *newsdatadb.py* in a word editor
5. Select a method in *newsdatadb.py* and enter a query.
6. Run command `python newsdatadb.py`

### Views 
- all_requests = SELECT date_trunc('day'::text, log."time") AS day,count(*) AS num FROM log GROUP BY (date_trunc('day'::text, log."time"));

- bad_requests =  SELECT date_trunc('day'::text, log."time") AS day,  count(*) AS num FROM log WHERE (log.status <> '200 OK'::text) GROUP BY (date_trunc('day'::text, log."time"));
- bad_percent_v2 =  SELECT all_requests.day, round(((((bad_requests.num)::double precision / (all_requests.num)::double precision) * (100)::double precision))::numeric, 1) AS percent FROM all_requests, bad_requests WHERE (all_requests.day = bad_requests.day);
