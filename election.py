import csv
import urllib2

geoserverUrl = "http://localhost:8080/geoserver/ows"
csvUrl = "http://lasos.blob.core.windows.net/graphical-prod/20140201/csv/ByPrecinct_47474.csv"


def get_csv_data(url):
    url_file = urllib2.urlopen(url)
    cvs_iter = csv.reader(url_file)
    headers = cvs_iter.next()
    rows = list(cvs_iter)
    return headers, rows


def sum_column(rows, col):
    return sum([int(row[col]) for row in rows])


def print_precinct_totals(headers, rows):
    candidate_cols = [4, 5, 6]

    print "### CSV Precinct Summary ###"
    print "headers: {}".format(headers)

    precincts_total = len(rows)
    is_reporting = lambda row: any(row[col] > 0 for col in candidate_cols)
    precincts_reporting = len(filter(is_reporting, rows))
    print "{} of {} precincts reporting".format(precincts_reporting, precincts_total)

    print "totals:"
    total_votes = sum(sum_column(rows, col) for col in candidate_cols)
    for col in candidate_cols:
        name = headers[col]
        votes = sum_column(rows, col)
        percent = 100.0 * votes / total_votes
        print "- {}: ({:.1f}%) {}".format(votes, percent, name)


def print_upload_sql(rows):
    for row in rows:
        culotta = row[4]
        mckenna = row[5]
        rouse = row[6]
        precinctid = row[2].lstrip("0") + "-" + row[3].lstrip("0")
        total = int(culotta) + int(mckenna) + int(rouse)
        mckenna_percent = -1
        if total > 0:
            mckenna_percent = float(mckenna) / total
        mckenna_percent = 1 - mckenna_percent
        print """update "Voting_Precinct" set culotta={}, mckenna={}, rouse={}, mckenna_per={:.4f} where "PRECINCTID" = '{}';""".format(
            culotta, mckenna, rouse, mckenna_percent, precinctid)


headers, rows = get_csv_data(csvUrl)
print_precinct_totals(headers, rows)
print_upload_sql(rows)

#print
#print "### requests test ###"
#payload = {'key1': 'value1', 'key2': 'the nature of things'}
#r = requests.post("http:#httpbin.org/post", data=payload)
#print r.json()
