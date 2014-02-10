import csv
import urllib2
import time
import datetime


ward_index = 2
precinct_index = 3
mckenna_index = 4
rouse_index = 5

update_rate_seconds = 120

geoserverUrl = "http://localhost:8080/geoserver/ows"
csvUrl = "http://lasos.blob.core.windows.net/graphical-prod/20140315/csv/ByPrecinct_50208.csv"

update_template = """
    <wfs:Update typeName="feature:Voting_Precinct" xmlns:feature="http://opengeo.org">
        <wfs:Property>
            <wfs:Name>mckenna</wfs:Name>
            <wfs:Value>{}</wfs:Value>
        </wfs:Property>
        <wfs:Property>
            <wfs:Name>rouse</wfs:Name>
            <wfs:Value>{}</wfs:Value>
        </wfs:Property>
        <wfs:Property>
            <wfs:Name>mckenna_per</wfs:Name>
            <wfs:Value>{:.4f}</wfs:Value>
        </wfs:Property>
        <ogc:Filter>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>PRECINCTID</ogc:PropertyName>
                    <ogc:Literal>{}</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
        </ogc:Filter>
    </wfs:Update>
    """

transaction_template = """
    <wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs"
                     xmlns:ogc="http://www.opengis.net/ogc"
                     service="WFS"
                     version="1.1.0"
                     xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        {}
    </wfs:Transaction>"""


def get_csv_data(url):
    url_file = urllib2.urlopen(url)
    cvs_iter = csv.reader(url_file)
    headers = cvs_iter.next()
    rows = list(cvs_iter)
    return headers, rows


def sum_column(rows, col):
    return sum(int(row[col]) for row in rows)


def safe_percent(numerator, denominator):
    if denominator == 0:
        return 0.0
    return 100.0 * numerator / denominator


def print_precinct_totals(headers, rows):
    print "### CSV Precinct Summary ###"
    print "headers: {}".format(headers)

    precincts_total = len(rows)
    precincts_reporting = len([r for r in rows if int(r[mckenna_index]) > 0 or int(r[rouse_index]) > 0])
    print "{} of {} precincts reporting ({:.1f}%)".format(precincts_reporting,
                                                          precincts_total,
                                                          safe_percent(precincts_reporting, precincts_total))

    print "totals:"
    mckenna_votes = sum_column(rows, mckenna_index)
    rouse_votes = sum_column(rows, rouse_index)
    total_votes = mckenna_votes + rouse_votes
    template = "- {}: ({:.1f}%) {}"
    print template.format(mckenna_votes, safe_percent(mckenna_votes, total_votes), headers[mckenna_index])
    print template.format(rouse_votes, safe_percent(rouse_votes, total_votes), headers[rouse_index])


def build_update_xml(row):
    mckenna_votes = int(row[mckenna_index])
    rouse_votes = int(row[rouse_index])
    total_votes = mckenna_votes + rouse_votes
    mckenna_percent = safe_percent(mckenna_votes, total_votes)
    precinctid = row[ward_index].lstrip("0") + "-" + row[precinct_index].lstrip("0")
    return update_template.format(mckenna_votes, rouse_votes, mckenna_percent, precinctid)


def build_transaction_xml(rows):
    updates = [build_update_xml(row) for row in rows]
    return transaction_template.format("".join(updates))


def update():
    headers, rows = get_csv_data(csvUrl)
    print_precinct_totals(headers, rows)
    xml = build_transaction_xml(rows)
    # response = requests.post(geoserverUrl, data=xml)
    # print response.content


while True:
    update()
    print "Updates every", update_rate_seconds, "seconds. Last at", datetime.datetime.now()
    time.sleep(120)