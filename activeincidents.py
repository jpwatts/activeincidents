#!/usr/bin/env python3

import collections
import hashlib
import logging
import sqlite3
import sys
import time

import lxml.html

import requests


URL = "http://cohweb.houstontx.gov/ActiveIncidents/Combined.aspx"


logger = logging.getLogger(__name__)


Report = collections.namedtuple(
    'Report',
    (
        'agency',
        'address',
        'cross_street',
        'key_map',
        'call_time',
        'incident_type',
        'combined_response',
        'hash',
        'scrape_time'
    )
)


def iter_scrape(url=URL):
    scrape_time = int(time.time())
    with requests.get(url) as response:
        response.raise_for_status()
        tree = lxml.html.fromstring(response.text, base_url=url)
        for tr in tree.xpath('//*[@id="GridView2"]/tr[position()>1]'):
            fields = [td.text_content().strip() for td in tr.xpath('td')]
            fields.append(hashlib.sha1(b"".join(s.encode() for s in fields)).hexdigest())
            fields.append(scrape_time)
            yield Report(*fields)


def scrape():
    return list(iter_scrape())


_DUMP_CREATE = """CREATE TABLE IF NOT EXISTS report (
    agency TEXT NOT NULL,
    address TEXT NOT NULL,
    cross_street TEXT NOT NULL,
    key_map TEXT NOT NULL,
    call_time TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    combined_response TEXT NOT NULL,
    hash TEXT NOT NULL UNIQUE,
    scrape_time INTEGER NOT NULL
)"""

_DUMP_INSERT = "INSERT OR REPLACE INTO report VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

def dump(path):
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute(_DUMP_CREATE)
        cursor.executemany(_DUMP_INSERT, iter_scrape())


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        path = sys.argv[1]
    except IndexError:
        path = "activeincidents.db"
    dump(path)


if __name__ == '__main__':
    main()

