#!/usr/bin/env python
import psycopg2
from datetime import datetime

DBNAME = "news"

most_viewed_3articles_query = """select articles.title, count(path) as num
 from articles, log
 where log.status = '200 OK'
 and articles.slug = substring(log.path from articles.slug)
 group by articles.title
 order by num desc limit 3;"""
most_author_views_query = """"select authors.name, count(path) as num
 from articles, log, authors
 where log.status = '200 OK'
 and articles.slug= substring(log.path from articles.slug)
 and authors.id = articles.author
 group by authors.name
 order by num desc;"""
bad_requests_query = """select cast(all_requests.day as date),
 bad_percent_v2.percent
 from all_requests, bad_percent_v2
 where all_requests.day = bad_percent_v2.day
 and bad_percent_v2.percent > 1.0;"""


def get_most_viewed(query):

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    for r in results:
        print str(r[0]) + " -- " + str(r[1]) + " views"
    return results
    db.close


def get_days_with_bad_requests(query):

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    for r in results:
        date = str(r[0])
        formated_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d,%Y")
        print formated_date + " -- " + str(r[1]) + "% errors"
    return results
    db.close
