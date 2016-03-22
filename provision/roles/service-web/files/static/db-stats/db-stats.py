#!/usr/bin/env python


import psycopg2


def get_stats():
    output = "DATABASE: dbstats\n"
    conn = psycopg2.connect(
                dbname='dbstats',
                user='dbstats',
                password='dbstats',
                host='172.20.20.10'
    )
    cur = conn.cursor()
    cur.execute("""SELECT table_schema, table_name FROM information_schema.tables;""")
    recs = cur.fetchall()
    for rec in recs:
        output += "* {0}.{1}\n".format(*rec)
    conn.close()

    return str(output)


def application(environ, start_response):
    response = get_stats()
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(response)))
    ]

    status = '200 OK'
    start_response(status, response_headers)
    return [response]


if __name__ == "__main__":
    print get_stats()


# vim: set ts=8 sts=4 sw=4 et:
