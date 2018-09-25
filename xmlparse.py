#!/usr/local/bin/python3

import xml.etree.ElementTree as ET
from io import StringIO
import os
import codecs
import argparse
import getpass
import time
import json
import csv
import sys
import datetime
import random

# to go through all xml files in a directory

path = os.getcwd()
for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue

    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    root = tree.getroot()


def export(env):

    global token
    global refresh_token
    global token_time

    if env == "prod":
        base_url = "https://app.alegion.com/api/v1/batches/%s/results/?pageSize=1000" % batch_id
    if env == "staging":
        base_url = "https://app-staging.alegion.com/api/v1/batches/%s/results/?pageSize=1000" % batch_id

    results = ""

    # if the user passed in a first page start exporting on page <n> 
    if first_page:
        next_page = first_page
    else:
        next_page = 1

    url = base_url
    os.makedirs(outPath+'/files')

    while url:

        # get a new token if it's been > 45sec
        token_age = time.time() - token_time
        if token_age > 30:
            token, refresh_token, token_time = get_token(user, pw, type="refresh")
            print "refreshing token (%ss old)" % token_age

        url += "&page=%s&sort=-createdAt" % next_page

        if last_page:
            if next_page == (last_page + 1):
                break

        t0 = time.time()

        # make sure we have the latest token
        headers = {
            'authorization': "Bearer %s" % token,
            'cache-control': "no-cache",
            'accept': "text/csv"
        }

        response = requests.get(url=url, headers=headers)

        # strip off the trailing newline so that we cleanly concatenate multiple exports
        results = response.text.rstrip()

        # Get count of rows to print results, start at -1 to account for header
        record_count = -1
        reader = csv.reader(StringIO.StringIO(results.encode('utf-8')), csv.excel)
        for row in reader:
            record_count += 1
        print "  %s records" % record_count, "   elapsed time %ss" % round((time.time() - running_time), 2)

        filename = "exported_%s_pg%s.csv" % (batch_id, next_page)
        file = "%s/%s" % (subOutPath, filename)
        f = codecs.open(file, "wb+", "utf-8")
        f.write(results)
        f.close()

        print "\nsaved %s\n" % filename

        # set url to the next page
        try:
            next_page += 1
            url = base_url + "&page=%s&sort=-createdAt" % next_page

        # we're done when there's a KeyError
        except KeyError:
            break