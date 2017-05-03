#!/usr/bin/env python2.7
import psycopg2


def connect():
    return psycopg2.connect("dbname=news")


# ===========================================================
# 1. What are the most popular three articles of all time?
# ===========================================================
def top_three():
    """
        Returns top three posts
    """
    db = connect()
    c = db.cursor()
    query = """
               SELECT articles.title, count(log.path) as popularity
               FROM articles LEFT JOIN log
               ON log.path like CONCAT('%', articles.slug, '%')
               WHERE log.status != '404 NOT FOUND'
               GROUP BY articles.title
               ORDER BY popularity DESC
               LIMIT 3
           """
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("Top Three Posts:")
    print("----------------")
    for r in result:
        print("%s - %s views" % (r[0], r[1]))

top_three()
print("")


# ===========================================================
# 2. Who are the most popular article authors of all time?
# ===========================================================
def author_popularity():
    """
        Returns author popularity in descending order
    """
    db = connect()
    c = db.cursor()
    query = """
               SELECT authors.name, sum(top.popularity) as views
               FROM authors,
               (SELECT articles.author as author_id, count(log.path) as popularity
               FROM articles LEFT JOIN log
               ON log.path like CONCAT('%', articles.slug, '%')
               WHERE log.status != '404 NOT FOUND'
               GROUP BY articles.author) as top
               WHERE top.author_id = authors.id
               GROUP BY authors.name
               ORDER BY views DESC
           """
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("Most Popular Article Authors")
    print("----------------------------")
    for r in result:
        print("%s - %s views" % (r[0], r[1]))

author_popularity()
print("")


# ===========================================================
# 3. On which days did more than 1% of requests lead to errors?
# ==========================================================
def errors():
    """
        Returns request errors over 1 percent
    """
    db = connect()
    c = db.cursor()
    query = """
               SELECT *
               FROM
               (SELECT a.time::date,
               round(
               (count(a.status)::numeric * 100 / bit_or(b.total)::numeric), 1)
               AS yield
               FROM log as a,
               (SELECT time::date, count(*) as total
               FROM log
               GROUP BY time::date) as b
               WHERE a.time::date = b.time::date
               AND a.status = '404 NOT FOUND'
               GROUP BY a.time::date) as c
               WHERE c.yield > 1
           """
    c.execute(query)
    result = c.fetchall()
    db.close()
    print("Request Errors Over 1%")
    print("----------------------")
    for r in result:
        print("%s - %s%%" % (r[0], r[1]))

errors()
