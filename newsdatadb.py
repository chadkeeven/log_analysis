#!/usr/bin/env python
import psycopg2
from datetime import datetime

DBNAME = "news"

most_viewed_3articles_query = """select articles.title, count(path) as num
 from articles, log
 where log.status = '200 OK'
 and log.path = concat('/article/', articles.slug)
 group by articles.title
 order by num desc limit 3;"""
most_author_views_query = """select authors.name, count(path) as num
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


def run_query(query):

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close


def get_top3_viewed_articles():

    results = run_query(most_viewed_3articles_query)
    print "The top three articles viewed:"
    for r in results:
        print str(r[0]) + " -- " + str(r[1]) + " views"


def get_most_popular_authors():

    results = run_query(most_author_views_query)
    print "The most popular authors:"
    for r in results:
        print str(r[0]) + " -- " + str(r[1]) + " views"


def get_days_with_bad_requests():

    results = run_query(bad_requests_query)
    print "Days with more than 1% of bad requests:"
    for r in results:
        date = str(r[0])
        fmt_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d,%Y")
        print fmt_date + " -- " + str(r[1]) + "% errors"
